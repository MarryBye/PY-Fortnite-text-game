from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QSound

from ui import *
from vars import *
from json import dump

import requests
import os
import shutil
import threading


def showMessage(name, txt):
    msgBox = QMessageBox()
    msgBox.gmrs_ico = QPixmap(FILE_PATHS["ICON"])
    msgBox.gmrs_ico = msgBox.gmrs_ico.scaled(50, 50)
    msgBox.setIconPixmap(msgBox.gmrs_ico)
    msgBox.setWindowIcon(QIcon(FILE_PATHS["ICON"]))
    msgBox.setText(txt)
    msgBox.setWindowTitle(name)

    mediaplayer.setMedia(QMediaContent(
        QUrl(FILE_PATHS['COMPLETE_SOUND'])))
    mediaplayer.play()

    msgBox.exec()


def loadConfigFile():
    cfg = None

    if "config.json" not in os.listdir("./"):
        cfg = {"minecraft_path": ""}
        config_file = open("config.json", "w", encoding="utf-8")
        dump(cfg, config_file, sort_keys=True,
             ensure_ascii=False, indent=4)
    else:
        config_file = open("config.json", "r", encoding="utf-8")
        cfg = load(config_file)

    return cfg


def chooseMinecraftDirectory():
    if not canStartInstall:
        return

    cfg = loadConfigFile()

    minecraft_directory = QFileDialog.getExistingDirectory()

    if minecraft_directory != "":
        cfg["minecraft_path"] = minecraft_directory
        config_file = open("config.json", "w", encoding="utf-8")
        dump(cfg, config_file, sort_keys=True,
             ensure_ascii=False, indent=4)
        input_choosed_dir.setText(cfg["minecraft_path"])


def getVersionsList():
    for version in MODLOADER_CLOUD_INFO["versions"]:
        versions_list.addItem(version)


def chooseVersionFromList():
    global choosed_version
    choosed_version = versions_list.currentItem().text()
    choosed_version_data = MODLOADER_CLOUD_INFO["versions"][choosed_version]["data"]

    version_name_text, version_name_color = choosed_version_data[
        "name_text"], choosed_version_data["name_color"]
    version_undername_text, version_undername_color = choosed_version_data[
        "undername_text"], choosed_version_data["undername_color"]
    version_desc_text, version_desc_color = choosed_version_data[
        "description_text"], choosed_version_data["description_color"]
    version_version = MODLOADER_CLOUD_INFO["versions"][choosed_version]["version"]

    versions_description.setText(
        f"""<h1 style='text-align: center; color: {version_name_color}'>{version_name_text}</h1>
        <h3 style='text-align: center; color: {version_undername_color}'>{version_undername_text}</h3>
        <p style='color: {version_desc_color}'>{version_desc_text}</p>
        <p style='color: lightgray'>Версия: {version_version}</p>
        """)


def getDonatersList():
    global donaters

    for donater in sorted(MODLOADER_CLOUD_INFO["donaters"], key=lambda x: MODLOADER_CLOUD_INFO["donaters"][x], reverse=True):
        donaters_list.addItem(donater)

    for i in range(donaters_list.count()):
        donaters_avatar_response = requests.get(
            f"https://mc-heads.net/avatar/{donaters_list.item(i).text()}").content
        donater_avatar = QPixmap()
        donater_avatar.loadFromData(donaters_avatar_response)
        donaters_list.item(i).setIcon(QIcon(donater_avatar))


def loadLists():
    getVersionsList()
    getDonatersList()


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


def downloadProcess():
    global canStartInstall, t
    if loadConfigFile()["minecraft_path"] == "":
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

    fileDownload(url + MODLOADER_CLOUD_INFO["versions"][choosed_version]["id"],
                 version_zip_destination, download_progressbar)

    download_progressbar.setFormat("Удаляю старую версию сборки...")

    if os.path.exists(download_path + choosed_version):
        shutil.rmtree(download_path + choosed_version)

    download_progressbar.setFormat("Распаковка новой версии...")

    shutil.unpack_archive(version_zip_destination,
                          version_destination, "zip")

    os.remove(version_zip_destination)

    download_progressbar.setFormat("Очищаю папку майнкрафта...")

    for file in need_delition["files"]:
        file_now = loadConfigFile()["minecraft_path"] + file
        if os.path.exists(file_now):
            os.remove(file_now)

    for dir in need_delition["dirs"]:
        dir_now = loadConfigFile()["minecraft_path"] + dir
        if os.path.exists(dir_now):
            shutil.rmtree(dir_now)

    download_progressbar.setFormat("Установка...")

    shutil.copytree(version_destination,
                    loadConfigFile()["minecraft_path"], dirs_exist_ok=True)

    download_progressbar.setFormat("")
    download_progressbar.setValue(0)

    btn_choose_dir.setDisabled(False)
    play_button.setDisabled(False)
    versions_list.setDisabled(False)
    canStartInstall = True

    mediaplayer.setMedia(QMediaContent(
        QUrl(FILE_PATHS["COMPLETE_SOUND"])))
    mediaplayer.play()


def startModLoader():
    if not os.path.exists(download_path):
        os.mkdir("Downloaded")

    input_choosed_dir.setText(loadConfigFile()["minecraft_path"])

    btn_choose_dir.clicked.connect(chooseMinecraftDirectory)

    versions_list.currentRowChanged.connect(chooseVersionFromList)

    play_button.clicked.connect(lambda: threading.Thread(
        target=downloadProcess, daemon=True).start())

    threading.Thread(target=loadLists, daemon=True).start()
    threading.Thread(target=main_window.show(), daemon=True).start()

    application.exec_()
