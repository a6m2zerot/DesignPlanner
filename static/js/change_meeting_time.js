const mts = document.getElementById('meeting_time_start');
const mtf = document.getElementById('meeting_time_finish');
const inputDate = document.querySelector('.inputdate');

const checkForm = () => {
    if(mts.value){
        inputDate.disabled = false
    }else{
        inputDate.disabled = true
    }
};

checkForm()

mts.addEventListener('change', ()=> {
    let new_mts = new Date(document.getElementById('meeting_time_start').value);
    new_mts.setHours(new_mts.getHours() + 4);  //! Здесь добавляем в функции ".... +4", т.к. учиьываем  часовой пояс UTC+3 и добавляем смещение на +1 час вперед
    let output = new_mts.toISOString().slice(0, 16).replace(/T/g, ' ');
    mtf.value = output;
    checkForm()
});   




