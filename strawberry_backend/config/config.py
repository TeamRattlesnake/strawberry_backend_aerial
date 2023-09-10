"""
Модуль с настройками проекта
"""

import json
from enum import Enum
from os import listdir

BASIC_DIRECTORY = "data/configs"
CONTEXTS_CONFIG = "contexts.json"
DATABASE_CONFIG = "database.json"
DOCS_CONFIG = "docs.json"
SERVER_CONFIG = "server.json"


class Config:
    def __init__(self, path=BASIC_DIRECTORY):
        # Загрузка конфига контекстов
        with open(f"{path}/{CONTEXTS_CONFIG}", "r", encoding="UTF-8") as file:
            self.contexts_data = json.load(file)

        self.contexts_create_directory = self.contexts_data["create_directory"]
        self.contexts_edit_directory = self.contexts_data["edit_directory"]
        self.contexts_correct_directory = self.contexts_data["correct_directory"]

        self.contexts_create = [
            context_name.replace(".txt", "")
            for context_name in listdir(self.contexts_create_directory)
        ]
        self.contexts_edit = [
            context_name.replace(".txt", "")
            for context_name in listdir(self.contexts_edit_directory)
        ]
        self.contexts_correct = [
            context_name.replace(".txt", "")
            for context_name in listdir(self.contexts_correct_directory)
        ]

        self.contexts_schema = {
            "create": self.contexts_create,
            "edit": self.contexts_edit,
            "correct": self.contexts_correct,
        }

        self.contexts_names = (
            self.contexts_create + self.contexts_edit + self.contexts_correct
        )

        self.generate_methods = Enum("GenerateMethod", self.contexts_names)

        self.contexts_create_filepath = [
            f"{self.contexts_create_directory}/{filename}"
            for filename in listdir(self.contexts_create_directory)
        ]
        self.contexts_edit_filepath = [
            f"{self.contexts_edit_directory}/{filename}"
            for filename in listdir(self.contexts_edit_directory)
        ]
        self.contexts_correct_filepath = [
            f"{self.contexts_correct_directory}/{filename}"
            for filename in listdir(self.contexts_correct_directory)
        ]

        # Загрузка конфига базы данных
        with open(
            f"{BASIC_DIRECTORY}/{DATABASE_CONFIG}", "r", encoding="UTF-8"
        ) as file:
            self.database_data = json.load(file)

        # Загрузка документации и описаний
        with open(f"{BASIC_DIRECTORY}/{DOCS_CONFIG}", "r", encoding="UTF-8") as file:
            self.docs_data = json.load(file)
        self.docs_title = self.docs_data["title"]
        self.docs_version = self.docs_data["version"]
        self.docs_description = self.docs_data["description"]
        self.docs_contact = self.docs_data["contact"]

        # Загрузка конфига сервера
        with open(f"{BASIC_DIRECTORY}/{SERVER_CONFIG}", "r", encoding="UTF-8") as file:
            self.server_data = json.load(file)
        self.server_origins = self.server_data["origins"]
        self.server_client_secret = self.server_data["client_secret"]


config = Config()
