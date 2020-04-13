import logging
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    logging.warning("Could not instantiate dial")
import threading
import callmanager_events as cme
import event


class Dial:

    def __init__(self, dial_active_pin, pulse_pin, hook_pin):
        self.dialing = False
        self.DIAL_ACTIVE_PIN = dial_active_pin
        self.PULSE_PIN = pulse_pin
        self.HOOK_PIN = hook_pin
        self.phone_number = None
        self.currentcount = 0
        self.dialing_timer = threading.Timer(5, self.dialing_complete)
        self.callbacks = {
                cme.DIAL_NUMBER_UPDATED: [],
                cme.DIAL_DIALING_COMPLETE: [],
                cme.DIAL_HOOK_CHANGE: []
        }

        try:
            GPIO.setup(self.HOOK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.DIAL_ACTIVE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self.HOOK_PIN, GPIO.RISING, callback=self.hook_event, bouncetime=100)
            GPIO.add_event_detect(self.DIAL_ACTIVE_PIN, GPIO.BOTH, callback=self.rotation_event)
            GPIO.add_event_detect(self.PULSE_PIN, GPIO.RISING, callback=self.count_pulse, bouncetime=80)

            self.onhook = GPIO.input(self.HOOK_PIN)
        except Exception:
            logging.warning("Could not instantiate dial")

    def hook_event(self, channel):
        self.onhook = GPIO.input(self.HOOK_PIN)
        if self.onhook:
            # reset dialing and end any calls
            self.dialing_timer.cancel()
            self.currentcount = 0
            self.phone_number = None

        self.notify(cme.DIAL_HOOK_CHANGE, on_hook=self.onhook)

    def dialing_complete(self):
        self.notify(cme.DIAL_DIALING_COMPLETE, phone_number=self.phone_number)

    def rotation_event(self, channel):
        self.dialing = GPIO.input(self.DIAL_ACTIVE_PIN)
        if not self.dialing:
            # dialing ended. Check if a number was dialed
            if self.currentcount > 0:
                self.add_digit(self.currentcount)
                self.currentcount = 0
        else:
            self.dialing_timer.cancel()

    def count_pulse(self, channel):
        if not self.onhook and self.dialing:
            self.currentcount += 1

    def add_digit(self, digit):
        # convert 10 to 0
        if digit == 10:
            digit = 0
        self.dialing_timer = threading.Timer(5, self.dialing_complete)
        self.dialing_timer.start()
        self.phone_number += str(digit)
        self.notify(cme.DIAL_NUMBER_UPDATED, phone_number=self.phone_number, digit=digit)

    def subscribe(self, callback, event_t):
        self.callbacks[event_t].append(callback)

    def notify(self, event_t, **attrs):
        e = event.Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks[event_t]:
            fn(e)
