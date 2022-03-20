<!-- Project Title -->
# ![gesture-volume-controller-app](https://user-images.githubusercontent.com/95453430/159134380-a93ad113-28e9-4210-91cc-86e32f8ca53f.svg)

<!-- Project Images -->
![Gesture Volume Controller App (1)](https://user-images.githubusercontent.com/95453430/159134540-637d129d-fac1-4eb3-8929-2ad446dacebc.png)

<!-- Project Description -->
# ![project-description (9)](https://user-images.githubusercontent.com/95453430/159134386-25693e6a-4ddb-4f26-a035-4915a8c411ac.svg)

This is a **Gesture Volume Controller App** in which the User is able to control to their **Main System Volume** using their **Thumb & Index Fingers Gestures**. The App was made using a **Python Library** called **EEL** used to make **Electron-like GUI Apps**. **HTML, CSS**, were used for the **App Layout & Styling**, and **JavaScript** was used **to implement logic in the frontend and communicate with Python in the backend** . The **Finger Gestures Tracking & Hand Tracking** is achieved through the **Cross-Platform Machine Learning Solutions Library called Mediapipe** loaded using **OpenCV Python** and served through my custom **Hand Tracking Library**. The **User Interface(UI) Prototype** was designed in **Figma**. There are two buttons: **Open Webcam & Close Webcam**, which allow the User to turn on their webcam video feed and use the App or turn it off respectively. Just below the buttons, there is a **Statistics Board** that displays the **Video Frame Rate (FPS)**, the **Center x-axis(XPOS1) & y-axis(YPOS1)** positions of Thumb, and the **Center x-axis(XPOS2) & yaxis(YPOS2)** of the Index Finger. **This project has only been tested in Windows**.

<!-- Project Tech-Stack -->
# ![technologies-used (9)](https://user-images.githubusercontent.com/95453430/159134388-cb04063b-1d27-473e-b5cc-42655699ca10.svg)

![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Python](https://img.shields.io/badge/OpenCV-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Python](https://img.shields.io/badge/tkinter-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Python](https://img.shields.io/badge/Mediapipe-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Python](https://img.shields.io/badge/EEL-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

<!-- How To Use Project -->
# ![how-to-use-project (4)](https://user-images.githubusercontent.com/95453430/159134390-d77c1d1c-61bc-4732-b4e6-094a9d39b48c.svg)

**Install the following Python libraries in your Virtual Environment using PIP**.

*Note: The library names are **CASE-SENSITIVE** for PIP installations below. Make sure your type them correctly.*

*Install OpenCV for Python*
```Python
pip install opencv-python
```

*Install OpenCV Contrib for Python*
```Python
pip install opencv-contrib-python
```

*Install Mediapipe for Python*
```Python
pip install mediapipe
```

*Install EEL for Python*
```Python
pip install eel
```

*Install Numpy for Python*
```Python
pip install numpy
```

*Install PyCaw for Python*
```Python
pip install pycaw
```

Download a copy of this repository onto your local machine and extract it into a suitable folder.
- Create a Virtual Environment in that folder.
- Install all the required Python libraries mentioned above.
- Open a Command Prompt/Terminal in the **Root Directory** of the Project.
- Type the following command in the terminal to start an instance of the EEL App.
```Python
python GestVolContApp.py
```

- Enjoying using the App!
