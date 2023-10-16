# pip install pillow

from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

# filename = "original2"
# format = ".jpg"

# with Image.open(filename + format) as pic:

#     # Вивести інформацію про зображення
#     print("Розмір зображення:", pic.size)
#     print("Формат зображення:", pic.format)
#     print("Колірний тип:", pic.mode)

#     # Зробити чорно-білим
#     pic_gray = pic.convert("L")
#     pic_gray.save("gray_" + filename + ".jpg")

#     # Зробити розмитим
#     pic_blured = pic.filter(ImageFilter.BLUR)
#     pic_blured.save("blured_" + filename + ".jpg")

#     # Перевернути на 180 градусів
#     pic_rotated = pic.transpose(Image.ROTATE_180)
#     pic_rotated.save("rotated_" + filename + ".jpg")

#     # Відзеркалити зображення
#     pic_mirror = pic.transpose(Image.FLIP_LEFT_RIGHT)
#     pic_mirror.save("mirror_" + filename + ".jpg")

#     # Контраст (БОНУС)
#     pic_contrast = ImageEnhance.Contrast(pic).enhance(2.5)
#     pic_contrast.save("contrast_" + filename + ".jpg")


class ImageEditor:
    def __init__(self):
        self.filename = None
        self.original = None
        self.photos = []

    def open(self, filepath):
        self.original = Image.open(filepath)

    def make_bw(self):
        self.original = self.original.convert("L")

    def make_blur(self):
        self.original = self.original.filter(ImageFilter.BLUR)

    def do_left(self):
        self.original = self.original.transpose(Image.ROTATE_90)

    def do_right(self):
        self.original = self.original.transpose(Image.ROTATE_270)

    def save(self, filename):
        self.photos.append(self.original)
        self.original.save(filename)


editor = ImageEditor()
editor.open("original.jpg")
editor.do_left()
editor.do_left()
editor.do_left()
editor.do_left()
editor.do_left()
editor.make_bw()
editor.make_blur()
editor.save("ex.jpg")
