import bbbparser.main
import database_manager

Parser = bbbparser.main.Parser()


def get_list_lecture(url_room: str) -> dict[dict]:
    list_lecture = database_manager.update_json(Parser.get_metadata(url_room))

    return list_lecture

def download_lecture_files(url_lecture: str) -> str:
    url_id = Parser.main_cycle(url_lecture)

    return url_id
