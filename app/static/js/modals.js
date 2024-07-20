function showModal(label, text, state, callback) {
    let stateClass = 'window-info';
    let imgHTML = '<img class="window-icon" src="/static/images/info-blue.svg">'

    switch (state) {
        case 'success':
            stateClass = 'window+' + state
            imgHTML = '<img class="window-icon" src="/static/images/check.svg">'
            break;
        case 'error':
            stateClass = 'window+' + state
            imgHTML = '<img class="window-icon" src="/static/images/cross.svg">'
            break;
    }
    const modal = `
    <div class="background-modal">
        <div class="modal-window">
            <div class="window-top">
                ${imgHTML}
                <label>${label}</label>
            </div>
            <div class="window-middle">${text}</div>
            <div class="window-bottom">
                <a href="javascript:closeModal()">Закрыть</a>
            </div>
        </div>
    </div>
    `
    $(modal).appendTo('body');
    
}

function closeModal() {
    // убрать окно через анимацию
    $('.modal-window').addClass('modal-close');
    setTimeout(() => {
        $('.background-modal').remove();
        $('.')
        if (callback) {
            callback();
        }
    }, 600);
}