import scene as scn
import os
import time

class DisplayManager:
    def __init__(self):
        self.current_scene = None
        self.backdrop_scene = None
        self.scene_queue = []

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