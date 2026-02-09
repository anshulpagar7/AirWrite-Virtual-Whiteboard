import cv2
import numpy as np
import time
import os
from datetime import datetime
from hand_tracking import HandTracker

# ================== CAMERA SETUP ==================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("AirWrite", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AirWrite", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

tracker = HandTracker()

# ================== SAVE FOLDER ==================
SAVE_DIR = "saved_drawings"
os.makedirs(SAVE_DIR, exist_ok=True)

# ================== CANVAS ==================
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

# ================== DRAW STATE ==================
prev_x, prev_y = 0, 0
draw_color = (255, 255, 255)
color_name = "WHITE"

brush_thickness = 10
min_thickness = 5
max_thickness = 40
eraser_size = 50

thickness_cooldown = 0
current_mode = ""

# ================== UNDO / REDO ==================
undo_stack = []
redo_stack = []
MAX_HISTORY = 15

def save_state():
    undo_stack.append(canvas.copy())
    if len(undo_stack) > MAX_HISTORY:
        undo_stack.pop(0)
    redo_stack.clear()

# ================== TOAST SYSTEM ==================
toast_text = ""
toast_color = (255, 255, 255)
toast_time = 0
TOAST_DURATION = 2.5

def show_toast(text, color=(255, 255, 255)):
    global toast_text, toast_color, toast_time
    toast_text = text
    toast_color = color
    toast_time = time.time()

# ================== UTIL ==================
def fingers_up(lm):
    return sum([
        lm[8][2] < lm[6][2],    # index
        lm[12][2] < lm[10][2],  # middle
        lm[16][2] < lm[14][2],  # ring
        lm[20][2] < lm[18][2]   # pinky
    ])

# ================== MAIN LOOP ==================
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = tracker.find_hands(frame)
    landmarks = tracker.get_landmarks(frame)

    if landmarks:
        ix, iy = landmarks[8][1], landmarks[8][2]
        count = fingers_up(landmarks)

        index_up  = landmarks[8][2]  < landmarks[6][2]
        middle_up = landmarks[12][2] < landmarks[10][2]
        ring_up   = landmarks[16][2] < landmarks[14][2]
        pinky_up  = landmarks[20][2] < landmarks[18][2]

        rock = index_up and pinky_up and not middle_up and not ring_up

        # ✍️ PEN
        if count == 1:
            if current_mode != "PEN":
                save_state()
                show_toast("✍️ Mode: PEN", draw_color)
                current_mode = "PEN"

            if prev_x == 0:
                prev_x, prev_y = ix, iy

            cv2.line(canvas, (prev_x, prev_y), (ix, iy),
                     draw_color, brush_thickness)
            prev_x, prev_y = ix, iy
            cv2.circle(frame, (ix, iy), 6, draw_color, cv2.FILLED)

        # 🎨 COLOR CHANGE
        elif count == 3:
            prev_x, prev_y = 0, 0

            if ix < 426:
                draw_color = (0, 0, 255)
                color_name = "RED"
            elif ix < 852:
                draw_color = (0, 255, 0)
                color_name = "GREEN"
            else:
                draw_color = (255, 0, 0)
                color_name = "BLUE"

            show_toast(f"🎨 Color: {color_name}", draw_color)
            current_mode = "COLOR"

        # 🧽 ERASER
        elif count == 0:
            if current_mode != "ERASER":
                save_state()
                show_toast("🧽 Mode: ERASER", (200, 200, 200))
                current_mode = "ERASER"

            cv2.circle(canvas, (ix, iy), eraser_size, (0, 0, 0), -1)
            cv2.circle(frame, (ix, iy), eraser_size, (200, 200, 200), 2)
            prev_x, prev_y = 0, 0

        # 📏 THICKNESS (🤟)
        elif rock:
            if thickness_cooldown == 0:
                if iy < 360:
                    brush_thickness = min(max_thickness, brush_thickness + 2)
                else:
                    brush_thickness = max(min_thickness, brush_thickness - 2)

                show_toast(f"📏 Size: {brush_thickness}", draw_color)
                thickness_cooldown = 8

            current_mode = "SIZE"
            prev_x, prev_y = 0, 0

        else:
            prev_x, prev_y = 0, 0

    if thickness_cooldown > 0:
        thickness_cooldown -= 1

    # ================== MERGE CANVAS ==================
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    # ================== UI ==================
    # Title
    cv2.putText(frame, "AirWrite", (520, 60),
                cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 0, 0), 6)
    cv2.putText(frame, "AirWrite", (520, 60),
                cv2.FONT_HERSHEY_DUPLEX, 1.6, (255, 255, 255), 2)

    # Thickness Sidebar
    bar_x = 1220
    bar_top, bar_bottom = 140, 600

    cv2.rectangle(frame, (bar_x, bar_top),
                  (bar_x + 18, bar_bottom), (70, 70, 70), -1)

    fill_height = int((brush_thickness / max_thickness)
                      * (bar_bottom - bar_top))

    cv2.rectangle(frame,
                  (bar_x, bar_bottom - fill_height),
                  (bar_x + 18, bar_bottom),
                  draw_color, -1)

    cv2.putText(frame, "Size", (1195, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

    # Toast
    if time.time() - toast_time < TOAST_DURATION:
        cv2.putText(frame, toast_text, (520, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    toast_color, 3)

    cv2.imshow("AirWrite", frame)

    # ================== KEYS ==================
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('c'):
        save_state()
        canvas[:] = 0
        show_toast("🧼 Canvas Cleared")

    elif key == ord('s'):
        filename = f"{SAVE_DIR}/airwrite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(filename, canvas)
        show_toast("💾 Drawing Saved", (0, 255, 0))

    elif key == ord('z') and undo_stack:
        redo_stack.append(canvas.copy())
        canvas = undo_stack.pop()
        show_toast("↩️ Undo")

    elif key == ord('y') and redo_stack:
        undo_stack.append(canvas.copy())
        canvas = redo_stack.pop()
        show_toast("↪️ Redo")

cap.release()
cv2.destroyAllWindows()
