const overlay = document.getElementById("overlay");
//https://cdna.artstation.com/p/assets/images/images/047/774/418/original/camila-brugnoli-carpincho.gif?1648418619
//href="/get_lecture?url_lecture=${lection_url}"
document.getElementById('searchButton').addEventListener('click', function() {
    const url = document.getElementById('urlInput');
    url_value = url.value;
    simulate_loading();
    if (url) {
        fetch(`/get_list?url_room=${url_value}`)
            .then(response => response.json())
            .then(data => {
                overlay.style.display = "none";
                if (document.getElementById("tableSection").hasChildNodes) {
                    modify_lections(data)
                } else {
                    set_lections(data);
                };
            })
            .catch(error => {
                // overlay.style.display = "none"
                // set_lections(json);
                document.getElementById('response').innerText = 'Ссылка не найдена';
            }); 
    } else {
        document.getElementById('response').innerText = 'Пожалуйста, введите URL.';
    }
});

function set_lections(lections) {
    const parent_elem = document.getElementById("tableSection");
    for (key in lections) {
        const lection = document.createElement("div");
        lection.className = "lections";
        lection_url = lections[key]["url"];
        createAndAppendElementWithInnerHTML(`<div class="lection_name_teacher">${lections[key]["name_teacher"]}</div><div class="lection_title">${lections[key]["name_subject"]}</div><div class="lection_time">${lections[key]["datetime"]}</div><div class="lection_download_btn"><a onClick="httpGet('/get_lecture?url_lecture=${lection_url}', 'conspect.pdf')" class="lecture_download_a">${lections[key]['path'] == null ? 'Сгенерировать':'Скачать'}</a></div>`, lection);
        parent_elem.appendChild(lection);
    }
    parent_elem.classList.add("visible");
};

function createAndAppendElementWithInnerHTML(html, container) {
    container.innerHTML += html;
    return container.lastElementChild;
};

function simulate_loading() {
    overlay.style.display = "flex";
}

function httpGet(theUrl, fileName) {   
    document.getElementById('response').innerText = '';
    simulate_loading();

    requestAnimationFrame(() => {
        requestAnimationFrame(() => { 
            fetch(theUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка');
                    }
                    return response.blob();
                })
                .then(blob => {
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = fileName || theUrl.split('/').pop();
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    URL.revokeObjectURL(link.href);
                })
                .catch(() => {
                    document.getElementById('response').innerText = 'Ошибка загрузки файла'; 
                })
                .finally(() => {
                    overlay.style.display = "none";
                });
        });
    });
}


function modify_lections(lections) {
    const parent_elem = document.getElementById("tableSection");
    parent_elem.classList.remove("visible");
    parent_elem.innerHTML="";
    for (key in lections) {
        const lection = document.createElement("div");
        lection.className = "lections";
        lection_url = lections[key]["url"];
        createAndAppendElementWithInnerHTML(`<div class="lection_name_teacher">${lections[key]["name_teacher"]}</div><div class="lection_title">${lections[key]["name_subject"]}</div><div class="lection_time">${lections[key]["datetime"]}</div><div class="lection_download_btn"><a onClick="httpGet('/get_lecture?url_lecture=${lection_url}', 'conspect.pdf')" class="lecture_download_a">${lections[key]['path'] == null ? 'Сгенерировать':'Скачать'}</a></div>`, lection);
        parent_elem.appendChild(lection);
    }
    parent_elem.classList.add("visible");
}

const json = {

    "lection_0": {
        "id": null,
        "name_file": null,
        "name_teacher": "\u0413\u0440\u0435\u0448\u043d\u044f\u043a\u043e\u0432 \u041f\u0430\u0432\u0435\u043b \u0418\u0432\u0430\u043d\u043e\u0432\u0438\u0447",
        "url": "https://bbb.ssau.ru:8443/playback/presentation/2.3/cf5215d4ed77ac8f39337081f34c2a49a413621d-1649044933105",
        "name_subject": "\u0420\u043e\u0431\u043e\u0442\u043e\u0442\u0435\u0445\u043d\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441\u044b",
        "datetime": "Apr 04, 2022 4:02am",
        "lenght": null,
        "path": "что-то",
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
};