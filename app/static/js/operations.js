
function changeTarif(tarif, buttonId) {
    // смена тарифного плана
    let oldBtn = $('#' + buttonId).clone();
    $('#' + buttonId).removeAttr('href');
    $('#' + buttonId).css('cursor', 'pointer');
    $('#' + buttonId).html('Загрузка..')
    $.ajax({
        type: "get",
        url: "/api/set_tarif",
        timeout: 5000,
        data: {tarif_plane: tarif},
        dataType: "json",
        success: function (response) {
            routeRequest('/tarif', 'a-info'); //обновить текущую страницу
            $('#' + buttonId).replaceWith(oldBtn);
            if (response.status) {
                showModal(
                    label='Информация',
                    text=response.info,
                    state='info'
                );
            } else {
                showModal(
                    label='Ошибка',
                    text='Не удалось сменить тарифный план, сервер не ответил на запрос',
                    state='error'
                );
            }
            
        },
        error: function (response) {
            $('#' + buttonId).replaceWith(oldBtn);
            showModal(
                label='Ошибка',
                text='Не удалось сменить тарифный план, сервер не ответил на запрос',
                state='error'
            );
        }
    });
}

function changePhoneNumber() {
    let number = $('#phone-number').val();
    let oldBtn = $('.phone-button').clone();
    if (number.length < 10 && number.length > 0) {
        showModal(
            label='Короткий номер',
            text='Номер телефона должен состоять из 10 цифр',
            state='error'
        )
        return;
    }
    if (!number) {
        number = '';
    }

    $('.phone-button').removeAttr('href');
    $('.phone-button').css('cursor', 'pointer');
    $('.phone-button').html('Загрузка..')
    
    $.ajax({
        timeout: 5000,
        type: "get",
        url: "/api/set_phone",
        data: {'number': number},
        dataType: "json",
        success: function (response) {
            let txt = 'Новый номер телефона привязан к аккаунту, теперь на него будут приходить SMS уведомления'
            if (!number) {
                txt = 'Номер телефона успешно отвязан от аккаунта'
            }
            showModal(
                label='Успешно',
                text=txt,
                state='success'
            );
            routeRequest('/phone', 'a-sms');
        },
        error: function () {
            showModal(
                label='Ошибка',
                text='Не удалось сменить номер телефона',
                state='error'
            );
            $('.phone-button').replaceWith(oldBtn);
        }
    });


}