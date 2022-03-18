
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

        #
        logging.error('{}\n{}'.format(ErrorMsg, e.args))

        # Calling the ThrowError Function to display the error message box to the User
        ThrowError(ErrorTitle='Failed to start the local server',
                   ErrorMsg=ErrorMsg)

        # Exiting the Python App
        sys.exit()


if __name__ == '__main__':

    # Calling the Main App Function to Run the App
    GestureVolumeControllerApp()
