import sys
import time

from DTL.api.threadlib import ThreadedProcess

class CommandTicker(ThreadedProcess):
    '''A threading class for command line operations that will take a long time and need a "i'm processing" gui type of bar'''
    TICKS = ['[.  ]', '[.. ]', '[...]', '[ ..]', '[  .]', '[   ]']
    #------------------------------------------------------------
    def __init__(self, **kwds):
        ThreadedProcess.__init__(self, **kwds)
        
    #------------------------------------------------------------
    def run(self):
        i = 0
        first = True        
        while self.isMainloopAlive():
            time.sleep(.25)
            if i == len(self.TICKS):
                first = False
                i = 0
            if not first:
                sys.stderr.write("\r%s\r" % self.TICKS[i])
                sys.stderr.flush()
            i += 1
        
        sys.stderr.flush()  


#This example runs best standalone in a console
if __name__ == '__main__':
    import time
    # Start a ticker
    ticker_thread = CommandTicker()
    ticker_thread.start()
    # This is the potentially long-running call.
    try:
        for i in range(20):
            time.sleep(1)
        
        print "Finished"
    except KeyboardInterrupt:
        raise Exception("Keyboard interruption detected")
    finally:
        # Tell the ticker to stop.
        ticker_thread.stop()