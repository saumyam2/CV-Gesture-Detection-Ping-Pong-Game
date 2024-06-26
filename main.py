import numpy as np
import cv2 as cv
import cvzone
from cvzone.HandTrackingModule import HandDetector

capture = cv.VideoCapture(0)  
detector = HandDetector(detectionCon=0.8, maxHands=2)

capture.set(3,1280)  # changing the width of the pop-up window
capture.set(4,720)   

background = cv.imread('Resources\Background.png')
ball = cv.imread('Resources\Ball.png', cv.IMREAD_UNCHANGED)
bat1 = cv.imread('Resources\Bat1.png', cv.IMREAD_UNCHANGED)
bat2 = cv.imread('Resources\Bat2.png', cv.IMREAD_UNCHANGED)
gameOver = cv.imread('Resources\GameOver.png')

position = [100,100]
isOver = False
speedX, speedY = 10, 10
score = [0,0]

while True:
    isTrue, frame = capture.read()
    frame = cv.flip(frame, 1)
    # frame = cv.resize(frame, (1280,720))
    hands, frame = detector.findHands(frame, flipType=False)

    frame = cv.addWeighted(frame, 0.5, background, 0.5, 0.0)

    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox'] 
            h1, w1, _ = bat1.shape  
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 415)
            if hand['type'] == 'Left':
                frame = cvzone.overlayPNG(frame, bat1, (59, y1))
                if (59 < position[0] < 59 + w1) and (y1 < position[1] < y1 + h1):
                    speedX = -speedX
                    position[0] += 20
                    score[0] += 1

            if hand['type'] == 'Right':
                frame = cvzone.overlayPNG(frame, bat2, (1195, y1))
                if (1145 < position[0] < 1165) and (y1 < position[1] < y1 + h1):
                    speedX = -speedX
                    position[0] -= 20
                    score[1] += 1

    if position[0] < 40 or position[0] > 1195:
        isOver = True

    if isOver:
        frame = gameOver
        cv.putText(frame, str(score[1] + score[0]).zfill(2), (585, 360), cv.FONT_HERSHEY_COMPLEX,
                   2.5, (200, 0, 200), 5)  
    else:
        if position[1] >= 500 or position[1] <= 10:
            speedY = -speedY

        position[0] += speedX
        position[1] += speedY

        frame = cvzone.overlayPNG(frame, ball, position)

        cv.putText(frame, str(score[0]), (300, 650),
                   cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv.putText(frame, str(score[1]), (900, 650),
                   cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)                

    cv.imshow('Pong game', frame)
    key = cv.waitKey(1)

    if key == ord('r'):
        position = [100, 100]
        speedX = 10
        speedY = 10
        isOver = False
        score = [0, 0]
        gameOver = cv.imread('Resources\GameOver.png')

    if key == ord('q'):
        break