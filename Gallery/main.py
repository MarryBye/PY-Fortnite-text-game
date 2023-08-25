from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from PIL import Image, ImageEnhance
from PIL.ImageFilter import *

import os

# Создали пустое приложение
app = QApplication([])
main_window = QWidget()
main_window.resize(800, 500)
main_window.setWindowTitle("Gallery")

# Создаем элементы программы
label_image = QLabel("Картинка")

btn_directory = QPushButton("Папка")
btn_rotate_left = QPushButton("Влево")
btn_smooth = QPushButton("Сгладить")
btn_rotate_right = QPushButton("Вправо")
btn_flip = QPushButton("Отзеркалить")
btn_blackandwhite = QPushButton("Ч/Б")
btn_sharp = QPushButton("Резкость")
btn_contrast = QPushButton("Контраст")
btn_blur = QPushButton("Блюр")

photos_list = QListWidget()

# Интерфейс программы
main_layout = QHBoxLayout()  # Главный лейаут

left_column = QVBoxLayout()
right_column = QVBoxLayout()

left_column.addWidget(btn_directory)
left_column.addWidget(photos_list)

right_column.addWidget(label_image)

button_layout = QHBoxLayout()
button_layout.addWidget(btn_rotate_left)
button_layout.addWidget(btn_rotate_right)
button_layout.addWidget(btn_blur)
button_layout.addWidget(btn_rotate_right)
button_layout.addWidget(btn_contrast)
button_layout.addWidget(btn_sharp)
button_layout.addWidget(btn_flip)
button_layout.addWidget(btn_blackandwhite)
button_layout.addWidget(btn_smooth)

right_column.addLayout(button_layout)
main_layout.addLayout(left_column, 20)
main_layout.addLayout(right_column, 80)

main_window.setLayout(main_layout)

# Логика программы
working_directory = ""


def choose_directory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()


allowed_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]


def file_filter(files):
    result = []
    for file in files:
        for ext in allowed_extensions:
            if file.endswith(ext):
                result.append(file)
    return result


def makeFileList():
    choose_directory()
    files = file_filter(os.listdir(working_directory))
    photos_list.clear()
    for file in files:
        photos_list.addItem(file)


btn_directory.clicked.connect(makeFileList)

# Класс для работы с изображением


class ImageProcessor:
    def __init__(self):
        self.image = None  # объект изображения
        self.file = None  # название изображения
        self.save_dir = "Edited/"  # место для измененных картинок

    def loadImage(self, file):
        self.file = file
        image_path = os.path.join(working_directory, self.file)
        self.image = Image.open(image_path)  # создать изображение в PIL

    def showImage(self, path):
        label_image.hide()
        pixmapimage = QPixmap(path)  # создать изображение в PYQT
        w, h = label_image.width(), label_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        label_image.setPixmap(pixmapimage)
        label_image.show()

    def saveImage(self):
        save_path = os.path.join(working_directory, self.save_dir)
        if not (os.path.exists(save_path) or os.path.isdir(save_path)):
            os.mkdir(save_path)
        image_path = os.path.join(save_path, self.file)
        self.image.save(image_path)

    def rotate_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def rotate_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def sharpen(self):
        self.image = self.image.filter(SHARPEN)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def makebw(self):
        self.image = self.image.convert("L")

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def sharpen(self):
        self.image = self.image.filter(SHARPEN)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def contrast(self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.5)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def blur(self):
        self.image = self.image.filter(BLUR)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)

    def smooth(self):
        self.image = self.image.filter(SMOOTH)

        self.saveImage()
        image_path = os.path.join(working_directory, self.save_dir, self.file)
        self.showImage(image_path)


working_image = ImageProcessor()


def showChosenImage():
    if photos_list.currentRow() >= 0:
        image_name = photos_list.currentItem().text()
        working_image.loadImage(image_name)
        image_path = os.path.join(working_directory, working_image.file)
        working_image.showImage(image_path)


photos_list.currentRowChanged.connect(showChosenImage)
btn_flip.clicked.connect(working_image.mirror)
btn_blackandwhite.clicked.connect(working_image.makebw)
btn_rotate_left.clicked.connect(working_image.rotate_left)
btn_rotate_right.clicked.connect(working_image.rotate_right)
btn_sharp.clicked.connect(working_image.sharpen)
btn_blur.clicked.connect(working_image.blur)
btn_smooth.clicked.connect(working_image.smooth)
btn_contrast.clicked.connect(working_image.contrast)

# Запуск приложения
main_window.show()
app.exec_()
