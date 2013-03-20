# Taken and modified from:
# http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

import os
import sys
import atexit
import signal
import time
import logging
import logging.handlers
if sys.platform == 'win32':
    import win32service
    import win32serviceutil
    import win32api
    import win32con
    import win32event
    import servicemanager

from DTL.api.logger import Logger

if (hasattr(os, "devnull")):
    DEVNULL = os.devnull
else:
    DEVNULL = "/dev/null"


#------------------------------------------------------------
#------------------------------------------------------------
class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the mainloop() and shutdown() method
    """
    __metaclass__ = Logger
    #------------------------------------------------------------
    def __init__(self, serviceName, pidfile, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL):
        super(Daemon, self).__init__()

        self._serviceName = serviceName
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        self._pidfile = pidfile
        self._continue = True

    #------------------------------------------------------------
    def _daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self._stdin, 'r')
        so = file(self._stdout, 'a+')
        se = file(self._stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile and subsys file
        pid = str(os.getpid())
        file(self._pidfile,'w+').write("%s\n" % pid)
        if os.path.exists('/var/lock/subsys'):
            fh = open(os.path.join('/var/lock/subsys', self._serviceName), 'w')
            fh.close()

    #------------------------------------------------------------
    def _delpid(self):
        if os.path.exists(self._pidfile):
            os.remove(self._pidfile)

        subsysPath = os.path.join('/var/lock/subsys', self._serviceName)
        if os.path.exists(subsysPath):
            os.remove(subsysPath)

        self.shutdown()

    #------------------------------------------------------------
    def _start(self, daemonize=True):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self._pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self._pidfile)
            sys.exit(1)

        # Start the daemon
        if daemonize:
            self._daemonize()

        # Cleanup handling
        def termHandler(signum, frame):
            self._delpid()
        signal.signal(signal.SIGTERM, termHandler)
        atexit.register(self._delpid)

        # Run the daemon
        self.mainloop()

    #------------------------------------------------------------
    def _stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self._pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self._pidfile)
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self._pidfile):
                    os.remove(self._pidfile)
            else:
                print str(err)
                sys.exit(1)

    #------------------------------------------------------------
    # Begin Overrides
    #------------------------------------------------------------
    def start(self):
        if sys.platform == 'win32':
            self._start(daemonize=False)
        else:
            self._start()

    #------------------------------------------------------------
    def stop(self):
        self._continue = False
        self._stop()

    #------------------------------------------------------------
    def foreground(self):
        self._start(daemonize=False)

    #------------------------------------------------------------
    def restart(self):
        self.stop()
        self.start()

    #------------------------------------------------------------
    def mainloop(self):
        while self._continue :
            self.logger.info("Daemon is running!")
            time.sleep(2)

    #------------------------------------------------------------
    def shutdown(self):
        pass

#------------------------------------------------------------
if sys.platform == 'win32':
    class WindowsService(win32serviceutil.ServiceFramework):
        """
        Windows service wrapper
        """
        _svc_name_ = '_unNamed'
        _svc_display_name_ = '_Service Template'
        
        #------------------------------------------------------------
        def __init__(self, *args):
            win32serviceutil.ServiceFramework.__init__(self, *args)
            self.stop_event = win32event.CreateEvent(None, 0, 0, None)
            self.isAlive = True
            self.logger = logging.getLogger()
        
        #------------------------------------------------------------
        def log(self, msg):
            servicemanager.LogInfoMsg(str(msg))
            self.logger.info(str(msg))
        
        #------------------------------------------------------------
        def sleep(self, sec):
            win32api.Sleep(sec*1000, True)
        
        #------------------------------------------------------------
        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            self.stop()
            win32event.SetEvent(self.stop_event)
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        
        #------------------------------------------------------------
        def SvcDoRun(self):
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            try:
                self.ReportServiceStatus(win32service.SERVICE_RUNNING)
                self.start()
                win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            except Exception, x:
                self.SvcStop()
        
        #------------------------------------------------------------
        def start(self):
            raise NotImplementedError("")
        
        #------------------------------------------------------------
        def stop(self):
            raise NotImplementedError("")


class TestService(WindowsService):
    _svc_name_ = 'MyTestService'
    _svc_display_name_ = 'My Test Service'    
    #------------------------------------------------------------
    def start(self):
        while self.isAlive :
            for i in range(2):
                self.log("I'm Alive")
            self.sleep(1)
            self.isAlive = False
        
        self.SvcStop()
    
    #------------------------------------------------------------
    def stop(self):
        pass

if __name__ == "__main__":
    if sys.platform == 'win32':
        win32serviceutil.HandleCommandLine(TestService)
    else:
        print "Unix"
        daemon = Daemon('Testing','c:/test.pid')
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                daemon.start()
            elif 'stop' == sys.argv[1]:
                daemon.stop()
            elif 'restart' == sys.argv[1]:
                daemon.restart()
            elif 'foreground' == sys.argv[1]:
                daemon.foreground()
            else:
                print "Unknown command"
                sys.exit(2)
                sys.exit(0)
        else:
            print "usage: %s start|stop|restart|foreground" % sys.argv[0]
            sys.exit(2)