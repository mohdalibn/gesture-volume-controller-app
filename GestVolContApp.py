
"""

    Project: Gesture Volume Controller App
    Made By: Mohd Ali Bin Naser
    Github : github.com/mohdalibn

"""

# Importing the required libraries for the project
from tkinter import Tk, messagebox
import eel
import cv2
import sys
import logging
import base64
import os


#
Webcam = None

# Creating a class for the OpenCV Webcam Input


class OpenWebcam(object):
    def __init__(self):  # Init Method
        # Getting the User's Webcam Video Input Using OpenCV
        self.CamVideo = cv2.VideoCapture(0)

        # Setting the Width and Height of the Video Window
        self.VidWidth = self.CamVideo.set(3, 660)
        self.VidHeight = self.CamVideo.set(4, 480)

    def GetFrame(self):  # Method to get the individual frames of the Video
        success, frame = self.CamVideo.read()

        if success:
            _, jpegFrame = cv2.imencode('.jpg', frame)
            return jpegFrame.tobytes()

        else:
            return None

    # Method to Close the Webcam Video Feed
    def CloseVideo(self):
        self.CamVideo.release()

    def __del__(self):  # Method to close the Webcam Video Stream
        self.CamVideo.release()


# This function creates a generator for all the video frames
def GenerateFrames(Webcam):
    while True:
        singleframe = Webcam.GetFrame()

        if singleframe != None:
            yield singleframe

        else:
            break


# function that updates the Video Frames in the App
@eel.expose
def DisplayVideo():
    global Webcam

    # This if statement acts as a Button Spam Filter
    if Webcam is None:
        # Creating an instance of the OpenWebcam class
        Webcam = OpenWebcam()

        # Calling the GenerateFrames() function
        VideoFrames = GenerateFrames(Webcam)

        for SingleFrame in VideoFrames:

            # for all the single frames in video frames, we are converting the frames from Bytes to base64 Encoded String.
            frame = base64.b64encode(SingleFrame)
            frame = frame.decode("utf-8")
            eel.UpdateVideoScreen(frame)()

    else:
        # Displays text on the terminal when the Open Webcam button is spammed
        print("Do Not Spam The Button!")

# Function that closes the Webcam Video Stream


@eel.expose
def CloseWebcam():
    global Webcam

    # This if statement acts as a Button Spam Filter
    if Webcam is not None:
        # Releasing the Webcam using OpenCV
        Webcam.CloseVideo()
        Webcam = None
    else:
        # Displays text on the terminal when the Close Webcam button is spammed
        print("Do Not Spam The Button!")

# This function Displays the Error Message to the User using a Tkinter Window


def ThrowError(ErrorTitle, ErrorMsg):
    # This function will initialize a tkinter window to display the error message incase the eel App fails to load
    root = Tk()
    root.withdraw()

    # Call the messagebox class to show the error
    messagebox.showerror(ErrorTitle, ErrorMsg)

    # Close the tkinter window
    root.destroy()


# This is the main function that runs the eel App
def GestureVolumeControllerApp():

    # This function is going to handle errors
    try:

        # Getting the absolute path for the web files
        WebFolderDirectory = os.path.dirname(
            os.path.abspath(__file__)) + "\web"

        # # Initializing the eel App
        eel.init(WebFolderDirectory)

        # # Starting the eel App with index.html file and the window size
        eel.start('index.html', size=(1015, 750), options={
                  'chromeFlags': ['--disable-http-cache']}, suppress_error=True)

    except Exception as e:
        # Error message for displaying purpose
        ErrorMsg = 'There was a problem while loading the EEL App.'

        # Formatting the Error Message
        logging.error('{}\n{}'.format(ErrorMsg, e.args))

        # Calling the ThrowError Function to display the error message box to the User
        ThrowError(ErrorTitle='Failed to start the local server',
                   ErrorMsg=ErrorMsg)

        # Exiting the Python App
        sys.exit()


if __name__ == '__main__':

    # Calling the Main App Function to Run the App
    GestureVolumeControllerApp()
