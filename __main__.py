import callmanager
import time
import signal
import threading
import logging
import ringer
import callmanager_events as cme
import displaymanager
import scene as scn
import dial


class App:
    def __init__(self):
        self.displaymgr = displaymanager.DisplayManager(23)
        scene = scn.Scene()
        scene.add_animation("reg_start", picture_duration=100)
        self.displaymgr.set_scene(scene)
        time.sleep(1)

        self.dialmgr = dial.Dial(25,24,18)
        self.dialmgr.subscribe(self.hook_event, cme.DIAL_HOOK_CHANGE)
        self.dialmgr.subscribe(self.number_received, cme.DIAL_DIALING_COMPLETE)
        self.dialmgr.subscribe(self.digit_added_to_number, cme.DIAL_NUMBER_UPDATED)

        signal.signal(signal.SIGINT, self.keyboardInterruptHandler)
        self.callmgr = callmanager.CallManager()
        self.callmgr.subscribe(self.incoming_call, cme.CM_CALL_INCOMING)
        self.callmgr.subscribe(self.call_accepted, cme.CM_CALL_ACCEPTED)
        self.callmgr.subscribe(self.call_declined, cme.CM_CALL_ENDED)
        self.callmgr.subscribe(self.registration_complete, cme.CM_ACCOUNT_REG_COMPLETE)

        self.ringer = ringer.Ringer()

        self.callmgr.register()
        self.server = ["http://", "phone.local"]

        self.dialing_allowed = False

        print("Registration phase finished")
        self.runapp()

    def shutdown(self):
        scene = scn.Scene()
        scene.add_animation("app_shutdown", picture_duration=100)

        self.displaymgr.set_scene(scene)
        self.callmgr.unregister()

        scene = scn.Scene()
        scene.add_animation("app_remove_power", picture_duration=100)
        self.displaymgr.set_scene(scene)

    def registration_complete(self, event):
        if event.code == 403:
            scene = scn.Scene()
            scene.add_animation("reg_perm_fail")
            self.displaymgr.set_scene(scene)
            scene = scn.FaultScene("Wrong username or password supplied. Visit "+self.server[0] + self.server[1] + " to resolve.")
            self.displaymgr.show_scene(scene)
        elif event.code == 200:
            self.displaymgr.set_home_screen()
            scene = scn.SuccessScene("Now able to make and accept calls.")
            self.displaymgr.show_scene(scene)
        else:
            scene = scn.FaultScene("Unknown connection error. Visit "+self.server[0] + self.server[1] + " to resolve.")
            self.displaymgr.show_scene(scene)

    def hook_event(self, event):
        # end everything if hook is thrown on
        if event.on_hook:
            self.callmgr.end_calls()
            self.displaymgr.set_home_screen()
            self.allow_dialing(False)
        else:
            # hook is picked up. Answer call if exists or play dial tone if registered
            if not self.callmgr.account.call and self.callmgr.account.isValid():
                self.allow_dialing(True)
            else:
                self.callmgr.accept_call()

    def digit_added_to_number(self, event):
        if self.dialing_allowed:
            scene = scn.Scene()
            scene.add_text(str(event.phone_number))
            self.displaymgr.set_scene(scene)

    def number_received(self, event):
        # todo: change outgoing sip address to something valid
        if self.dialing_allowed:
            self.allow_dialing(False)
            self.callmgr.invoke_call("sip:"+event.phone_number+"@sip.example.com")

    def call_accepted(self, event):
        self.ringer.stop()
        scene = scn.Scene()
        scene.add_animation("call_oncall", picture_duration=200)
        scene.add_text("On call", picture_duration=800)
        self.displaymgr.set_scene(scene)

    def call_declined(self, event):
        scene = scn.Scene()
        scene.add_text("Call declined",picture_duration=2000)
        self.displaymgr.show_scene(scene)
        self.displaymgr.set_home_screen()
        self.ringer.stop()

    def allow_dialing(self, allow):
        print("dialing allowed: "+str(allow))
        self.dialing_allowed = allow
        if allow:
            # play dial tone
            pass
        else:
            # stop dial tone
            pass

    def incoming_call(self, event):
        # Solved: ringing is blocked by something. Audio stuttering -- edit: I think this is caused by the thread calling this method. It's actually called via a callback
        print("Starting ringing!")
        scene = scn.Scene()
        scene.add_animation("call_incoming", picture_duration=200)
        scene.add_animation("call_incoming", picture_duration=200)
        scene.add_text(event.info.remoteContact + "(" + event.info.remoteUri + ")", picture_duration=1500)
        scene.add_text("Pick up or decline with PTT-button", picture_duration = 1000)
        self.displaymgr.set_scene(scene)
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
