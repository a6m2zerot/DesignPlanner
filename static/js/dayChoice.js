const myContainer = document.querySelector('.my_container');
const events = document.querySelectorAll('.events');
const meetings = document.querySelectorAll('.meetings');


myContainer.addEventListener('click', (e) => {
    
    const target = e.target
    
    if (target.classList.contains('round') && target.style.backgroundColor != 'transparent') {
        const numb = target.getAttribute('value')

        events.forEach((elem) => {
            if (elem.getAttribute('value') == numb) {
                elem.style.display = 'block'
            } else {
                elem.style.display = 'none'
            };

        meetings.forEach((el) => {
            if (el.getAttribute('value') == numb) {
                el.style.display = 'block'
            } else {
                el.style.display = 'none'
            };
        });
    });
  };
});

