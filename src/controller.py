import src.bbbparser.main
import src.database_manager
import os
from src.ai.decode_audio.audio_recognition import AudioRecognition
from src.ai.summary.summary import SummaryLection
from src.pdfeel import pdf_generator as pdf
from config import PATH
import json

Parser = src.bbbparser.main.Parser()


def get_list_lecture(url_room: str) -> dict[dict]:
    l = Parser.get_metadata(url_room)
    list_lecture = src.database_manager.update_json(l)

    return list_lecture


def handler_lecture(url_lecture: str):
    url_id=url_lecture.split("/")[-1]
    if not src.database_manager.check_lecture(url_lecture):
        url_id = Parser.main_cycle(url_lecture)

        path_audio_file = PATH / f"data/temporary_files/{url_id}/audio/lecture.webm"
        path_temp_file_json = PATH / f"data/temporary_files/{url_id}/temp.json"
        path_temp_file_txt = PATH / f"data/temporary_files/{url_id}/temp.txt"
        length_audio = Parser.get_length(str(PATH / f"data/temporary_files/{url_id}/audio/lecture.webm"))
        slides = os.listdir(PATH / f"data/temporary_files/{url_id}/slides/")
        count_slides = len(list(filter(lambda x: x.endswith('.svg'), slides)))

        recognizer = AudioRecognition()
        summarizer = SummaryLection()

        recognizer.recognize_to_file(
            input_file=path_audio_file,
            output_file=path_temp_file_json
        )

        text = recognizer.parse_from_file(
            input_file=path_temp_file_json,
            slide_count=count_slides
        )

        summarizer.transform_json_to_txt(
            input_file=path_temp_file_json,
            output_file=path_temp_file_txt
        )

        summary = summarizer.summarize_from_file(
            input_file=path_temp_file_txt
        )

        pdf.generate_pdf(
            images_path=PATH / f"data/temporary_files/{url_id}/slides",
            texts=text,
            summary=summary,
            file_path=PATH / f"data/files/{url_id}.pdf"
        )
        src.database_manager.remove_temporary_files(url_id)
        src.database_manager.add_file(name_file=f"{url_id}.pdf",
                                      url=url_lecture,
                                      length=length_audio,
                                      path=PATH / f"data/files/{url_id}.pdf",
                                      size=None)
        
    return str(PATH / f"data/files/{url_id}.pdf")
