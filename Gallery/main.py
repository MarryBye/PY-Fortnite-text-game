import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

app = QApplication([])  # ? Створили додаток
win = QWidget()  # ? Створили вікно додатку
win.setWindowTitle("Image Editor")  # ? Встановили назву вікна
win.resize(800, 600)  # ? Встановили розміри вікна

# ! Створення віджетів

btn_choose_dir = QPushButton("Папка")

btn_rotate_left = QPushButton("Ліворуч")
btn_rotate_right = QPushButton("Праворуч")
btn_flip_horizontal = QPushButton("Відзеркалити")
btn_sharpness = QPushButton("Різкість")
btn_black_and_white = QPushButton("Ч/Б")

list_files = QListWidget()
label_image = QLabel("*Тут могла бути ваша реклама*")

# ! Створення лейаутів

layout_window = QHBoxLayout()  # ? Лейаут, який всіх об'єднає
layout_column1 = QVBoxLayout()  # ? Ліва колонка
layout_column2 = QVBoxLayout()  # ? Права колонка
layout_buttons = QHBoxLayout()  # ? Лейаут для кнопок під зображенням

# ! Розміщення елементів у лейаутах

layout_column1.addWidget(btn_choose_dir)
layout_column1.addWidget(list_files)

layout_column2.addWidget(label_image)

layout_buttons.addWidget(btn_rotate_left)
layout_buttons.addWidget(btn_rotate_right)
layout_buttons.addWidget(btn_flip_horizontal)
layout_buttons.addWidget(btn_sharpness)
layout_buttons.addWidget(btn_black_and_white)

layout_column2.addLayout(layout_buttons)

# ! Об'єднання усіх лейаутів в один

layout_window.addLayout(layout_column1, 20)  # ? 20% від ширини вікна
layout_window.addLayout(layout_column2, 80)  # ? 80% від ширини вікна

# ? Встановили розміщення елементів програми у вікні
win.setLayout(layout_window)

# ! Функціонал програми

working_directory = ""  # ? Місце, яке обрав користувач


def choose_working_directory():
    """Функція, щоб отримати шлях від користувача"""
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()


def filter(files, extensions):
    """Функція щоб відділити зображення від інших файлів"""
    result = list()
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                result.append(file)
                break
    return result


def get_image_files():
    """Функція, що виконується при натисненні на кнопку"""
    extensions = [".png", ".jpeg", ".jpg", ".bmp", ".svg", ".esp"]
    choose_working_directory()
    if working_directory != "":
        files = filter(os.listdir(working_directory), extensions)
        list_files.clear()
        list_files.addItems(files)


# ! Говоримо, які елементи що й коли роблять (з'єднуємо з функціями)
btn_choose_dir.clicked.connect(get_image_files)


win.show()  # ? Показали вікно
app.exec()  # ? Запустили додаток
