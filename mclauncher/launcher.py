from funcs import MODLOADER_CLOUD_INFO, MODLOADER_VERSION, showMessage, startModLoader

# Проверка версии лаунчера
TODAY_MODLOADER_VERSION = MODLOADER_CLOUD_INFO["MODLOADER_VERSION"]

if TODAY_MODLOADER_VERSION != MODLOADER_VERSION:
    showMessage(
        "Обновление", f"Ваша версия GAMERS MODLOADER устарела!\nПожалуйста, скачайте обновленную версию.\n\nВаша версия: {MODLOADER_VERSION}\nСовременная: {TODAY_MODLOADER_VERSION}")
else:
    startModLoader()
