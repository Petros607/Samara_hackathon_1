import os
import pathlib
from config import PATH

PATH_files = PATH / "data/files"
path_db = PATH / "data/db.json"


def add_file(id: int,
             url_id: str,
             name_subject: str,
             name_teacher: str,
             date: str,
             length: str,
             path: str,
             size: str):
    pass


def remove_file(id: int):
    pass


def search_file(name_teacher: str,
                name_object: str,
                date: str,
                count: int):
    pass


def get_max_id() -> int:
    pass


def remove_temporary_files(url_id: str):
    pass


def update_json(dict_lecture: dict):
    list_lecture = list(dict_lecture.values())

    with open(path_db, "r") as db:
        db = db.readlines()

    db = eval(db)
    data = {}
    i = 1

    for lecture in list_lecture:
        for element in db["list"]:
            if lecture["url"] == element["url"]:
                lecture["id"] = element["id"]
                lecture["name_file"] = element["name_file"]
                lecture["length"] = element["length"]
                lecture["path"] = element["path"]
                lecture["size"] = element["size"]

                break

        dict = {f'lection_{i}': lecture}
        i += 1
        data.update(dict)

    return data

