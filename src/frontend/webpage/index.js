const overlay = document.getElementById("overlay");

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
                console.log(error);
                overlay.style.display = "none"
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
        createAndAppendElementWithInnerHTML(`<div class="lection_name_teacher">${lections[key]["name_teacher"]}</div><div class="lection_title">${lections[key]["name_subject"]}</div><div class="lection_time">${lections[key]["datetime"]}</div><div class="lection_download_btn"><button onClick="httpGet('/get_lecture?url_lecture=${lection_url}')" id="searchButton">${lections[key]['path'] == null ? 'Сгенерировать':'Скачать'}</button></div>`, lection);
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

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return eval(xmlHttp.responseText);
};

function modify_lections(lections) {
    const parent_elem = document.getElementById("tableSection");
    parent_elem.classList.remove("visible");
    parent_elem.innerHTML = "";
    for (key in lections) {
        const lection = document.createElement("div");
        lection.className = "lections";
        lection_url = lections[key]["url"];
        createAndAppendElementWithInnerHTML(`<div class="lection_name_teacher">${lections[key]["name_teacher"]}</div><div class="lection_title">${lections[key]["name_subject"]}</div><div class="lection_time">${lections[key]["datetime"]}</div><div class="lection_download_btn"><button onClick="httpGet('/get_lecture?url_lecture=${lection_url}')" id="searchButton">${lections[key]['path'] == null ? 'Сгенерировать':'Скачать'}</button></div>`, lection);
        parent_elem.appendChild(lection);
    }
    parent_elem.classList.add("visible");
}
