
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
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# Initializations from the pycaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# Default Webcam Variable Value to Start the App
Webcam = None

# Variables to store the current time and the previous time (To Calculate the FPS)
CurrTime = 0
PrevTime = 0

# Storing the min and max volume levels
MinVolume = volume.GetVolumeRange()[0]
MaxVolume = volume.GetVolumeRange()[1]
Volume = 0  # This is the initial declaration of the variable to avoid the error of not being defined

# Getting the System Volume Level Using Pycaw
SystemVolume = volume.GetMasterVolumeLevelScalar()
SystemVolume = math.floor(SystemVolume * 100)
# print("System Volume Level: " + str(SystemVolume))


# This function updates the Display Volume according to the System Volume
@eel.expose
def SendVol(VolValue=SystemVolume):
    eel.SetVolume(VolValue)()


# Creating a class for the OpenCV Webcam Input
class OpenWebcam(object):
    def __init__(self):  # Init Method
        # Getting the User's Webcam Video Input Using OpenCV
        self.CamVideo = cv2.VideoCapture(0)

        # Setting the Width and Height of the Video Window
        self.VidWidth = self.CamVideo.set(3, 660)
        self.VidHeight = self.CamVideo.set(4, 480)

        # Creating an object from the Hand Tracking class with a detection confidence of 70%
        self.Tracker = Htl.HandTracker(DetectionConfidence=0.7, MaxHands=1)

        self.VolumePercentage = 0  # Variable to store the Volume Percentage Value
        self.BoundingArea = 0  # Variable to store the Bounding Box Area

    def GetFrame(self):  # Method to get the individual frames of the Video
        global CurrTime, PrevTime
        success, frame = self.CamVideo.read()

        if success:
            # Detecting the presence of a hand
            frame = self.Tracker.Detect_hands(frame)

            # Storing all the landmark positions of all the hand in a list
            LndmrkList, BndBox = self.Tracker.Find_Landmark_Position(
                frame, draw=True)

            # Variables to store the center coordinates of the thumb and index fingers
            center_x1 = 0
            center_y1 = 0
            center_x2 = 0
            center_y2 = 0

            if len(LndmrkList) != 0:

                # Normalizing the size of the hand to maintain a uniform calculation of the line length at different hand distance from the camera
                BndBoxWidth = BndBox[2] - BndBox[0]
                BndBoxHeight = BndBox[3] - BndBox[1]
                # Calculating the Area
                self.BoundingArea = (BndBoxWidth * BndBoxHeight) // 100

                if self.BoundingArea > 250 and self.BoundingArea < 1000:

                    frame, LineLength, CenterList = self.Tracker.Get_Finger_Distance(
                        frame, 4, 8, draw=True)

                    # Getting the Center Coordinates of the Thumb & the Index Fingers
                    center_x1, center_y1 = CenterList[0], CenterList[1]
                    center_x2, center_y2 = CenterList[2], CenterList[3]

                    LineCenter_x = CenterList[4]
                    LineCenter_y = CenterList[5]

                    # This volume convertion is for the percentage displays
                    self.VolumePercentage = np.interp(
                        LineLength, [24, 165], [0, 100])

                    # A constant increment volume value by "10" to smooth the volume increasing and decreasing experience.
                    VolSmoothness = 5
                    self.VolumePercentage = round(
                        self.VolumePercentage / VolSmoothness) * VolSmoothness

                    # Sets the Main System Volume Level According the Length of the Line between the thumb and the index finger
                    volume.SetMasterVolumeLevelScalar(
                        self.VolumePercentage / 100, None)

                    # Calling the SendVol Function to Updated the Volume Bar Indicator on the App
                    SendVol(VolValue=self.VolumePercentage)

                    if LineLength < 24:
                        # Changing the color to green when the length is less than 60
                        cv2.circle(frame, (LineCenter_x, LineCenter_y),
                                   8, (167, 99, 246), cv2.FILLED)

                # Displays Text if the User's Hand is smaller than the Range defined above
                elif self.BoundingArea < 250:
                    cv2.putText(frame, "Hand is too far from the camera!",
                                (45, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

                # Displays Text if the User's Hand is larger than the Range defined above
                elif self.BoundingArea > 1000:
                    cv2.putText(frame, "Hand is too close to the camera!",
                                (45, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

            _, jpegFrame = cv2.imencode('.jpg', frame)

            # Calculating the fps
            CurrTime = time.time()
            FPS = 1 // (CurrTime - PrevTime)
            PrevTime = CurrTime

            return FPS, center_x1, center_y1, center_x2, center_y2, jpegFrame.tobytes()

        else:
            # Here, we return 0 FPS, 0 for all the coordinates, and None Frame
            return 0, 0, 0, 0, 0, None

    # Method to Close the Webcam Video Feed
    def CloseVideo(self):
        self.CamVideo.release()

    def __del__(self):  # Method to close the Webcam Video Stream
        self.CamVideo.release()


# This function creates a generator for all the video frames
def GenerateFrames(Webcam):
    while True:
        fps, xpos1, ypos1, xpos2, ypos2, singleframe = Webcam.GetFrame()

        if singleframe != None:
            yield fps, xpos1, ypos1, xpos2, ypos2, singleframe

        else:
            break


# Function that updates the Video Frames in the App
@eel.expose
def DisplayVideo():
    global Webcam

    # This if statement acts as a Button Spam Filter
    if Webcam is None:
        # Creating an instance of the OpenWebcam class
        Webcam = OpenWebcam()

        # Calling the GenerateFrames() function
        VideoFrames = GenerateFrames(Webcam)

        for Fps, Xpos1, Ypos1, Xpos2, Ypos2, SingleFrame in VideoFrames:

            # for all the single frames in video frames, we are converting the frames from Bytes to base64 Encoded String.
            frame = base64.b64encode(SingleFrame)
            frame = frame.decode("utf-8")
            eel.UpdateVideoScreen(Fps, Xpos1, Ypos1, Xpos2, Ypos2, frame)()

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
        eel.SetFPSZero()()
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
