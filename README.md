# OpenCV_Projects

## Project 1: Hand Tracking

### Overview
Real-time hand detection and tracking using **MediaPipe** and **OpenCV**.  
Tracks hand landmarks for applications like gesture recognition.

### Features
- Detects hands and tracks landmarks.
- Provides real-time visual feedback on hand position.
- Can be extended for gesture recognition.

### How to Run

1. Navigate to the project folder:
```bash
cd OpenCV_Projects
```
2. Run the script:
```bash
python hand_tracking.py
```
3. Make sure your webcam is active.
4. Move your hand within the frame to see real-time hand detection and tracking.

## Project 2: Volume Control using OpenCV

### Overview

Control system volume using hand gestures detected via webcam.
Distance between thumb and index finger is mapped to volume percentage.

### Features

- Detects hand landmarks and calculates finger distance.
- Controls system volume in real-time (Windows using pycaw).
- Shows visual volume bar and percentage.

### How to Use

1. Navigate to the volume control folder:
```bash
cd OpenCV_Projects
```
2. Run the script:
```bash
python volume_control.py
```
3. Place your hand in front of the webcam.
4. Move your thumb and index finger closer or further apart to adjust volume.

### Requirements

1. Python 3.7+
2. Libraries:
- opencv-python
- mediapipe
- numpy
- pycaw (Windows only)
- comtypes

### Install all dependencies using:
```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install comtypes
pip install pycaw==20220416
```

