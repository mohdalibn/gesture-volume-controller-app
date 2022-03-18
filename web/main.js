
// Script to change the Volume Value
const slider = document.querySelector("input");
const value = document.querySelector(".volume-value");

value.textContent = slider.value;

slider.oninput = function(){
    value.textContent = this.value;
}


// Script for Opening and Closing The Webcam Video Stream

const VideoText = document.querySelector(".webcam-off-text") // Getting the Webcam OFF Text
let ImageWindow = document.getElementById('ImgWindow'); // Getting the Image Window
let VideoWindow = document.getElementById('VidWindow'); // Getting the Image Window


function OpenVideo(){
    // Setting the Display of the Webcam OFF Text to None
    VideoText.style.display="none";

    // Adding the Video Window Border when the User Opens the Webcam
    VideoWindow.style.border = "2px solid #BFAED2";

    // Setting the Display of the Image Window to Block
    ImageWindow.style.display="block";

    // Calling the DisplayVideo() function from the Python File
    eel.DisplayVideo()()
}

eel.expose(UpdateVideoScreen);
function UpdateVideoScreen(Value){
    ImageWindow.src = "data:image/jpeg;base64," + Value;

}

function CloseVideo(){

    // Setting the Display of the Image Window to None
    ImageWindow.style.display="none";

    // Removing the Video WIndow Border When the User closes the webcam
    VideoWindow.style.border = "none";

    // Setting the Display of the Webcam OFF Text to Block
    VideoText.style.display="block";
}