
# This project was initially used with Ip Webcam as the video source. Later, it was moved to IvCam and so the code has been sligthy altered. (Mostly the drawings of lines and rectanges and fonts etc.)

# Library Imports
import cv2
import mediapipe as mp
import time
import numpy as np
import math
import HandTrackingLibrary as Htl

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

# volume.GetMute()
# volume.GetMasterVolumeLevel()
VolumeRange = volume.GetVolumeRange()


# Storing the min and max volume levels
MinVolume = VolumeRange[0]
MaxVolume = VolumeRange[1]


video = cv2.VideoCapture(0)
video.set(3, 640)
video.set(4, 480)

# Using the Ip Webcam app on the phone for better camera feed
# address = 'http://192.168.2.101:8080/video'
# video.open(addres)

# Variables to store the current time and the previous time
CurrTime = 0
PrevTime = 0

# Creating an object from the Hand Tracking class with a detection confidence of 70%
Tracker = Htl.HandTracker(DetectionConfidence=0.7)

Volume = 0  # This is the initial declaration of the variable to avoid the error of not being defined

BarVolume = 400  # Set to 900 according to the drawing in the code down below

VolumePercentage = 0

# Variable to store the Bounding Box Area
BoundingArea = 0

run = True
while run:
    success, frame = video.read()

    # Detecting the presence of a hand
    frame = Tracker.Detect_hands(frame)

    # Storing all the landmark positions of all the hand in a list and the bounding box coordinates
    LndmrkList, BndBox = Tracker.Find_Landmark_Position(frame, draw=True)

    if len(LndmrkList) != 0:
        # the landmark indices of the thumb and the index finger are 4, 8 respectively
        #print(LndmrkList[4], LndmrkList[8])

        # Normalizing the size of the hand to maintain a uniform calculation of the line length at different hand distance from the camera
        BndBoxWidth = BndBox[2] - BndBox[0]
        BndBoxHeight = BndBox[3] - BndBox[1]
        # Calculating the Area
        BoundingArea = (BndBoxWidth * BndBoxHeight) // 100
        print(BoundingArea)

        if BoundingArea > 150 and BoundingArea < 1000:

            frame, LineLength, CenterList = Tracker.Get_Finger_Distance(
                frame, 4, 8, draw=True)

            LineCenter_x = CenterList[4]
            LineCenter_y = CenterList[5]

            # In my case, the avg minimum distance between the fingers was 24 and the avg maximum was 165

            # Coverting the line length range into the volume range using numpy
            # Volume = np.interp(LineLength, [24, 165], [MinVolume, MaxVolume])
            # print(Volume) # printing the volume level

            # This Volume convertion is for the bar so that it doesn't draw off the screen
            BarVolume = np.interp(LineLength, [24, 165], [400, 150])

            # This volume convertion is for the percentage displays
            VolumePercentage = np.interp(LineLength, [24, 165], [0, 100])

            # A constant increment volume value by "X" to smooth the volume increasing and decreasing experience.
            VolSmoothness = 5
            VolumePercentage = round(
                VolumePercentage / VolSmoothness) * VolSmoothness

            # Sending the level of the volume to control it
            volume.SetMasterVolumeLevelScalar(VolumePercentage / 100, None)

            if LineLength < 24:
                # Changing the color to green when the length is less than 60
                cv2.circle(frame, (LineCenter_x, LineCenter_y),
                           8, (0, 255, 0), cv2.FILLED)

    # CODE FOR DISPLAYING A VOLUME LEVEL BAR ON THE SCREEN BELOW

    # This line draws the rectangular frame for the volume bar
    cv2.rectangle(frame, (50, 150), (85, 400), (0, 0, 255), 2)

    # This line fills the rectangular bar according to the volume
    cv2.rectangle(frame, (50, int(BarVolume)),
                  (85, 400), (0, 0, 255), cv2.FILLED)

    # Displaying the percentage on the screen
    cv2.putText(frame, "Vol: " + str(int(VolumePercentage)) + "%",
                (40, 440), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # Calculating the fps
    CurrTime = time.time()
    Fps = 1/(CurrTime - PrevTime)
    PrevTime = CurrTime

    # Displaying the frame rate
    cv2.putText(frame, "FPS: " + str(int(Fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("VolumeController", frame)

    key = cv2.waitKey(1)
    if key == 81 or key == 113:
        run = False
        break
