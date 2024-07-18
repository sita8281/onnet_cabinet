

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
    const content = `
    <div class="label-content">Профиль абонента</div>
    <table class="info-table">
        <thead></thead>
            <tbody class="tbody-list">
            </tbody>
    </table>
    `

    $('.view-content').html(content);
    $.each(data.info_list, function (indexInArray, valueOfElement) { 
         $(`<tr><td class="td-name">${valueOfElement[0]}</td><td class="td-info">${valueOfElement[1]}</td></tr>`).appendTo('.tbody-list');
    });

    if (data.dedicaded_ip) {
        $(`<tr><td class="td-name">Выделенный IP:</td><td class="td-info on-ip">Услуга подключена</td></tr>`).appendTo('.tbody-list');
    } else {
        $(`<tr><td class="td-name">Выделенный IP:</td><td class="td-info off-ip">Услуга не подключена</td></tr>`).appendTo('.tbody-list');
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