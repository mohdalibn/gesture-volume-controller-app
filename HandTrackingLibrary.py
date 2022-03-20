
# This is Basic hand tracking library made using the mediapipe framework.

# Packages
import cv2
import mediapipe as mp
import time


class HandTracker():
    def __init__(self, mode=False, MaxHands=2, modelComplexity=1, DetectionConfidence=0.5, TrackingConfidence=0.5):
        self.mode = mode
        self.MaxHands = MaxHands
        self.modelComplex = modelComplexity
        self.DetectionConfidence = DetectionConfidence
        self.TrackingConfidence = TrackingConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode, self.MaxHands, self.modelComplex, self.DetectionConfidence, self.TrackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils

        self.LandmarkList = []  # this list will store all the landmarks position

        # Creating a list of all the finger tip indices
        self.FingerTipIndices = [4, 8, 12, 16, 20]

    def Detect_hands(self, frame, draw=True):

        # Passing the rgb frame to the hand object since it only uses rgb format
        RgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processing our rgb image using the hands object
        self.results = self.hands.process(RgbFrame)

        # executes if there is a detection
        if self.results.multi_hand_landmarks:
            # Checking for multiple hands in the frame
            for HandLandMarks in self.results.multi_hand_landmarks:

                if draw:  # draws the hand connections if the draw flag is set to true
                    self.mpDraw.draw_landmarks(
                        frame, HandLandMarks, self.mpHands.HAND_CONNECTIONS)

        return frame

    def Find_Landmark_Position(self, frame, HandNumber=0, draw=True):

        # executes if there is a detection
        if self.results.multi_hand_landmarks:
            # picks the specified hand's landmark
            ThisHand = self.results.multi_hand_landmarks[HandNumber]

        # id/index corresponding to the landmark
            for id, landmark in enumerate(ThisHand.landmark):
                # the landmark variable stores the ratio of the image. So, we will multiply the image with the width and height to get the pixel locations
                height, width, channels = frame.shape

                # gets the pixel locations of the all the landmarks
                center_x, center_y = int(
                    landmark.x*width), int(landmark.y*height)

                # Appending the landmarks to the landmark's list
                self.LandmarkList.append([id, center_x, center_y])

                if draw:
                    # Drawing a circle in the pixel location of the first landmark
                    if id == 4 or id == 8:
                        cv2.circle(frame, (center_x, center_y),
                                   20, (255, 0, 255), cv2.FILLED)

        return self.LandmarkList

    # This Method returns the list of the fingers that are UP

    def Get_Fingers_Up(self):
        FingersUp = []

        # This statement acts as a fail check when the Landmark List is empty
        if len(self.LandmarkList) != 0:

            if self.LandmarkList[self.FingerTipIndices[0]][1] < self.LandmarkList[self.FingerTipIndices[0] - 1][1]:
                FingersUp.append(1)
            else:
                FingersUp.append(0)

            # We use FingerTipIndices[index] - 2 to get the value 2 indices below the tip.
            for index in range(1, 5):
                if self.LandmarkList[self.FingerTipIndices[index]][2] < self.LandmarkList[self.FingerTipIndices[index] - 2][2]:
                    FingersUp.append(1)
                else:
                    FingersUp.append(0)

            return FingersUp

        else:
            print("No Landmarks Detected! The landmark list is empty.")

            # This returns an empty list
            return []


def HandTracking():

    # Creating the video object and setting the window size
    video = cv2.VideoCapture(0)
    video.set(3, 640)
    video.set(4, 480)

    # Using the Ip Webcam app on the phone for better camera feed
    address = 'http://192.168.2.101:8080/video'
    video.open(address)

    # Variable to store the current time and the previous time
    PrevTime = 0
    CurrTime = 0

    Tracker = HandTracker()  # creating an object of the class

    run = True
    while run:
        success, frame = video.read()
        # calling the function of the class
        frame = Tracker.Detect_hands(frame)

        LndmrkList = Tracker.Find_Landmark_Position(frame)

        # Only executes is the list isn't empty
        # if len(LndmrkList) != 0:
        #     print(LndmrkList[8])

        # Calculationg the frame rate
        CurrTime = time.time()
        Fps = 1/(CurrTime - PrevTime)
        PrevTime = CurrTime

        # Displaying the frame rate
        cv2.putText(frame, "FPS: " + str(int(Fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        frame = cv2.resize(frame, (640, 480))
        cv2.imshow("Image", frame)

        key = cv2.waitKey(1)
        if key == 81 or key == 113:
            run = False
            break


if __name__ == '__main__':
    HandTracking()
