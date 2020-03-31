import RPi.GPIO as GPIO
import threading

class Dial:

    def __init__(self, dial_active_pin, pulse_pin, hook_pin):
        self.dialing = False
        self.DIAL_ACTIVE_PIN = dial_active_pin
        self.PULSE_PIN = pulse_pin
        self.HOOK_PIN = hook_pin
        self.subscribers = dict()
        self.phone_number = None
        self.currentcount = 0
        self.dialing_timer = threading.Timer(5, self.dialing_complete)

        GPIO.setup(self.HOOK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.DIAL_ACTIVE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.HOOK_PIN, GPIO.RISING, callback=self.hook_event, bouncetime=100)
        GPIO.add_event_detect(self.DIAL_ACTIVE_PIN, GPIO.BOTH, callback=self.rotation_event)
        GPIO.add_event_detect(self.PULSE_PIN, GPIO.RISING, callback=self.count_pulse, bouncetime=80)

        self.onhook = GPIO.input(self.HOOK_PIN)
        events = ['HOOKCHANGE', 'NUMBERCHANGED', 'DIALINGCOMPLETE']
        self.events = {event: dict()
                       for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback=None):
        if callback is None:
            callback = getattr(who, 'update')
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)

    def hook_event(self):
        if GPIO.input(self.HOOK_PIN):
            self.onhook = True
            # reset dialing and end any calls
            self.dialing_timer.cancel()
            self.currentcount = 0
            self.phone_number = None
        else:
            self.onhook = False
        self.dispatch(self.events['HOOKCHANGE'], self.onhook)

    def dialing_complete(self):
        self.dispatch(self.events['DIALINGCOMPLETE'], self.phone_number)

    def rotation_event(self):
        if GPIO.input(self.DIAL_ACTIVE_PIN):
            self.dialing = False
            # dialing ended. Check if a number was dialed
            if self.currentcount is not 0:
                self.add_digit(self.currentcount)
                self.currentcount = 0
        else:
            self.dialing = True
            self.dialing_timer.cancel()

    def count_pulse(self):
        if not self.onhook and self.dialing:
            self.currentcount += 1

    def add_digit(self, digit):
        # convert 10 to 0
        if digit is 10:
            digit = 0
        self.dialing_timer.start()
        self.phone_number += str(digit)
        self.dispatch(self.events['NUMBERCHANGED'], digit)
