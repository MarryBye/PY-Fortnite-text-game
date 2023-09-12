from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QGroupBox, QPushButton, QLineEdit, QTextEdit, QListWidget, QProgressBar, QMessageBox, QFileDialog)
from PyQt5.QtGui import (QFontDatabase, QPixmap, QIcon)
from PyQt5.QtMultimedia import QMediaPlayer

from vars import FILE_PATHS, MODLOADER_VERSION

application = QApplication([])
mediaplayer = QMediaPlayer()

QFontDatabase.addApplicationFont(FILE_PATHS["FONT_MINECRAFT"])
application.setStyleSheet(open(FILE_PATHS["MAIN_STYLE"]).read())

main_window = QWidget()
main_window.setWindowTitle("GAMERS Modloader " + MODLOADER_VERSION)
main_window.setWindowIcon(QIcon(FILE_PATHS["ICON"]))
main_window.resize(640, 480)

window_layout = QVBoxLayout()

# Верхняя часть

header_group = QGroupBox()

header_layout = QHBoxLayout()

btn_choose_dir = QPushButton("Выбрать папку...")
input_choosed_dir = QLineEdit()
input_choosed_dir.setPlaceholderText("Папка с установленным майнкрафтом...")
input_choosed_dir.setReadOnly(True)

header_layout.addWidget(btn_choose_dir)
header_layout.addWidget(input_choosed_dir)

header_group.setLayout(header_layout)

# ====================================================

# Основная программа

main_layout = QHBoxLayout()

# Список версий

versions_group = QGroupBox()
versions_layout = QVBoxLayout()

versions_list = QListWidget()

versions_layout.addWidget(versions_list, 50)

versions_group.setLayout(versions_layout)

# Донатеры

donaters_group = QGroupBox()
donaters_layout = QVBoxLayout()

donaters_list = QListWidget()
donaters_list.setObjectName("donat")

donaters_layout.addWidget(donaters_list, 50)

donaters_group.setLayout(donaters_layout)

main_left_layout = QVBoxLayout()
main_left_layout.addWidget(versions_group, stretch=65)
main_left_layout.addWidget(donaters_group, stretch=35)

# Правая часть

main_right_group = QGroupBox()
main_right_layout = QVBoxLayout()

versions_description = QTextEdit()
versions_description.setReadOnly(True)
versions_description.acceptRichText()

main_right_layout.addWidget(versions_description)
main_right_group.setLayout(main_right_layout)

main_layout.addLayout(main_left_layout, stretch=25)
main_layout.addWidget(main_right_group, stretch=75)

# ====================================================

# Нижняя часть

footer_group = QGroupBox()

footer_layout = QHBoxLayout()

play_button = QPushButton("Скачать и установить")
download_progressbar = QProgressBar()
download_progressbar.setRange(0, 100)

footer_layout.addWidget(play_button, stretch=25)
footer_layout.addWidget(download_progressbar, stretch=75)

footer_group.setLayout(footer_layout)

# ====================================================

window_layout.addWidget(header_group)
window_layout.addLayout(main_layout)
window_layout.addWidget(footer_group)

# ====================================================

# Реакции элементов

main_window.setLayout(window_layout)
