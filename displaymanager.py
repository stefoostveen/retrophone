import scene as scn
import os
import time

class DisplayManager:
    def __init__(self):
        self.prev_screen = None
        self.current_screen = None

    def set(self, scene):
        for picture in scene:
            if scene.type == scrn.SCENE_IMAGE:
                folder = os.path.dirname(__file__)
                image = Image.open(scene.path).convert('1')
                self.disp.image(image)
                self.disp.display()
            elif scene.type == scrn.SCENE_TEXT:
                pass

    def _display_loop(self, scene):
        for picture in scene.pictures:
            self.disp.image(picture.image)
            self.disp.display()
            time.sleep(picture.duration/1000)


    def show(self, screen):
        self.prev_screen = self.current_screen

        pass

    def show_home_screen(self):
        pass