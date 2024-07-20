
function openPaymentWindow (accountId) {
    var widget = new cp.CloudPayments();

    var data = {};
    var auto = $('#payment-sub').is(':checked'); //проверка
    let amount = $('#payment-sum').val()

    if (auto) { //включаем подписку

        var date = new Date(); //текущая дата
        date.setMonth(date.getMonth() + 1); //следующий месяц
        date.setDate(date.getDate() - 1); //минус один день

        var recurrent = { interval: 'Day', period: 30, startDate: date }; //один раз в месяц начиная со следующего месяца за минусом одного дня
        data.cloudPayments = {
            recurrent: recurrent
        }
    }
    widget.charge({ // options
        publicId: 'pk_524c2e6910d96abbecb08a0e7d7ae', //id из личного кабинета
        description: 'Пополнение счета. Договор № ' + accountId, //назначение
        amount: parseFloat(amount), //сумма
        currency: 'RUB', //валюта
	    invoiceId: accountId,
        accountId: accountId, //идентификатор плательщика (обязательно для создания подписки)
	    skin: "modern",
        data: data
    },
    function (options) { // success
        //действие при успешной оплате
        paymentOk();
    },
    function (reason, options) { // fail
        //действие при неуспешной оплате
        console.log('Не удалось пополнить баланс');
    });
};
