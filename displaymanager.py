import scene as scn
import os
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

class DisplayManager:
    def __init__(self,RST,DC,SPI_PORT,SPI_DEVICE):
        self.current_scene = None
        self.backdrop_scene = None
        self.scene_queue = []

        # 128x32 display with hardware SPI:
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

        # Initialize library.
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

    def set_scene(self, scene):
        self.backdrop_scene = scene

    def _service(self):
        if self.scene_queue:
            scene = self.scene_queue.pop()
            self._display_scene(scene)
        else:
            self._display_scene(self.backdrop_scene)

    def _display_scene(self, scene):
        self.current_scene = scene
        for picture in scene.pictures:
            self.disp.image(picture.image)
            self.disp.display()
            time.sleep(picture.duration/1000)


    def show_scene(self, scene):
        self.scene_queue.append(scene)

    def set_home_screen(self):
        scene = scn.EmptyScene()