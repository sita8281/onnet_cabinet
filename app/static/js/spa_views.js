

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

function tarifView(data) {
    // анимация загрузки
    $(containerViewsClass).html($('<div>', {class: 'tarif-list'}))
    $.each(data.tarifs, function (indexInArray, valueOfElement) { 
         $(`<div>${valueOfElement}</div>`).appendTo('.tarif-list');
    });
    $(`<div>Текущий тариф: ${data.current}</div>`).appendTo('.tarif-list');
}

function phoneView() {
    // анимация загрузки
}

function paymentView(data) {
    // анимация загрузки
    let htmlDoc = `
    <div>Оплата</div>
    <input type="text" placeholder="Сумма оплаты, Руб" value="${data.amount}" id="payment_sum">
    <input type="checkbox" name="" id="" placeholder="Автопродление">
    <button id="payment_button">Оплатить</button>
    `
    $(containerViewsClass).html($(htmlDoc))
    $('#payment_button').click(function (e) { 
        e.preventDefault();
        openPaymentWindow(
            parseFloat($('#payment_sum').val()),
            data.account_id
        )
    });
    
}