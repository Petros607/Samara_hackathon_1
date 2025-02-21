import src.bbbparser.main
import src.database_manager
import os
from src.ai.decode_audio.audio_recognition import AudioRecognition
from src.ai.summary.summary import SummaryLection
from config import PATH

Parser = src.bbbparser.main.Parser()


def get_list_lecture(url_room: str) -> dict[dict]:
    l = Parser.get_metadata(url_room)
    list_lecture = src.database_manager.update_json(l)

    return list_lecture


def handler_lecture(url_lecture: str):
    if not src.database_manager.check_lecture(url_lecture):
        url_id = Parser.main_cycle(url_lecture)

        path_audio_file = PATH / f"data/temporary_files/{url_id}/audio/lecture.webm"
        path_temp_file_json = PATH / f"data/temporary_files/{url_id}"
        path_temp_file_txt = PATH / f"data/temporary_files/{url_id}"
        length_audio = Parser.get_length(str(PATH / f"data/temporary_files/{url_id}/audio/lecture.webm"))
        count_slides = len(os.listdir(PATH / f"data/temporary_files/{url_id}/slides/"))

        recognizer = AudioRecognition()
        summarizer = SummaryLection()

        recognizer.recognize_to_file(
            input_file=path_audio_file,
            output_file=path_temp_file_json
        )

        text = recognizer.parse_from_file(
            input_file=path_temp_file_json,
            audio_delay=length_audio,
            slide_count=count_slides
        )

        summarizer.transform_json_to_txt(
            input_file=path_temp_file_json,
            output_file=path_temp_file_txt
        )

        summary = summarizer.summarize_from_file(
            input_file=path_temp_file_txt
        )

        # TODO generation PDF

        src.database_manager.remove_temporary_files(url_id)
        src.database_manager.add_file(name_file=f"{url_id}.pdf",
                                      url=url_lecture,
                                      length=length_audio,
                                      path=PATH / f"data/files/{url_id}.pdf",
                                      size=None)
