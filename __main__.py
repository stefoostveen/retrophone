import callmanager
import time
import signal
import threading
import logging
import ringer
import callmanager_events as cme
import displaymanager
import scene as scn


class App:
    def __init__(self):
        self.displaymgr = displaymanager.DisplayManager()
        scene = scn.Scene().add_animation("reg_start")
        self.displaymgr.set(scene)

        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        self.callmgr = callmanager.CallManager()
        self.callmgr.subscribe(self.incoming_call, cme.CM_CALL_INCOMING)
        self.callmgr.subscribe(self.call_accepted, cme.CM_CALL_ACCEPTED)
        self.callmgr.subscribe(self.call_declined, cme.CM_CALL_ENDED)

        self.ringer = ringer.Ringer()

        self.callmgr.register()
        self.server = ["http://", "phone.local"]

        print("Registration phase finished")
        self.runapp()

    def shutdown(self):
        self.callmgr.unregister()

    def registration_complete(self, event):
        if event.code == 403:
            screen = scn.Scene().add_animation("reg_perm_fail")
            self.displaymgr.set(screen)
            screen = scn.FaultScene("Wrong username or password supplied. Visit "+self.server[0] + self.server[1] + " to resolve.")
            self.displaymgr.show(screen)
        elif event.code == 200:
            self.displaymgr.show_home_screen()
            screen = scn.SuccessScene("Now able to make and accept calls.")
            self.displaymgr.show(screen)
        else:
            screen = scn.FaultScene("Unknown connection error. Visit "+self.server[0] + self.server[1] + " to resolve.")
            self.displaymgr.show(screen)

    def call_accepted(self, event):
        self.ringer.stop()

    def call_declined(self, event):
        self.ringer.stop()

    def incoming_call(self, event):
        # Solved: ringing is blocked by something. Audio stuttering -- edit: I think this is caused by the thread calling this method. It's actually called via a callback
        print("Starting ringing!")
        self.ringer.ring()

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
