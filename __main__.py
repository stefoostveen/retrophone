import callmanager
import time
import signal
import threading
import logging
import ringer
import callmanager_events as cme
import queue


class App:
    def __init__(self):
        self.timer = threading.Timer(1,self.accept_call)
        self.callback_queue = queue.Queue()

        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        self.callmgr = callmanager.CallManager()
        self.callmgr.subscribe(self.incoming_call, cme.CM_CALL_INCOMING)
        self.callmgr.subscribe(self.call_accepted, cme.CM_CALL_ACCEPTED)
        self.callmgr.subscribe(self.call_declined, cme.CM_CALL_ENDED)

        self.ringer = ringer.Ringer()

        self.callmgr.register()

        print("Registration phase finished")
        self.runapp()

    def shutdown(self):
        self.callmgr.unregister()

    def call_accepted(self, event):
        pass
        self.ringer.stop()

    def call_declined(self, event):
        pass
        self.ringer.stop()

    def incoming_call(self, event):
        # Solved: ringing is blocked by something. Audio stuttering -- edit: I think this is caused by the thread calling this method. It's actually called via a callback
        print("Starting ringing!")
        self.ringer.ring()
        self.timer.start()

    def accept_call(self):
        print("put in queue")
        self.callback_queue.put(self.callmgr.accept_call)
        #self.callmgr.accept_call()

    def keyboardInterruptHandler(self, signal, frame):
        print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
        exit(0)

    def runapp(self):
        while True:
            if not self.callback_queue.empty():
                cb = self.callback_queue.get(False)  # doesn't block
                cb()
            # Do some polling due to threadcnt being zero: https://www.pjsip.org/pjsip/docs/html/classpj_1_1Endpoint.htm#ade134bcab9fdbef563236237034ec3ec
            self.callmgr.run()
            time.sleep(0.1)


if __name__ == '__main__':
    App()
