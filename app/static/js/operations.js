
function changeTarif(tarif, buttonId) {
    let oldBtn = $('#' + buttonId).clone();
    $('#' + buttonId).removeAttr('href');
    $('#' + buttonId).css('cursor', 'pointer');
    $('#' + buttonId).html('Загрузка..')
    $.ajax({
        type: "get",
        url: "/api/set_tariff",
        timeout: 5000,
        data: {tarif_plane: tarif},
        dataType: "json",
        success: function (response) {
            pass
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