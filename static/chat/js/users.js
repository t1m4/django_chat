"use strict";

function get_users(onSuccess, onError) {
    var URL = "/api/users/";
    var xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    //обработчик события
    xhr.addEventListener("load", function () {
        if (xhr.status === 200) {
            onSuccess(xhr.response);
        } else {
            onError("Статус ответа: " + xhr.status + " " + xhr.statusText);
        }
    });
    xhr.addEventListener("error", function () {
        console.log("Произошла ошибка соединения")
        onError("Произошла ошибка соединения");
    });
    xhr.addEventListener("timeout", function () {
        onError("Запрос не успел выполниться за " + xhr.timeout + "мс");
    });

    xhr.timeout = 3000; //10s
    //открываем запрос на сервер
    xhr.open("GET", URL);
    //отправляем запрос на сервер
    xhr.send();
}

function addElement(client) {
    for (var i in client) {
        var elem = document.createElement("p");
        elem.innerHTML = i.toString() + " " + client[i]
        document.body.appendChild(elem);
    }

}

function ok(data) {
    // addElement(data)
   // console.log(data.users);

}

function fail(url) {
    alert('Ошибка при запросе: ' + url);
}


(function () {
    get_users(ok, fail);
})();