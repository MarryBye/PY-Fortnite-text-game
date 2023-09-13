import json
import os

FILES_TUPLE = ("members_info.json", "voice_channels.json", "guild_settings.json", "messages.json")


class GuildFS:
    def __init__(self, g_id: int):

        self.file = None
        self.file_path = None
        self.g_id = g_id
        self.guild_folder = os.path.join("data", str(g_id))

    @staticmethod
    def format_json(fs) -> dict:
        formatted_json = {}
        for k, v in fs.items():
            if k.isdigit():
                formatted_json[int(k)] = v
            else:
                formatted_json[k] = v
        return formatted_json

    def load_guild_file(self, f_type: int) -> dict:

        try:
            self.file_path = os.path.join(self.guild_folder, FILES_TUPLE[f_type])

            self.file = open(self.file_path, "r", encoding="UTF-8")

            return json.load(self.file, object_hook=self.format_json)
        except FileNotFoundError:
            print(f"Невозможно загрузить файлы сервера {self.g_id}! У этого сервера нет файлов.")

    async def save_guild_file(self, value=None) -> None:

        if value is None:
            value = {}

        self.file = open(self.file_path, "w", encoding="UTF-8")

        json.dump(value, self.file)

    async def create_guild_files(self) -> None:

        try:
            os.mkdir(self.guild_folder)

            for file in FILES_TUPLE:
                new_guild_file = open(os.path.join(self.guild_folder, file), "w", encoding="utf-8")
                json.dump({}, new_guild_file, ensure_ascii=False, indent=4)
                new_guild_file.close()
        except FileExistsError:
            print(f"Невозможно создать файлы для сервера {self.g_id}! Файлы уже существуют.")
        except FileNotFoundError:
            print(f"Невозможно создать файлы для сервера {self.g_id}! Возможно повреждена папка data.")
