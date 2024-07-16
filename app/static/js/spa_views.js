

// основной контейнер отображения информации
let containerViewsClass = '.view-content';


function loadingView() {
    // анимация загрузки
    $(containerViewsClass).html(animLoadingHTML);
}

function errorView(info) {
    // анимация загрузки
    $(containerViewsClass).html(errorHTML);
}

function userInfoView(data) {
    // анимация загрузки
    $(containerViewsClass).html($('<div>', {class: 'user-info'}))
    $.each(data.info_list, function (indexInArray, valueOfElement) { 
         $(`<div>${valueOfElement}</div>`).appendTo('.user-info');
    });

    if (data.dedicaded_ip) {
        $(`<div>Поключена услуга выделенный IP</div>`).appendTo('.user-info');
    }
}

function operationsView(data) {
    // анимация загрузки
    $(containerViewsClass).html($('<div>', {class: 'operations-list'}))
    $.each(data, function (indexInArray, valueOfElement) { 
         $(`<div>${valueOfElement}</div>`).appendTo('.operations-list');
    });
}

function tarifView() {
    // анимация загрузки
    $(containerViewsClass).html($('<div>', {class: 'tarif-list'}))
    $.each(data, function (indexInArray, valueOfElement) { 
         $(`<div>${valueOfElement}</div>`).appendTo('.operations-list');
    });
}

function phoneView() {
    // анимация загрузки
}

function paymentView() {
    // анимация загрузки
}