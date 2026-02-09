import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, detection_conf=0.7, tracking_conf=0.7):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    frame, handLms, self.mpHands.HAND_CONNECTIONS
                )
        return frame

    def get_landmarks(self, frame):
        lm_list = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = frame.shape

            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

        return lm_list
