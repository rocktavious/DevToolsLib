import sys
import threading

class CommandTicker(threading.Thread):
    '''A threading class for command line operations that will take a long time and need a "i'm processing" gui type of bar'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        ticks = ['[.  ]', '[.. ]', '[...]', '[ ..]', '[  .]', '[   ]']
        i = 0
        first = True
        while True:
            self.stop_event.wait(0.25)
            if self.stop_event.isSet(): break
            if i == len(ticks):
                first = False
                i = 0
            if not first:
                sys.stderr.write("\r%s\r" % ticks[i])
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
        ticker_thread.join()