import datetime

from DTL.api import loggingUtils

#------------------------------------------------------------
#------------------------------------------------------------
class Stopwatch(object):
    __metaclass__ = loggingUtils.LoggingMetaclass
    #------------------------------------------------------------
    def __init__(self, name):
        self._name = str(name)
        self._count = 0
        self._lapStack = []

        self.reset()
    
    #------------------------------------------------------------
    def newLap(self, message):
        """ Convenience method to stop the current lap and create a new lap """
        self.stopLap()
        self.startLap(message)
    
    #------------------------------------------------------------
    def reset( self ):
        self._starttime = datetime.datetime.now()
        self._laptime	= None
        self._records	= []
        self._laps	= []
    
    #------------------------------------------------------------
    def startLap( self, message ):
        self._lapStack.append( (message,datetime.datetime.now()) )
        return True
    
    #------------------------------------------------------------
    def stop( self ):
        # pop all the laps
        while ( self._lapStack ):
            self.stopLap()

        ttime = str(datetime.datetime.now() - self._starttime)

        # output the logs
        self.log.info('Time:{0} | {1} Stopwatch'.format(ttime,self._name))
        for record in self._records :
            self.log.info(record)
        
        return True
    
    #------------------------------------------------------------
    def stopLap( self ):
        if ( not self._lapStack ):
            return False

        curr = datetime.datetime.now()

        message, sstart = self._lapStack.pop()

        # process the elapsed time
        elapsed		= str(curr - sstart)
        if ( not '.' in elapsed ):
            elapsed += '.'

        while ( len( elapsed ) < 14 ):
            elapsed += '0'

        # record a lap
        self._records.append('\tlap: {0} | {1}'.format(elapsed, message))


if __name__ == "__main__":
    import time
    timer = Stopwatch("Test")
    def myFunc():
        time.sleep(1)
    
    
    for i in range(5):
        myFunc()
    timer.stop()
    