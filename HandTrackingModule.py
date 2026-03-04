import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time


class HandTracker:
    def __init__(self, model_path="hand_landmarker.task", num_hands=1):
        self.num_hands = num_hands

        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=self.num_hands,
            running_mode=vision.RunningMode.VIDEO
        )

        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.results = None

    def findHands(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp = int(time.time() * 1000)
        self.results = self.landmarker.detect_for_video(mp_image, timestamp)

        if self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                for landmark in hand_landmarks:
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

        return frame

    def findPosition(self, frame, handNo=0):
        lmList = []

        if self.results and self.results.hand_landmarks:
            if handNo < len(self.results.hand_landmarks):
                hand = self.results.hand_landmarks[handNo]
                h, w, c = frame.shape

                for id, lm in enumerate(hand):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

        return lmList