import json  # Импортируем JSON формат для передачи данных между контроллером и БД
import requests  # Импорт библиотеки для отправки HTTP-запросов
import urllib
import os
from bs4 import BeautifulSoup
import subprocess
import pathlib
from config import PATH

TEST_URL = "https://bbb.ssau.ru:8443/playback/presentation/2.3/aa788c4e3599195fe1a7a12ad585903f44c6f9ed-1739185560849"

METADATA_TEST_URL = "https://bbb.ssau.ru/b/djn-zw7-mep"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

PATH_files = pathlib.Path(PATH) / "data/temporary_files"


class Parser:

    def get_data(self, url: str):
        page = requests.get(url.replace("/playback", "").replace("/2.3", "") + "/presentation_text.json")
        content = json.loads(page.content)
        string = ""
        for key in content.keys():
            string = string + key + " "
        return "https://bbb.ssau.ru:8443/presentation/" + url.split("/")[6] + "/presentation/" + string.split(" ")[
            1] + "/svgs/slide" + "&" + string.split(" ")[1]

    def download_audio(self, url: str):
        id = url.split("/")[4]
        audio_id = url.split("&")[0].split("/")[4]
        audio_url = "https://bbb.ssau.ru:8443/presentation/" + audio_id + "/video/webcams.webm"

        path_id = pathlib.Path(PATH_files) / id

        if not os.path.exists(path_id):
            os.makedirs(path_id)
        if not os.path.exists(path_id / "audio"):
            os.makedirs(path_id / "audio")

        urllib.request.urlretrieve(audio_url, path_id / "audio/lecture.webm")
        return 0

    def get_metadata(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        lection_title = soup.find('h1', class_="display-3 text-left mb-3 font-weight-400").get_text(strip=True)
        teacher_name = soup.find('h5', id="room-owner-name",
                                 class_="font-weight-normal ml-4 mt-3 d-inline-block").get_text(strip=True).replace(
            " (Владелец)", "")
        lections_table = soup.find_all("table", id="recordings-table")[0]
        lections = lections_table.find_all("tr")[2:]
        i = 0
        data = {}
        for lection in lections:
            time = lection.find("time").get_text(strip=True)
            lection_url = \
                lection.find("a", class_="btn btn-sm btn-primary", target="_blank").get_attribute_list("href")[0]
            dict = {f'lection_{i}': {
                "id": None, "name_file": None, "name_teacher": teacher_name, "url": lection_url,
                "name_subject": lection_title,
                "datetime": time, "lenght": None, "path": None, "size": None
            }}
            data.update(dict)
            i += 1

        return data

    def main_cycle(self, url):
        self.download_image(self.get_data(url))
        self.download_audio(self.get_data(url))
        # self.get_length(url.split("/")[6] + "/audio/lecture.webm")
        return url.split("/")[6]

    def get_length(self, path):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        duration = result.stdout.decode('utf-8').strip()
        print(duration)
        
        return float(duration)

    def download_image(self, url: str):
        i = 1
        url = url.split("&")[0]
        id = url.split("/")[4]

        path_id = pathlib.Path(PATH_files) / id

        if not os.path.exists(path_id):
            os.makedirs(path_id)
        if not os.path.exists(path_id / 'slides'):
            os.makedirs(path_id / "slides")
        while True:
            try:
                save_path = path_id / f"/slides/slide{str(i)}.svg"
                response = requests.get(url + str(i) + ".svg")
                if response.status_code == 200:
                    with open(save_path, "wb") as file:
                        file.write(response.content)
                    i += 1
                else:
                    break
            except:
                break
        return 0


if __name__ == "__main__":
    test = Parser()
    test.get_metadata(METADATA_TEST_URL)
