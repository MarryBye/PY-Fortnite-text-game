from json import load
from file_paths import FILE_PATHS

import requests

url = "https://docs.google.com/uc?export=download&confirm=t&id="

MODLOADER_VERSION = "1.0.2"
MODLOADER_CLOUD_INFO = requests.get(
    url + "1LGwMRz4-uEKSNTE8EOuKgCXVe2ilTBRN").json()

choosed_version = ""
download_path = "./Downloaded/"
canStartInstall = True
need_delition = {
    "files": ["/options.txt"],
    "dirs": ["/mods/", "/versions/", "/config/", "/bin/", "/libraries/", "/logs/", "/crash-reports/", "/assets/", "/defaultconfigs/", "/webcache2/", "/server-resource-packs/"]
}
