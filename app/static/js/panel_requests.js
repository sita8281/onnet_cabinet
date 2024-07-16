function addRequestsToPanel() {
    // добавить действия к кнопкам в панели-меню
    
}

let requestRunning = false;

function routeRequest(url, selectedId) {
    /* навесить маршрут запроса на кнопку или ссылку,
    нужно для панели-меню */

    if (requestRunning) {
        return;
    }

    // убрать выделение со всех кнопок
    let buttonsList =  $('.panel').children();
    $.each(buttonsList, function (indexInArray, valueOfElement) { 
        $('#' + valueOfElement.id).removeClass('selected__a');

    });


    // выделить нажатую кнопку
    if (selectedId) {
        $('#' + selectedId).addClass('selected__a');
    }
        
}


function urlHandler(url) {
    /* Обработчик URL к API ендпоинтам, нужен для сопоставления ссылок с 
    HTML-отображением информации, приходящий от API */
    switch (url) {
        case '/user':
            break;
        case '/operations':
            break;
        case '/tarif':
            break;
        case '/phone':
            break;
        case '/payment':
            break;

    }
}

