# Gesture Controlled Mouse

This project allows you to control your mouse cursor using hand gestures captured through your webcam. Leveraging MediaPipe library, it detects your hand movements and translates them into mouse actions using pyautogui. <br>
<br>

**Video Tutorial**

## Features
<b>Real-time Hand Detection:</b> Uses the MediaPipe library for efficient and accurate hand detection in real-time video streams.<br>
<b>Mouse Movement:</b> Control your mouse cursor by moving your hand in front of the camera.<br>
<b>Click Actions:</b> Perform left-click, right-click, and drag-and-drop actions using specific hand gestures.<br>

## Installation
### Clone the repository:

```bash
git clone https://github.com/your_username/HandGestureMouseControl.git
```

### Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Usage
1. Run the main.py script:
```bash
python main.py
```

2. Position your hand in front of the webcam.

3. Perform hand gestures for specific functionality

4. To exit the application, press the Esc key.

### Gestures
#### 1. Mouse Movement
mouse can be moved using index fingers.

![Alt text](https://github.com/jayant1211/GestureControlledMouse/blob/master/results/movement.gif)

#### 2. Left Click

Left click can be triggered by touching index and thumb.

![Alt text](https://github.com/jayant1211/GestureControlledMouse/blob/master/results/left.gif)

#### 3. Right Click

Right click can be triggered by touching thumb and middle finger.

![Alt text](https://github.com/jayant1211/GestureControlledMouse/blob/master/results/right.gif)

#### 4. Hold and Drag

Can be triggered using Three fingers, Index, Middle and Ring.  

![Alt text](https://github.com/jayant1211/GestureControlledMouse/blob/master/results/drag.gif)
