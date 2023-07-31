from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import json
import os
import wget
import shutil
import time

stylesheet = """
* {
    border-radius: 8px;
}
QWidget {
    background-color: rgb(25, 25, 25);
    color: rgb(180, 180, 180);
    font-family: Arial;
}
QPushButton { 
    padding: 4px 4px 4px 4px;
    background-color: gray;
    border-style: solid;
    border-width: 2px;
    border-color: gray;
    color: black;
}
QPushButton:hover {
    background-color: lightgray;
    border-color: white;
    color: black;
}
QGroupBox {
    border-style: solid;
    border-width: 3px;
    border-color: gray;
}
QGroupBox::title {
    subcontrol-origin: padding;
    subcontrol-position: top center;
    font-size: 14px;
}
QListWidget {
    border: none;
    show-decoration-selected: 0;
    outline: 0;
}
QListWidget::item {
    border: none;
    margin-top: 4px;
    text-align: center;
    padding: 4px 4px 4px 4px;
    border-radius: 8px;
    color: lightgray;
}
QListWidget::item:hover {
    border-width: 2px;
    border-color: gray;
    border-style: solid;
    color: lightgray;
}
QListWidget::item:selected {
    border-width: 2px;
    border-color: gray;
    border-style: solid;
    background-color: rgba(25, 55, 125, 0.25);
    color: lightgray;
}
QTextEdit {
    border: none;
}
QProgressBar {
    border-width: 2px;
    border-color: gray;
    border-style: solid;
    color: rgba(0, 0, 0, 0)
}
QProgressBar::chunk {
    background-color: gray;
    width: 5px;
    margin-left: 1px;
    margin-right: 1px;
}
QLineEdit {
    border-width: 2px;
    border-color: gray;
    border-style: solid;
    padding: 4px 4px 4px 4px;
}
"""

application = QApplication([])

main_window = QWidget()
main_window.setWindowTitle("GAMERS Launcher")
main_window.setWindowIcon(QIcon('icon.ico'))
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

# Левая часть

main_left_group = QGroupBox()
main_left_layout = QVBoxLayout()

versions_list = QListWidget()

main_left_layout.addWidget(versions_list)

main_left_group.setLayout(main_left_layout)

# Правая часть

main_right_group = QGroupBox()
main_right_layout = QVBoxLayout()

versions_description = QTextEdit()
versions_description.setReadOnly(True)
versions_description.acceptRichText()

main_right_layout.addWidget(versions_description)
main_right_group.setLayout(main_right_layout)

main_layout.addWidget(main_left_group, stretch=25)
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

# Создание конфига и сохранение пути

loaded_config = {}

if "config.json" not in os.listdir("./"):
    with open("config.json", "w", encoding="UTF-8") as file:
        loaded_config = {
            "minecraft_path": ""
        }
        json.dump(loaded_config, file, sort_keys=True,
                  ensure_ascii=False, indent=4)
else:
    with open("config.json", "r", encoding="UTF-8") as file:
        loaded_config = json.load(file)

input_choosed_dir.setText(loaded_config["minecraft_path"])


def chooseMinecraftDirectory():
    global loaded_config
    minecraft_directory = QFileDialog.getExistingDirectory()
    with open("config.json", "w", encoding="UTF-8") as file:
        loaded_config["minecraft_path"] = minecraft_directory
        json.dump(loaded_config, file, sort_keys=True,
                  ensure_ascii=False, indent=4)
    input_choosed_dir.setText(loaded_config["minecraft_path"])


btn_choose_dir.clicked.connect(chooseMinecraftDirectory)

# Получение списка версий

url = "https://docs.google.com/uc?export=download&confirm=t&id="
id = "1OAhKgzM_OurZTjNhbTMp8_LWZLJOsAjN"

versions_filename = "versions.json"

if os.path.exists(versions_filename):
    os.remove(versions_filename)
versions_file = wget.download(url + id, out=versions_filename)


with open(versions_filename, "r", encoding="UTF-8") as file:
    versions = json.load(file)
    for version in versions:
        versions_list.addItem(version)

choosed_version = ""


def chooseVersionFromList():
    global choosed_version
    choosed_version = versions_list.currentItem().text()
    versions_description.setText(
        f"{versions[choosed_version]['description']}\n<p>Версия: {versions[choosed_version]['version']}</p>")


versions_list.currentRowChanged.connect(chooseVersionFromList)

# Скачивание версии

download_path = ".\\Downloaded\\"

if not os.path.exists("./Downloaded/"):
    os.mkdir("Downloaded")

need_delition = {
    "files": ["/options.txt"],
    "dirs": ["/mods/", "/versions/", "/config/", "/bin/", "/libraries/", "/logs/", "/crash-reports/", "/assets/", "/defaultconfigs/", "/webcache2/", "/server-resource-packs/"]
}

canStartInstall = True


def downloadVersion():
    global canStartInstall
    if loaded_config["minecraft_path"] == "":
        return
    if choosed_version == "":
        return
    if not canStartInstall:
        return

    canStartInstall = False
    download_progressbar.setValue(5)

    if os.path.exists(download_path + choosed_version + ".zip"):
        os.remove(download_path + choosed_version + ".zip")
    version_downloaded = wget.download(url+versions[choosed_version]
                                       ["id"], out=download_path + choosed_version + ".zip")

    download_progressbar.setValue(50)

    if os.path.exists(download_path + choosed_version):
        shutil.rmtree(download_path + choosed_version)

    download_progressbar.setValue(75)

    shutil.unpack_archive(version_downloaded,
                          download_path + choosed_version, "zip")

    download_progressbar.setValue(90)

    os.remove(version_downloaded)

    download_progressbar.setValue(100)

    time.sleep(1)
    download_progressbar.setValue(0)
    time.sleep(1)
    download_progressbar.setValue(5)

    for file in need_delition["files"]:
        file_now = loaded_config["minecraft_path"] + file
        if os.path.exists(file_now):
            os.remove(file_now)

    download_progressbar.setValue(30)

    for dir in need_delition["dirs"]:
        dir_now = loaded_config["minecraft_path"] + dir
        if os.path.exists(dir_now):
            shutil.rmtree(dir_now)

    download_progressbar.setValue(70)

    shutil.copytree(download_path + choosed_version,
                    loaded_config["minecraft_path"], dirs_exist_ok=True)

    download_progressbar.setValue(100)
    time.sleep(1)
    download_progressbar.setValue(0)
    canStartInstall = True


play_button.clicked.connect(downloadVersion)

main_window.setLayout(window_layout)
main_window.show()
application.setStyleSheet(stylesheet)
application.exec_()
