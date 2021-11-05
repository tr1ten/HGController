import cv2
import mediapipe as mp
import math
import keyboard
import joystick
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
d_threshold = 140
lr_margin = 5
max_x = 250
min_x = -max_x

def controll_key(x, f, b):
    # print('here x',x)
    joystick.joystick_press(x,smax=max_x,smin=min_x)
    if(f):
        keyboard.press('w')
    else:
        keyboard.release('w')
    press = 1 if b else 0
    joystick.joystick_break(press)


def main():
    forward = False
    backward = False
    left = False
    right = False
    x_start=x_end=0
    slope = 0
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_height, image_width, _ = image.shape
            if results.multi_hand_landmarks:
                print('len ',len(results.multi_hand_landmarks))
                text = ''
                for hand_landmarks in results.multi_hand_landmarks:
                    x_start, y_start = (int(
                        image_width*hand_landmarks.landmark[0].x), int(image_height*hand_landmarks.landmark[0].y))
                    x_end, y_end = (int(image_width*hand_landmarks.landmark[12].x), int(
                        image_height*hand_landmarks.landmark[12].y))
                    image = cv2.line(image, (x_start, y_start),
                                     (x_end, y_end), (0, 0, 0), 9)
                if((x_end-x_start) != 0):
                    slope = (y_end-y_start)/(x_end-x_start)
                distance = math.dist([x_start, y_start], [x_end, y_end])
                if(distance > d_threshold):
                    text = 'Forward'
                    forward = True
                    backward = False
                else:
                    text = 'Backward'
                    backward = True
                    forward = False
                if(slope < 0 and slope > -1*lr_margin):
                    text += ' | Left'
                    right = False
                    left = True
                elif (slope > 0 and slope < lr_margin):
                    text += ' | Right'
                    right = True
                    left = False
                else:
                    text += ' | Straight'
                    right = left = False
                # print(f'\r slope : {slope} distance:{distance}')
            else:
                text = 'Not detected'
                right = left = forward = backward = False
            controll_key(x_start-x_end, forward, backward)
            # Flip the image horizontally for a selfie-view display.
            image = cv2.putText(cv2.flip(image, 1), text, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 0), 2, cv2.LINE_AA, False)
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    cap.release()


if __name__ == "__main__":
    main()
