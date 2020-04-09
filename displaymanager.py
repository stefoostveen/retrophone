import scene as scn
import os
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import threading
import logging

class DisplayManager:
    def __init__(self,RST):
        self.current_scene = None
        self.backdrop_scene = None
        self.scene_queue = []
        self.stop = False

        # 128x32 display with hardware SPI:
        try:
            self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

            # Initialize library.
            self.disp.begin()
            self.disp.clear()
            self.disp.display()

            threading.Thread(target=self._service, daemon=True).start()
        except Exception as e:
            logging.warning("Could not instantiate display")


    def set_scene(self, scene):
        self.backdrop_scene = scene

    def _service(self):
        while not self.stop:
            if self.scene_queue:
                scene = self.scene_queue.pop()
                self._display_scene(scene)
            elif self.backdrop_scene:
                self._display_scene(self.backdrop_scene)
            else:
                time.sleep(0.5)

    def _display_scene(self, scene):
        self.current_scene = scene
        for picture in scene.pictures:
            self.disp.image(picture.image)
            self.disp.display()
            time.sleep(picture.duration/1000)

    def show_scene(self, scene):
        self.scene_queue.append(scene)

    def set_home_screen(self):
        self.backdrop_scene = scn.EmptyScene()
