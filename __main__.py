import callmanager
import time
import signal
import threading



class App:
    def __init__(self):
        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        self.callmgr = callmanager.CallManager()
        self.callmgr.register()
        #threading.Thread(target=self.callmgr.register).run()
        #threading.active_count()
        print("We're free!")
        self.runapp()

    def shutdown(self):
        self.callmgr.unregister()

    def keyboardInterruptHandler(self, signal, frame):
        print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
        exit(0)

    def runapp(self):
        while True:
            # Do some polling due to threadcnt being zero: https://www.pjsip.org/pjsip/docs/html/classpj_1_1Endpoint.htm#ade134bcab9fdbef563236237034ec3ec
            self.callmgr.run()
            time.sleep(0.1)


if __name__ == '__main__':
    App()
