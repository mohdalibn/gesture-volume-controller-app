
// Script to change the Volume Value
const slider = document.querySelector("input");
const value = document.querySelector(".volume-value");

value.textContent = slider.value;

slider.oninput = function(){
    value.textContent = this.value;
}


// Script for Hiding and Showing The Webcam Video Text

const VideoText = document.querySelector(".webcam-off-text")

function hideText(){
    VideoText.style.display="none";
}

function showText(){
    VideoText.style.display="block";
}