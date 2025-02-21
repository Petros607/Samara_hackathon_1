import os
import pathlib
import shutil
from config import PATH
import json

PATH_files = PATH / "data/files"
path_db = PATH / "data/db.json"


def get_max_id() -> int:
    with open(path_db, "r") as db:
        db = db.read()

    db = eval(db)

    max_id = 0
    for i in db["list"]:
        if i["id"] > max_id:
            max_id = i["id"]

    return max_id


def add_file(name_file: str,
             url: str,
             length: int,
             path: str,
             size: int):

    with open(path_db, "r") as db:
        db = db.read()

    db = eval(db)

    db["list"].append(
        {
            "id": get_max_id(),
            "name_file": name_file,
            "url": url,
            "length": length,
            "path": path,
            "size": size
        }
    )
    with open(path_db, "w") as file:
        json.dump(db, file)

    return 0


def remove_temporary_files(url_id: str):
    shutil.rmtree(PATH / f"data/temporary_files/{url_id}")


def check_lecture(url_lecture: str) -> bool:
    with open(path_db, "r") as db:
        db = db.read()
    return url_lecture in db


def update_json(dict_lecture: dict):
    v = dict_lecture.values()
    list_lecture = list(v)

    with open(path_db, "r") as db:
        db = json.load(db)

    data = {}
    i = 0

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
