// подгрузка данных после полной загрузки страницы

window.onload = () => {
    routeRequest('/user', 'a-info')
    
}


// глобальная переменная, подключен выделенный IP или нет

let dedicIpState = false;