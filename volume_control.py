import cv2
import numpy as np
import math
from ctypes import cast, POINTER

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingModule as htm

# -----------------------------
# Initialize Hand Detector
# -----------------------------
detector = htm.HandTracker()

# -----------------------------
# Initialize Volume Control (Modern Universal Way)
# -----------------------------
# Get default speakers
devices = AudioUtilities.GetSpeakers()

# Get the first audio endpoint (this works on all pycaw versions)
volume = devices.Activate(
    IAudioEndpointVolume._iid_,
    0,  # CLSCTX_ALL = 0 for universal compatibility
    None
)

volume = cast(volume, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# -----------------------------
# Start Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        # Thumb tip = 4, Index tip = 8
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # Draw circles and line
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        # Distance between fingers
        length = math.hypot(x2 - x1, y2 - y1)

        # Map distance to system volume
        vol = np.interp(length, [20, 200], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        # Volume Bar
        volBar = np.interp(length, [20, 200], [400, 150])
        volPercent = np.interp(length, [20, 200], [0, 100])

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPercent)} %', (40, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Show window
    cv2.imshow("Volume Control", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()