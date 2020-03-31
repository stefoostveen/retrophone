import callmanager
import time
import signal



class App:
    def __init__(self):
        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        self.callmgr = callmanager.CallManager()
        self.callmgr.register()
        signal.pause()

    def shutdown(self):
        self.callmgr.unregister()

    def keyboardInterruptHandler(self, signal, frame):
        print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
        exit(0)


if __name__ == '__main__':
    App()
