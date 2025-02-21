document.getElementById('searchButton').addEventListener('click', function() {
    const url = document.getElementById('urlInput').value;
    if (url) {
        fetch(`https://api.example.com/search?url=${encodeURIComponent(url)}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('response').innerText = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById('response').innerText = 'Ссфлыка не найдена';
            });
    } else {
        document.getElementById('response').innerText = 'Пожалуйста, введите URL.';
    }

});

function set_lections(lections) {
    const parent_elem = document.getElementById(tableSection)
  for (key in lections.keys()) {
    const lection = document.createElement("div")
    lection.className = "lections"
    lection.createAndAppendElementWithInnerHTML(`<div><span>${lections[key]["name_teacher"]}</span><span>${lections[key]["datetime"]}</span></div><div><button id="searchButton">Скачать лекцию</button></div>`, )
  }
}

function createAndAppendElementWithInnerHTML(html, container) {
    container.innerHTML += html;
    return container.lastElementChild;
}
json = {

        "lection_0": {
            "id": null,
            "name_file": null,
            "name_teacher": "\u0413\u0440\u0435\u0448\u043d\u044f\u043a\u043e\u0432 \u041f\u0430\u0432\u0435\u043b \u0418\u0432\u0430\u043d\u043e\u0432\u0438\u0447",
            "url": "https://bbb.ssau.ru:8443/playback/presentation/2.3/cf5215d4ed77ac8f39337081f34c2a49a413621d-1649044933105",
            "name_subject": "\u0420\u043e\u0431\u043e\u0442\u043e\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441\u044b",
            "datetime": "Apr 04, 2022 4:02am",
            "lenght": null,
            "path": null,
            "size": null
        },
        "lection_1": {
            "id": null,
            "name_file": null,
            "name_teacher": "\u0413\u0440\u0435\u0448\u043d\u044f\u043a\u043e\u0432 \u041f\u0430\u0432\u0435\u043b \u0418\u0432\u0430\u043d\u043e\u0432\u0438\u0447",
            "url": "https://bbb.ssau.ru:8443/playback/presentation/2.3/cf5215d4ed77ac8f39337081f34c2a49a413621d-1645415216551",
            "name_subject": "\u0420\u043e\u0431\u043e\u0442\u043e\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441\u044b",
            "datetime": "Feb 21, 2022 3:46am",
            "lenght": null,
            "path": null,
            "size": null
        },
        "lection_2": {
            "id": null,
            "name_file": null,
            "name_teacher": "\u0413\u0440\u0435\u0448\u043d\u044f\u043a\u043e\u0432 \u041f\u0430\u0432\u0435\u043b \u0418\u0432\u0430\u043d\u043e\u0432\u0438\u0447",
            "url": "https://bbb.ssau.ru:8443/playback/presentation/2.3/cf5215d4ed77ac8f39337081f34c2a49a413621d-1636948468965",
            "name_subject": "\u0420\u043e\u0431\u043e\u0442\u043e\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441\u044b",
            "datetime": "Nov 15, 2021 3:54am",
            "lenght": null,
            "path": null,
            "size": null
        }
}

const element = document.getElementById("tableSection");
set_lections(json)