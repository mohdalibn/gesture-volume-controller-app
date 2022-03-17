
// Script to change the Volume Value
const slider = document.querySelector("input");
const value = document.querySelector(".volume-value");

value.textContent = slider.value;

slider.oninput = function(){
    value.textContent = this.value;
}