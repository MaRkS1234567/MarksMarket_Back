const buttonEl = document.getElementById('add_photo')
const divEl = document.getElementById('div_photo')
buttonEl.addEventListener('click', ()=> {
    divEl.classList.toggle("hidden");
    divEl.classList.toggle("showen");
})

// const buttonEl2 = document.getElementById('bt-2')
// const divEl2 = document.getElementById('div-2')
// buttonEl2.addEventListener('click', ()=> {
//     divEl2.classList.toggle("hidden");
//     divEl2.classList.toggle("showen");
// })