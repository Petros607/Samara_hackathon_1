import whisper
from datetime import time
import json


def seconds_to_time(seconds: int | float) -> time:
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)  # Разделяем на часы и остаток
    minutes, seconds = divmod(remainder, 60)  # Разделяем остаток на минуты и секунды
    return time(hour=hours, minute=minutes, second=seconds)


class AudioRecognition:
    _DELAY = 60

    def __init__(self, model: str = "turbo"):
        """Downloads model of whisper and initializes it

        Args:
            model (str, optional): Model of whisper.
            One of ["tiny", "base", "small", "medium", "large", "turbo"].
            Defaults to "turbo".
        """
        self.model = whisper.load_model(model)

    def recognize_to_file(self, input_file: str, output_file: str) -> None:
        text_parts = self.model.transcribe(str(input_file), word_timestamps=True)["segments"]
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(text_parts, f, ensure_ascii=False)

    def parse_from_file(
        self,
        input_file: str,
        slide_count: int | None = None,
    ) -> list[list[dict[str, str | time]]]:
        with open(input_file, "r", encoding="utf-8") as f:
            text_parts = json.load(f)
        return self._divide_text_parts(
            text_parts=text_parts, slide_count=slide_count
        )

    def recognize(
        self,
        input_file: str,
        audio_delay: int | None = None,
        slide_count: int | None = None,
    ) -> list[list[dict[str, str | time]]]:
        text_parts = self.model.transcribe(input_file, word_timestamps=True)["segments"]
        return self._divide_text_parts(
            text_parts=text_parts, slide_count=slide_count
        )

    def _divide_text_parts_by_delay(
        self,
        text_parts: list[dict],
        delay: int,
    ) -> list[dict]:
        result = []
        to_join = []
        start_time = text_parts[0]["start"]
        end = start_time+delay
        for part in text_parts:
            if part["start"]<end:
                to_join.append(part["text"])
            else:
                result.append(
                    {
                        "time": seconds_to_time(start_time),
                        "text": "".join(to_join)
                    }
                )
                start_time = part["start"]
                end = start_time+delay
                to_join = [part["text"]]
        result.append(
            {
                "time": seconds_to_time(start_time),
                "text": "".join(to_join)
            }
        )
        return result

    def _divide_text_parts(
        self,
        text_parts: list[dict],
        slide_count: int | None = None,
    ) -> list[list[dict[str, str | time]]]:
        if not slide_count:
            slide_count+=1
        audio_delay = text_parts[-1]["end"]
        slide_delay = audio_delay / slide_count
        end = slide_delay
        result = []
        grouped_parts = []
        for part in text_parts:
            if part["start"] <= end:
                grouped_parts.append(part)
            else:
                result.append(self._divide_text_parts_by_delay(
                    text_parts=grouped_parts,
                    delay =  self._DELAY,
                ))
                grouped_parts = [part]
                end = part["start"] + slide_delay
        result.append(self._divide_text_parts_by_delay(
                    text_parts=grouped_parts,
                    delay =  self._DELAY,
                ))
        return result