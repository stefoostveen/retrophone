import logging

import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import configparser

class Ringer:

    def __init__(self):
        #todo: ringer does not work
        fn = "audio/ring.wav"
        cnf = "conf/audiodev.ini"
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.audio = os.path.join(__location__, fn)

        self.available_devices = sd.query_devices()
        print("Available audio devices:")
        print(self.available_devices)

        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(__location__, cnf))
            dev_cnf = config['DEV']
            self.pb_device = dev_cnf.getint('PlaybackDevice', 0)
            sd.default.device = int(self.pb_device)
        except Exception as e:
            logging.warning("[RINGER] Cannot instantiate playback device")
            self.pb_device = None

    def play(self, loop=False):
        data, fs = sf.read(self.audio, dtype='float32')
        if not self.pb_device:
            sd.play(data, fs, loop=loop)
        else:
            sd.play(data, fs, device=int(self.pb_device), loop=loop)

    def ring(self):
        print("[RINGER] Started ringing")
        print("[RINGER] Pbdev="+str(self.pb_device))
        self.play(True)

    def stop(self):
        sd.stop()
