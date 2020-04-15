import os
from PIL import Image, ImageDraw, ImageFont

SCENE_IMAGE = 0
SCENE_TEXT = 1


class Scene:
    def __init__(self):
        self.pictures = []

    def add_text(self, text, picture_duration = 500, chars_per_line=20):
        # this line fits, just draw it
        finished = False
        while not finished:
            pict = Picture(picture_duration)
            finished = pict.createFromText(text)
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
    def __init__(self, duration, font_name="VCR_OSD_MONO_1.001.ttf", font_size=15, pwidth=128, pheight=32):
        font_name = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), font_name)
        self.image = None
        self.duration = duration
        self.font = ImageFont.truetype(font_name, font_size)
        self.pwidth = pwidth
        self.pheight = pheight

    def create_empty(self):
        self.image = Image.new('1', (self.pwidth, self.pheight))

    def createFromText(self, line):
        # todo: text does not look nice. Overflow both left and right.
        x_margin = 5

        self.image = Image.new('1', (self.pwidth, self.pheight))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(self.image)
        tw, th = draw.textsize(line, font=self.font)
        font_y_pos = self.pheight/2 - th/2
        draw.text((x_margin, font_y_pos), line, fill=255, font=self.font)
        self.image = self.image.rotate(180)
        return tw + x_margin > self.pwidth

    def createFromImage(self, uri):
        imgdir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        imgdir = imgdir + "/img/"
        folder = os.path.dirname(__file__)
        self.image = Image.open(uri).convert('1')
        self.image = self.image.rotate(180)