
/* 
Базовые HTML заготовки под отображение различных данных
*/

// оторажение пользовательских данных
const userInfoHTML = `
<div class=>
  <h1>Информация</h1>
</div>

`

// оторажение списка тарифов
const tarifHTML = `
<h1>Тарифы</h1>
`

// отображение истории операций 
const operationsHTML = `
<h1>Операции</h1>
`

// отображение оплаты
const paymentHTML = `
<h1>Оплата</h1>
`

// отображение привязки номера к SMS уведомлениям 
const phoneHTML = `
<h1>SMS привязка</h1>
`

// отображение анимации загрузки
const animLoadingHTML = `
<div class="loader-container"><span class="loader"></span></div>
`

// отображение ошибки
const errorHTML = `
<label style="font-family: 'Roboto', sans-serif; font-size: 128px; font-weight: 500;">:(</label>
<br>
<label style="font-family: 'Roboto', sans-serif; font-size: 25px; font-weight: 300;">Не удалось загрузить информацию, повторите попытку</label>
`