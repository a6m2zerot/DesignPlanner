window.addEventListener("DOMContentLoaded", ()=> {
    "use strict";

    const open_modal = document.querySelector('#open_modal');
    const close_modal = document.getElementById('close_modal');
    const modal = document.getElementById('modal');
    const body = document.getElementsByTagName('body');

    open_modal.addEventListener('click', () => {
        modal.classList.add('modal_vision'); // добавляем видимость окна
        document.body.style.overflow = 'hidden' // убираем прокрутку
    })

    close_modal.addEventListener('click', () => {
        window.setTimeout(function() { // удаляем окно через полсекунды (чтоб увидеть эффект закрытия).
            modal.classList.remove('modal_vision');
            document.body.style.overflow = '' // возвращаем прокрутку
            }, 100);
    });

});