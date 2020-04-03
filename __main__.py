import callmanager
import time
import signal
import threading
import logging
import ringer
import callmanager_events as cme



class App:
    def __init__(self):
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

    def call_accepted(self):
        self.ringer.stop()

    def call_declined(self):
        self.ringer.stop()

    def incoming_call(self, event):
        # TODO: ringing is blocked by something. Audio stuttering
        print("Starting ringing!")
        thread = threading.Thread(target=self.ringer.ring)
        thread.start()
        #self.ringer.ring()

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
