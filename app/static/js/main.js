// подгрузка данных после полной загрузки страницы

window.onload = () => {
    //routeRequest('/user', 'a-info')
    paymentOk();
}


// глобальная переменная, подключен выделенный IP или нет

let dedicIpState = false;