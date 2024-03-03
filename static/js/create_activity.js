const SL =() => {
    const create_activity = document.querySelector('.create_activity');
    const wrapper = document.querySelector('.wrapper_task');
    const btn = document.querySelector('#submit')
    const todoID = window.location.href.split('/')[4]
    const form = document.querySelector('#former')
    let elements = form.querySelectorAll('.add_subtask');

    const deadline = document.getElementById('deadline');
    const inputDate = document.querySelector('#submit');

    const checkForm = () => {
        if(deadline.value){
            inputDate.disabled = false
        }else{
            inputDate.disabled = true
        }
    };
    checkForm()

    deadline.addEventListener('change', checkForm)

    //! Меняем ID элементов после их удаления
    const changeID = (elements) => {
        elements.forEach((elem, index) => {
            elem.id = index + 1;
            elem.children[0].id = `subtaskname_${index + 1}`
            elem.children[0].name = `subtaskname_${index + 1}`
        })
    }

    //! Меняем значение action='' в поле <form> html
    const writeForm = () => {
        const uri = window.location.origin
        elements = form.querySelectorAll('.add_subtask');
        form.action = `${uri}/push_data/${todoID}/${elements.length}`;
    }

    //! Создание куска кода html
    create_activity.addEventListener('click', (event) => {
        event.preventDefault()

        if (elements.length == 0) {
            const listItem = document.createElement('div');
            const ID = elements.length + 1;
            const content = `
            <div class="add_subtask" id='${ID}'>
                <input id="subtaskname_${ID}" name="subtaskname_${ID}" type="text" placeholder="Напиши подзадачу" required>
                <button class='remove_active'></button>
            </div>
            `
            listItem.insertAdjacentHTML("beforeend", content);
            wrapper.insertBefore(listItem, btn);
            writeForm()
        } else {
            const listItem = document.createElement('div');
            const ID = elements.length + 1;
            const content = `
            <div class="add_subtask" id='${ID}'>
                <input id="subtaskname_${ID}" name="subtaskname_${ID}" type="text" placeholder="Напиши подзадачу" required>
                <button class='remove_active'></button>
            </div>
            `
            listItem.insertAdjacentHTML("beforeend", content);
            wrapper.insertBefore(listItem, btn);
            writeForm()
        }
    });

    //! Удаление подзадачи
    wrapper.addEventListener('click', (e) => {
        const target = e.target
        if (target.classList.contains('remove_active'))
            {const parent = target.closest('.add_subtask');
                parent.remove()
                
                elements = form.querySelectorAll('.add_subtask');
                changeID(elements)
                writeForm()
            }
    });
}
SL()