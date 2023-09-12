from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import json
import os
import requests
import threading
import shutil

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
    color: white;
    font-size: 14px;
    text-align: center
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
main_window.setWindowTitle("GAMERS Modloader")
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

play_button = QPushButton("Скачать и установить!")
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

# Различные переменные

loaded_config = {}
versions = {}
choosed_version = ""
download_path = "./Downloaded/"
canStartInstall = True
need_delition = {
    "files": ["/options.txt"],
    "dirs": ["/mods/", "/versions/", "/config/", "/bin/", "/libraries/", "/logs/", "/crash-reports/", "/assets/", "/defaultconfigs/", "/webcache2/", "/server-resource-packs/"]
}
url = "https://docs.google.com/uc?export=download&confirm=t&id="


# ====================================================

# Создание конфига и сохранение пути

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
    if not canStartInstall:
        return
    minecraft_directory = QFileDialog.getExistingDirectory()
    if minecraft_directory != "":
        with open("config.json", "w", encoding="UTF-8") as file:
            loaded_config["minecraft_path"] = minecraft_directory
            json.dump(loaded_config, file, sort_keys=True,
                      ensure_ascii=False, indent=4)
        input_choosed_dir.setText(loaded_config["minecraft_path"])


btn_choose_dir.clicked.connect(chooseMinecraftDirectory)

# ====================================================

# Выбор версии в списке программы

# Получение списка версий


def getVersionsList():
    global versions
    # Файл с существующими версиями (ID с гугл диска)
    versions_response = requests.get(url + "1OAhKgzM_OurZTjNhbTMp8_LWZLJOsAjN")
    versions = versions_response.json()

    for version in versions:
        versions_list.addItem(version)


def chooseVersionFromList():
    global choosed_version
    choosed_version = versions_list.currentItem().text()
    choosed_version_data = versions[choosed_version]["data"]

    version_name_text, version_name_color = choosed_version_data[
        "name_text"], choosed_version_data["name_color"]
    version_undername_text, version_undername_color = choosed_version_data[
        "undername_text"], choosed_version_data["undername_color"]
    version_desc_text, version_desc_color = choosed_version_data[
        "description_text"], choosed_version_data["description_color"]
    version_version = versions[choosed_version]["version"]

    versions_description.setText(
        f"""<h1 style='text-align: center; color: {version_name_color}'>{version_name_text}</h1>
        <h3 style='text-align: center; color: {version_undername_color}'>{version_undername_text}</h3>
        <p style='color: {version_desc_color}'>{version_desc_text}</p>
        <p style='color: lightgray'>Версия: {version_version}</p>
        """)


versions_list.currentRowChanged.connect(chooseVersionFromList)

# ====================================================

# Скачивание версии


if not os.path.exists(download_path):
    os.mkdir("Downloaded")


def getPercentage(now, need):
    return 100 * int(now) // int(need)


def fileDownload(url, file_destination, bar=None):
    file_res = requests.get(url, stream=True, timeout=5)
    file_size = file_res.headers.get("content-length")
    file_downloaded = 0
    bar.setFormat("Подготовка к скачиванию...")
    if os.path.exists(file_destination):
        os.remove(file_destination)
    download_progressbar.setFormat("Скачивание...")
    with open(file_destination, "wb") as file:
        chunks = file_res.iter_content(chunk_size=1024)
        for chunk in chunks:
            file_downloaded += 1024
            file.write(chunk)
            if bar != None:
                bar.setValue(getPercentage(file_downloaded, file_size))


def downloadVersion():
    global canStartInstall
    if loaded_config["minecraft_path"] == "":
        return
    if choosed_version == "":
        return
    if not canStartInstall:
        return

    canStartInstall = False
    btn_choose_dir.setDisabled(True)
    play_button.setDisabled(True)
    versions_list.setDisabled(True)

    version_zip_destination = os.path.join(
        download_path, choosed_version + ".zip")
    version_destination = os.path.join(download_path, choosed_version)

    fileDownload(url + versions[choosed_version]["id"],
                 version_zip_destination, download_progressbar)

    download_progressbar.setFormat("Удаляю старую версию сборки...")

    if os.path.exists(download_path + choosed_version):
        shutil.rmtree(download_path + choosed_version)

    download_progressbar.setFormat("Распаковка новой версии...")

    shutil.unpack_archive(version_zip_destination, version_destination, "zip")

    os.remove(version_zip_destination)

    download_progressbar.setFormat("Очищаю папку майнкрафта...")

    for file in need_delition["files"]:
        file_now = loaded_config["minecraft_path"] + file
        if os.path.exists(file_now):
            os.remove(file_now)

    for dir in need_delition["dirs"]:
        dir_now = loaded_config["minecraft_path"] + dir
        if os.path.exists(dir_now):
            shutil.rmtree(dir_now)

    download_progressbar.setFormat("Установка...")

    shutil.copytree(version_destination,
                    loaded_config["minecraft_path"], dirs_exist_ok=True)

    download_progressbar.setFormat("")
    download_progressbar.setValue(0)

    btn_choose_dir.setDisabled(False)
    play_button.setDisabled(False)
    versions_list.setDisabled(False)
    canStartInstall = True


play_button.clicked.connect(lambda: threading.Thread(
    target=downloadVersion, daemon=True).start())

# ====================================================

# Загрузить версии вместе с загрузкой программы без пролагов
threading.Thread(target=getVersionsList, daemon=True).start()

main_window.setLayout(window_layout)
main_window.show()

application.setStyleSheet(stylesheet)
application.exec_()

# ====================================================
