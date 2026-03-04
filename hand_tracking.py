import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

# Download this model file once:
# https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
MODEL_PATH = "hand_landmarker.task"


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2
    )

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        while True:
            success, frame = cap.read()
            if not success:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            result = landmarker.detect(mp_image)

            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    for landmark in hand_landmarks:
                        h, w, _ = frame.shape
                        cx = int(landmark.x * w)
                        cy = int(landmark.y * h)
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            cTime = time.time()
            fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
            pTime = cTime

            cv2.putText(frame, f'FPS: {int(fps)}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)

            cv2.imshow("Hand Tracking", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()