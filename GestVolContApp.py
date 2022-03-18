
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


if __name__ == '__main__':

    # Initializing the eel App
    eel.init("web")

    # Starting the eel App with index.html file and the window size
    eel.start('index.html', size=(1015, 750), options={
              'chromeFlags': ['--disable-http-cache']}, suppress_error=True)
