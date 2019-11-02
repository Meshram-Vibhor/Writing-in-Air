import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)        ##Set camera resolution
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
Kernal = np.ones((3, 3), np.uint8)
x1 = []                 #List to store x coordinates
y1 = []                 #List to store x coordinates
while(1):
    ret, frame = cap.read()         ##Read image frame
    frame = cv2.flip(frame, +1)     ##Mirror image frame
    if not ret:                     ##If frame is not read then exit
        break
    if cv2.waitKey(1) == ord('s'):  ##While loop exit condition
        break
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)         ##BGR to HSV
    lb = np.array([105, 163, 201])
    ub = np.array([110, 255, 255])

    mask = cv2.inRange(frame2, lb, ub)                      ##Create Mask
    cv2.imshow('Masked Image', mask)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, Kernal)        ##Morphology
    cv2.imshow('Opening', opening)

    res = cv2.bitwise_and(frame, frame, mask = opening)             ##Apply mask on original image
    cv2.imshow('Resuting Image', res)

    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE,      ##Find contours
                                           cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        cnt = contours[0]
        (x, y), radius = cv2.minEnclosingCircle(cnt)                ##Find minimum enclosing circle
        x = int(x)
        y = int(y)
        x1.append(x)
        y1.append(y)

    for i in range(len(x1)):
            cv2.circle(frame, (x1[i], y1[i]), 2, (0, 255, 0), 2)            ##Draw circle
    cv2.imshow('Original Image', frame)

cap.release()                   ##Release memory
cv2.destroyAllWindows()         ##Close all the windows