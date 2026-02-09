import cv2
import numpy as np
from hand_tracking import HandTracker

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

tracker = HandTracker()

canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0
eraser_size = 40

def fingers_up(lm):
    fingers = []

    # Thumb (ignored for simplicity)
    fingers.append(0)

    # Index
    fingers.append(1 if lm[8][2] < lm[6][2] else 0)
    # Middle
    fingers.append(1 if lm[12][2] < lm[10][2] else 0)
    # Ring
    fingers.append(1 if lm[16][2] < lm[14][2] else 0)
    # Pinky
    fingers.append(1 if lm[20][2] < lm[18][2] else 0)

    return fingers.count(1)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame = tracker.find_hands(frame)
    landmarks = tracker.get_landmarks(frame)

    if landmarks:
        finger_count = fingers_up(landmarks)
        ix, iy = landmarks[8][1], landmarks[8][2]

        # ✍️ DRAW
        if finger_count == 1:
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = ix, iy
            cv2.line(canvas, (prev_x, prev_y), (ix, iy), (255, 255, 255), 5)
            prev_x, prev_y = ix, iy
            cv2.circle(frame, (ix, iy), 8, (0, 0, 255), cv2.FILLED)

        # ✊ ERASER
        elif finger_count == 0:
            cv2.circle(canvas, (ix, iy), eraser_size, (0, 0, 0), -1)
            cv2.circle(frame, (ix, iy), eraser_size, (255, 0, 0), 2)
            prev_x, prev_y = 0, 0

        # 🖐️ CLEAR BOARD
        elif finger_count == 5:
            canvas[:] = 0
            prev_x, prev_y = 0, 0

        # ❌ STOP DRAWING
        else:
            prev_x, prev_y = 0, 0

    # Merge canvas with frame
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("AirWrite", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
