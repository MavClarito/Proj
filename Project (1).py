import cv2
import mediapipe as mp
import pyautogui

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

THUMB_TIP = 4
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16

Z_THRESHOLD_PRESS = -200

# Define the basic keyboard layout
VK = {
    '1': {'x': 25, 'y': 100, 'w': 100, 'h': 100},
    '2': {'x': 125, 'y': 100, 'w': 100, 'h': 100},
    '3': {'x': 225, 'y': 100, 'w': 100, 'h': 100},
    '4': {'x': 325, 'y': 100, 'w': 100, 'h': 100},
    '5': {'x': 425, 'y': 100, 'w': 100, 'h': 100},
    '6': {'x': 525, 'y': 100, 'w': 100, 'h': 100},
    '7': {'x': 625, 'y': 100, 'w': 100, 'h': 100},
    '8': {'x': 725, 'y': 100, 'w': 100, 'h': 100},
    '9': {'x': 825, 'y': 100, 'w': 100, 'h': 100},
    '0': {'x': 925, 'y': 100, 'w': 100, 'h': 100},
    '-': {'x': 1025, 'y': 100, 'w': 100, 'h': 100},
    '=': {'x': 1125, 'y': 100, 'w': 100, 'h': 100},
    'Q': {'x': 70, 'y': 250, 'w': 100, 'h': 100},
    'W': {'x': 170, 'y': 250, 'w': 100, 'h': 100},
    'E': {'x': 270, 'y': 250, 'w': 100, 'h': 100},
    'R': {'x': 370, 'y': 250, 'w': 100, 'h': 100},
    'T': {'x': 470, 'y': 250, 'w': 100, 'h': 100},
    'Y': {'x': 570, 'y': 250, 'w': 100, 'h': 100},
    'U': {'x': 670, 'y': 250, 'w': 100, 'h': 100},
    'I': {'x': 770, 'y': 250, 'w': 100, 'h': 100},
    'O': {'x': 870, 'y': 250, 'w': 100, 'h': 100},
    'P': {'x': 970, 'y': 250, 'w': 100, 'h': 100},
    '[': {'x': 1070, 'y': 250, 'w': 100, 'h': 100},
    ']': {'x': 1170, 'y': 250, 'w': 100, 'h': 100},
    'A': {'x': 120, 'y': 400, 'w': 100, 'h': 100},
    'S': {'x': 220, 'y': 400, 'w': 100, 'h': 100},
    'D': {'x': 320, 'y': 400, 'w': 100, 'h': 100},
    'F': {'x': 420, 'y': 400, 'w': 100, 'h': 100},
    'G': {'x': 520, 'y': 400, 'w': 100, 'h': 100},
    'H': {'x': 620, 'y': 400, 'w': 100, 'h': 100},
    'J': {'x': 720, 'y': 400, 'w': 100, 'h': 100},
    'K': {'x': 820, 'y': 400, 'w': 100, 'h': 100},
    'L': {'x': 920, 'y': 400, 'w': 100, 'h': 100},
    ';': {'x': 1020, 'y': 400, 'w': 100, 'h': 100},
    '\'': {'x': 1120, 'y': 400, 'w': 100, 'h': 100},
    'Z': {'x': 170, 'y': 550, 'w': 100, 'h': 100},
    'X': {'x': 270, 'y': 550, 'w': 100, 'h': 100},
    'C': {'x': 370, 'y': 550, 'w': 100, 'h': 100},
    'V': {'x': 470, 'y': 550, 'w': 100, 'h': 100},
    'B': {'x': 570, 'y': 550, 'w': 100, 'h': 100},
    'N': {'x': 670, 'y': 550, 'w': 100, 'h': 100},
    'M': {'x': 770, 'y': 550, 'w': 100, 'h': 100},
    ',': {'x': 870, 'y': 550, 'w': 100, 'h': 100},
    '.': {'x': 970, 'y': 550, 'w': 100, 'h': 100},
    '/': {'x': 1070, 'y': 550, 'w': 100, 'h': 100},
    'SPACE': {'x': 1170, 'y': 400, 'w': 150, 'h': 100},  # Added 'Space' key
}

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Initialize a set to keep track of pressed keys
pressed_keys = set()

def draw_keys(img, x, y, z):
    global pressed_keys
    for k in VK:
        if ((VK[k]['x'] < x < VK[k]['x'] + VK[k]['w']) and (VK[k]['y'] < y < VK[k]['y'] + VK[k]['h']) and (
                z <= Z_THRESHOLD_PRESS)):
            cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x'] + VK[k]['w'], VK[k]['y'] + VK[k]['h']),
                          (0, 0, 255), -1)  # thickness -1 means filled rectangle
            cv2.putText(img, f"{k}", (VK[k]['x'] + 30, VK[k]['y'] + 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5,
                        cv2.LINE_AA)
            pressed_keys.add(k)  # Add the key to the set
        else:
            cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x'] + VK[k]['w'], VK[k]['y'] + VK[k]['h']),
                          (0, 255, 0), 1)  # thickness -1 means filled rectangle
            cv2.putText(img, f"{k}", (VK[k]['x'] + 30, VK[k]['y'] + 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5,
                        cv2.LINE_AA)

def type_keys():
    global pressed_keys
    if pressed_keys:
        try:
            typed_string = ''.join(pressed_keys)
            pyautogui.write(typed_string)
        except Exception as e:
            print(f"Error typing: {e}")
        finally:
            pressed_keys.clear()  # Clear the pressed keys after typing

def main():
    global pressed_keys
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        success, img = cap.read()

        if not success:
            print("Failed to capture frame")
            break

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        x = 0
        y = 0
        z = 0

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                try:
                    index_finger_tip = handLms.landmark[INDEX_FINGER_TIP]
                    x = int(index_finger_tip.x * FRAME_WIDTH)
                    y = int(index_finger_tip.y * FRAME_HEIGHT)
                    z = int(index_finger_tip.z * FRAME_WIDTH)
                    if (z <= Z_THRESHOLD_PRESS):
                        color = (100, 0, 0)  # BGR
                    else:
                        color = (0, 255, 0)
                    cv2.putText(img, f"{x}, {y}, {z}", (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1,
                                cv2.LINE_AA)
                except IndexError:
                    index_finger_tip = None

        draw_keys(img, x, y, z)
        type_keys()  # Type the keys pressed
        cv2.imshow("OpenCV Video Capture", img)

        # Check for key press events
        key = cv2.waitKey(1)
        if key & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()