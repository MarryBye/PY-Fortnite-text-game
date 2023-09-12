import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


FILE_PATHS = {
    "ICON": resource_path("assets/images/icon.ico"),
    "COMPLETE_SOUND": "assets/sounds/ding.mp3",
    "FONT_MINECRAFT": resource_path("assets/fonts/minecraft.ttf"),
    "MAIN_STYLE": resource_path("assets/style/style.qss")
}
