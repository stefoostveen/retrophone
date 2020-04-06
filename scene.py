import os

SCENE_IMAGE = 0
SCENE_TEXT = 1


class Scene:
    def __init__(self):
        self.pictures = []

    def add_text(self, text, picture_duration = 500):



    def add_animation(self, img_folder, picture_duration=500):
        img_folder = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "/img/" + img_folder)
        for imgf in sorted(os.listdir(img_folder)):
            if imgf.endswith(".ppm"):
                path = os.path.join(img_folder, imgf)
                pict = Picture(picture_duration)
                pict.createFromImage(path)
                self.pictures.append(pict)

class FaultScene(Scene):
    def __init__(self, title, text):
        Scene.__init__(self)
        pass

class SuccessScene(Scene):
    def __init__(self, title, text):
        Scene.__init__(self)
        pass

class ImgScene(Scene):
    def __init__(self, img_folder, picture_duration=500):
        Scene.__init__(self)

        img_folder = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "/img/" + img_folder)
        for imgf in sorted(os.listdir(img_folder)):
            if imgf.endswith(".ppm"):
                path = os.path.join(img_folder, imgf)
                pict = Picture(picture_duration)
                pict.createFromImage(path)
                self.pictures.append(pict)


class Picture:
    def __init__(self, duration):
        self.image = None
        self.duration = duration

    def createFromText(self):
        pass

    def createFromImage(self, uri):
        imgdir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        imgdir = imgdir + "/img/"
        folder = os.path.dirname(__file__)
        phoneimage = os.path.join(folder, "img/telephone.ppm")
        image = Image.open(phoneimage).convert('1')