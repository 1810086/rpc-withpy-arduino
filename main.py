import cv2
import mediapipe as mp
import math
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import emoji
import random
import time
import serial
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hand_mpDraw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_spec_dots = mp_drawing.DrawingSpec(color = (201,194,2),thickness=1, circle_radius=2)
drawing_spec_line = mp_drawing.DrawingSpec(color = (255,255,255),thickness=2, circle_radius=1)
options = ['Rock', 'paper', 'scissors']
NewValue = 0
last_pos = "None"
ans = "None"
tipIds = [4, 8, 12, 16, 20]
rock = [0,0,0,0,0]
paper = [1,1,1,1,1]
scissors = [0,1,1,0,0]
#arduino = serial.Serial("COM3", 9600, timeout=1)
p = 0

FONT_SIZE = 3
FONT_THICKNESS = 3

def get_gesture(lmList):
    fingers = []
    if lmList[tipIds[0]][2] < lmList[tipIds[0] - 1][2]:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers
    for id in range(1, 5):
        if lmList[tipIds[id]][1] > lmList[tipIds[id] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    if fingers == rock:
        return "Rock"
    elif fingers == paper:
        return "paper"
    elif fingers == scissors:
        return "scissors"



def puttext(user_action,computer_action):
    if user_action == computer_action:
        return ("It's a tie!")
    elif user_action == "Rock":
        if computer_action == "scissors":
            return ("You win!")
        else:
            return ("You lose.")
    elif user_action == "paper":
        if computer_action == "Rock":
            return ("You win!")
        else:
            return ("You lose.")
    elif user_action == "scissors":
        if computer_action == "paper":
            return ("You win!")
        else:
            return ("You lose.")

def motor():
    global options, last_pos
    cap = cv2.VideoCapture(0)
    i = 0
    booler = False
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    lmList = []
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                    res = get_gesture(lmList)
                    if res != last_pos:
                        p = random.randint(0, len(options) - 1)
                        ans = options[p]
                        # if p == 0:
                        #     arduino.write(b'1')
                        # if p == 1:
                        #     arduino.write(b'2')
                        # if p == 2:
                        #     arduino.write(b'3')
                        last_pos = res
                    cv2.putText(image, ("You: "+ str(res)), (5, 100), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (0, 0, 0), FONT_THICKNESS+2)
                    cv2.putText(image, ("You: "+ str(res)), (5, 100), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 255, 255),FONT_THICKNESS)
                    cv2.putText(image, ("CPU: "+ str(ans)), (300, 200), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (0, 0, 0), FONT_THICKNESS+2)
                    cv2.putText(image, ("CPU: "+ str(ans)), (300, 200), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 255),FONT_THICKNESS)
                    cv2.putText(image, str(puttext(res,ans)), (100, 400), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (0, 0, 0), FONT_THICKNESS+2)
                    cv2.putText(image, str(puttext(res, ans)), (100, 400), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE,(255, 0, 255), FONT_THICKNESS)
            cv2.imshow('MediaPipe Hands', image)
            if (cv2.waitKey(5) & 0xFF == 27):
                break
        cap.release()
        cv2.destroyAllWindows()
motor()