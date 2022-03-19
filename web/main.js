
// Script to change the Volume Value
const slider = document.querySelector("input");
const value = document.querySelector(".volume-value");

value.textContent = slider.value;

slider.oninput = function(){
    value.textContent = this.value;
}

eel.SendVol()()
eel.expose(SetVolume)
function SetVolume(Vol){
    Vol = Vol.toString()
    slider.value = Vol;
    value.textContent = slider.value;
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

    // Calling the DisplayVideo() function in the Python File
    eel.DisplayVideo()()

    // // Setting the Visibility of the Image Window to Visible
    // ImageWindow.style.visibility="visible";

}

eel.expose(UpdateVideoScreen);
function UpdateVideoScreen(Fps, Xpos1, Ypos1, Xpos2, Ypos2, Frame){
    ImageWindow.src = "data:image/jpeg;base64," + Frame;

    let Statistics = [Fps, Xpos1, Ypos1, Xpos2, Ypos2]
    Statistics.forEach(element => {
        element = element.toString();
    });

    // // Converting the Numeric FPS into a String
    // var FPS = Fps.toString();


    // Updating the InnerHTML of the FPS counter text
    document.querySelector('.fps').innerHTML = "FPS: " + Fps;
    document.querySelector('.xpos1').innerHTML = "XPOS1: " + Xpos1;
    document.querySelector('.ypos1').innerHTML = "YPOS1: " + Ypos1;
    document.querySelector('.xpos2').innerHTML = "XPOS2: " + Xpos2;
    document.querySelector('.ypos2').innerHTML = "YPOS2: " + Ypos2;

}

function CloseVideo(){

    // Setting the Display of the Image Window to None
    ImageWindow.style.display="none";

    // Calling the CloseWebcam() function in the Python File
    eel.CloseWebcam()()

    // // Setting the Visibility of the Image Window to Hidden
    // ImageWindow.style.visibility="hidden";

    // Removing the Video WIndow Border When the User closes the webcam
    VideoWindow.style.border = "none";

    // Setting the Display of the Webcam OFF Text to Block
    VideoText.style.display="block";

}

eel.expose(SetFPSZero);
function SetFPSZero(){
    document.querySelector('.fps').innerHTML = "FPS: 0";
}