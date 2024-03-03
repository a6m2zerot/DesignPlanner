const elements = document.querySelectorAll('.round');
const daysToFind = [6, 7, 13, 14, 20, 21, 27, 28, 34, 35, 41, 42]

for (let i = 0; i < elements.length; i++) {
    if (daysToFind.includes(i + 1) && elements[i].style.backgroundColor != 'transparent') {
        elements[i].style.backgroundColor = '#FFFF73';
        }
    };