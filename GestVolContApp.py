
"""

    Project: Gesture Volume Controller App
    Made By: Mohd Ali Bin Naser
    Github : github.com/mohdalibn

"""

# Importing the required libraries for the project
import HandTrackingLibrary as Htl
from tkinter import Tk, messagebox
import mediapipe as mp
import numpy as np
import math
import eel
import cv2
import sys
import logging
import base64
import os
import time

# library and its flies for controlling the volume
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initializations from the pycaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

SysVol = math.ceil(volume.GetMasterVolumeLevel())
print(SysVol)

OldMin = -65
OldMax = 0
NewMin = 0
NewMax = 100
OldValue = -7

OldRange = (OldMax - OldMin)
NewRange = (NewMax - NewMin)
NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
NewValue = math.floor(NewValue)
print(NewValue)


# Default Webcam Variable Value to Start the App
Webcam = None

# Variables to store the current time and the previous time (To Calculate the FPS)
CurrTime = 0
PrevTime = 0

# Creating a class for the OpenCV Webcam Input


class OpenWebcam(object):
    def __init__(self):  # Init Method
        # Getting the User's Webcam Video Input Using OpenCV
        self.CamVideo = cv2.VideoCapture(0)

        # Setting the Width and Height of the Video Window
        self.VidWidth = self.CamVideo.set(3, 660)
        self.VidHeight = self.CamVideo.set(4, 480)

        # Creating an object from the Hand Tracking class with a detection confidence of 70%
        self.Tracker = Htl.HandTracker(DetectionConfidence=0.7)

    def GetFrame(self):  # Method to get the individual frames of the Video
        global CurrTime, PrevTime
        success, frame = self.CamVideo.read()

        if success:
            # Detecting the presence of a hand
            frame = self.Tracker.Detect_hands(frame)

            # Storing all the landmark positions of all the hand in a list
            LndmrkList = self.Tracker.Find_Landmark_Position(frame, draw=False)

            if len(LndmrkList) != 0:
                # The center coords of both the thumb and the index finger
                center_x1 = LndmrkList[4][1]
                center_y1 = LndmrkList[4][2]

                center_x2 = LndmrkList[8][1]
                center_y2 = LndmrkList[8][2]

                # Calculating the center of the line between the fingers
                LineCenter_x = (center_x1 + center_x2) // 2
                LineCenter_y = (center_y1 + center_y2) // 2

                # Drawing the filled circles around the center of the tips of the fingers
                cv2.circle(frame, (center_x1, center_y1),
                           8, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, (center_x2, center_y2),
                           8, (255, 0, 0), cv2.FILLED)

                # Drawing a line between the fingers
                cv2.line(frame, (center_x1, center_y1),
                         (center_x2, center_y2), (255, 0, 0), 3)

                # Drawing a circle in the center of the line
                cv2.circle(frame, (LineCenter_x, LineCenter_y),
                           8, (255, 0, 0), cv2.FILLED)

            _, jpegFrame = cv2.imencode('.jpg', frame)

            # Calculating the fps
            CurrTime = time.time()
            FPS = 1 // (CurrTime - PrevTime)
            PrevTime = CurrTime

            return FPS, jpegFrame.tobytes()

        else:
            # Here, we return 0 FPS and None Frame
            return 0, None

    # Method to Close the Webcam Video Feed
    def CloseVideo(self):
        self.CamVideo.release()

    def __del__(self):  # Method to close the Webcam Video Stream
        self.CamVideo.release()


# This function creates a generator for all the video frames
def GenerateFrames(Webcam):
    while True:
        fps, singleframe = Webcam.GetFrame()

        if singleframe != None:
            yield fps, singleframe

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

        for Fps, SingleFrame in VideoFrames:

            # for all the single frames in video frames, we are converting the frames from Bytes to base64 Encoded String.
            frame = base64.b64encode(SingleFrame)
            frame = frame.decode("utf-8")
            eel.UpdateVideoScreen(Fps, frame)()

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
