// подгрузка данных после полной загрузки страницы

window.onload = () => {
    routeRequest('/user', 'a-info')
}


// глобальная переменная, подключен выделенный IP или нет

let dedicIpState = false;

function controlMenu(e) {
    if ($('.panel').css('display') == 'none') {
        $('.panel').css('display', 'flex')
        $('.panel').removeClass('hide-panel');
    } else {
        
        setTimeout(() => {
            $('.panel').removeAttr('style');
            $('.panel').removeClass('hide-panel');
        }, 800);
        $('.panel').addClass('hide-panel');
        //$('.panel').css('display', 'none')
    }
}


$('.button__menu').click(controlMenu);