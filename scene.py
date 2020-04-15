import os
from PIL import Image, ImageDraw, ImageFont

SCENE_IMAGE = 0
SCENE_TEXT = 1


class Scene:
    def __init__(self):
        self.pictures = []

    def add_text(self, text, picture_duration = 500, chars_per_line=20):
        # this line fits, just draw it
        pict = Picture(picture_duration)
        pict.createFromText(text)
        self.pictures.append(pict)

    def add_animation(self, img_folder, picture_duration=500):
        img_folder = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "img/" + img_folder)
        for imgf in sorted(os.listdir(img_folder)):
            if imgf.endswith(".ppm"):
                path = os.path.join(img_folder, imgf)
                pict = Picture(picture_duration)
                pict.createFromImage(path)
                self.pictures.append(pict)


class FaultScene(Scene):
    def __init__(self, text):
        Scene.__init__(self)
        self.add_animation("fault", picture_duration=1000)
        self.add_text(text, picture_duration=5000)


class SuccessScene(Scene):
    def __init__(self, text):
        Scene.__init__(self)
        self.add_animation("success", picture_duration=1000)
        self.add_text(text, picture_duration=3000)

class EmptyScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        pict = Picture(1000)
        pict.create_empty()
        self.pictures.append(pict)

class Picture:
    def __init__(self, duration):
        self.image = None
        self.duration = duration

    def create_empty(self):
        self.image = Image.new('1', (128, 32))

    def createFromText(self, line):
        # todo: text does not look nice. Overflow both left and right.
        line_y = 5
        self.image = Image.new('1', (128, 32))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(self.image)
        tw, th = draw.textsize(line)
        draw.text(((128 - tw) / 2, line_y), line, fill=255)
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def createFromImage(self, uri):
        imgdir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        imgdir = imgdir + "/img/"
        folder = os.path.dirname(__file__)
        self.image = Image.open(uri).convert('1')
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)