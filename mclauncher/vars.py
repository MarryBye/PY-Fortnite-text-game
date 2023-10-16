from json import load
from file_paths import FILE_PATHS

import requests

url = "https://docs.google.com/uc?export=download&confirm=t&id="

MODLOADER_VERSION = "1.0.3"
MODLOADER_CLOUD_INFO = requests.get(
    url + "1y404KwKV1Pz9vvzwz5LWEz-SnRxGjkIa").json()

choosed_version = ""
download_path = "./Downloaded/"
canStartInstall = True
need_delition = {
    "files": ["/options.txt"],
    "dirs": ["/mods/", "/versions/", "/config/", "/bin/", "/libraries/", "/logs/", "/crash-reports/", "/assets/", "/defaultconfigs/", "/webcache2/", "/server-resource-packs/"]
}
