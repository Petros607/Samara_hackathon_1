import whisper
from datetime import time


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

    def recognize(
        self,
        input_file: str,
        audio_delay: int | None = None,
        slide_count: int | None = None,
    ) -> list[list[dict[str, str | time]]]:
        text_parts = self.model.transcribe(input_file, word_timestamps=True)["segments"]
        return self._divide_text_parts(
            text_parts=text_parts, audio_delay=audio_delay, slide_count=slide_count
        )

    def _divide_text_parts_by_delay(
        self,
        text_parts: list[dict],
        delay: int,
        start_time: float,
        need_enclosure: bool,
    ) -> list[dict] | list[list[dict]]:
        result = []
        to_join = []
        border = start_time + delay
        for part in text_parts:
            if not start_time:
                start_time = part["start"]
            if part["start"] < border:
                to_join.append(part["text"])
            else:
                new_part = {
                    "time": seconds_to_time(start_time),
                    "text": "".join(to_join),
                }
                if need_enclosure:
                    result.append([new_part])
                else:
                    result.append(new_part)
                to_join = []
                border = border + delay
                start_time = None
        return result

    def _divide_text_parts(
        self,
        text_parts: list[dict],
        audio_delay: int | None = None,
        slide_count: int | None = None,
    ) -> list[list[dict[str, str | time]]]:
        if (
            not (audio_delay and slide_count)
            or audio_delay // slide_count < self._DELAY * 2
        ):
            return self._divide_text_parts_by_delay(
                start_time=0,
                delay=self._DELAY,
                text_parts=text_parts,
                need_enclosure=True,
            )
        delay = audio_delay // slide_count
        start_time = 0
        result = []
        to_cut = []
        border = start_time + delay
        for part in text_parts:
            if part["start"] < border:
                to_cut.append(part)
            else:
                result.append(
                    self._divide_text_parts_by_delay(
                        start_time=start_time,
                        delay=60,
                        text_parts=to_cut,
                        need_enclosure=False,
                    )
                )
                start_time = part["start"]
                border = start_time + delay
                to_cut = []
        return result


recognizer = AudioRecognition()
print(recognizer.recognize("lecture.mp3"))
