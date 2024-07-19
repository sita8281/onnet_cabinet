

// основной контейнер отображения информации
let containerViewsClass = '.view-content';


function loadingView() {
    // анимация загрузки
    $(containerViewsClass).html(animLoadingHTML);
}

function errorView(info) {
    // экран ошибки
    $(containerViewsClass).html(errorHTML);
}

function userInfoView(data) {
    // информация пользователя
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
    // история операций
    const content = `
    <div class="label-content">История платёжных операций</div>
    <table class="operations-table">
        <thead>
            <th>Дата</th>
            <th>Тип</th>
            <th>Сумма</th>
            <th>Описание</th>
        </thead>
        <tbody>
        </tbody>
    </table>
    `
    $('.view-content').html(content);
    $.each(data, function (indexInArray, valueOfElement) {
        let color = 'silver';
        if (indexInArray % 2 == 0) {
            color = '#F0F0F0';
        } else {
            color = 'white';
        }
        
        let row = `
        <tr style="background-color: ${color}">
            <td>${valueOfElement[0]}</td>
            <td>${valueOfElement[1]}</td>
            <td>${valueOfElement[2]}</td>
            <td>${valueOfElement[3]}</td>
        </tr>
        `
        $(row).appendTo('.operations-table tbody');
    });
}

function tarifView(data) {
    // доступные тарифы
    const content = `<div class="label-content">Доступные тарифы</div><div class="tarif-list"></div>`
    $(containerViewsClass).html($('<div>', {class: 'tarif-list'}))
    $('.view-content').html(content);
    $(`<div class="current-tarif">Текущий тариф: ${data.current[0]}</div>`).appendTo('.tarif-list');
    $(`<div class="box-tarif"></div>`).appendTo('.tarif-list');

    $.each(data.tarifs, function (indexInArray, valueOfElement) { 
         $(`<div class="unit-tarif"><div>${valueOfElement[0]}</div><a href="">Подключить</a></div>`).appendTo('.tarif-list');
    });
}

function paymentView(data) {
    // страница оплаты
    const content = `
    <div class="label-content">Пополнение баланса Банковской картой</div><div class="payment-container"></div>
    `
    $(containerViewsClass).html($(content))
    $('<label class="label-sub"><input id="payment-sub" type="checkbox">Включить ежемесячные платежи</label>').appendTo('.payment-container');
    $(`<div class="payment-sum"><label>Сумма:</label><input id="payment-sum" type="text" autocomplete="off" value="${data.amount}"></div>`).appendTo('.payment-container');
    $(`<a class="payment-button" href="javascript:openPaymentWindow('${data.account_id}')">Перейти к оплате</a>`).appendTo('.payment-container');
}

function phoneView(data) {
    // страница номера телефона
    const content = `
    <div class="label-content">Настройка SMS уведомлений</div><div class="phone-container"></div>
    `
    const notify = `
    <div class="info-notify">
        <div class="info-notify-header">
            <img src="/static/images/info.svg">
        </div>
        <label class="info-notify-text">
            Номер мобильного телефона без первой восьмерки, пробелов и скобок 10 цифр. <br>
            Пример: 9034445566
        </label>
    </div>
    `
    $(containerViewsClass).html($(content))
    $(notify).appendTo('.phone-container');
    $(`<div class="phone-div"><label>Номер телефона:</label><input maxlength="10" pattern="9[0-9]{9}" id="phone-number" type="text" autocomplete="off" value="${data}"></div>`).appendTo('.phone-container');
    $(`<a class="phone-button" href="">Сохранить</a>`).appendTo('.phone-container');
}


function controlView() {
    // страница услуг (выделенный IP)
    const content = `
    <div class="label-content">Список доступных услуг</div><div class="control-container"></div>
    `

    const notify = `
    <div class="info-notify">
        <div class="info-notify-header">
            <img src="/static/images/info.svg">
        </div>
        <label class="info-notify-text">
            Для отключения услуги "Выделенный IP" обратитесь в тех.поддержку
        </label>
    </div>
    `
    $(containerViewsClass).html($(content));
    $(notify).appendTo('.control-container');
    
}

