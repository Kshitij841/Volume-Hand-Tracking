import cv2
import time
import numpy as np
import hand_tracking_module as htm
import math
#pycaw stuff
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
pTime = 0
vol = 0
volBar = 400
volPerc = 0

detector = htm.handDetector(detectionConfidence=0.75)

#USING pycaw TO CONTROL THE VOLUME OF THE SYSTEM https://github.com/AndreMiras/pycaw#

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() #RANGE = (-65.25, 0.0, 0.03125) where 0 is max -65.25 is minimum we don't give a fuck about 0.03125
#######################################################################################
minVol = volRange[0]
maxVol = volRange[1]


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        #Making variables for index x and y co-ordinate
        x1, y1 = lmList[4][1], lmList[4][2]
        #Making variables for index x and y co-ordinate
        x2, y2 = lmList[8][1], lmList[8][2]
        #Finding center of the line we drawing between index finger and the thumb
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        #Finding the length of the line b/w index and thumb
        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        #Hand Range was for me 35 - 225
        #Volume Range -65.25 - 0
        #Making a relation between our index thumb length range and suystem volume range..... M A T H O_o
        vol = np.interp(length, [25, 225], [minVol, maxVol])
        #for the bar to show correctly the volume filled
        volBar = np.interp(length, [25, 225], [400, 150])
        #to show vol percentage
        volPerc = np.interp(length, [25, 225], [0, 100])

        print(int(length), vol)
        #using pycaw here to give the volume to our system :D
        volume.SetMasterVolumeLevel(vol, None)

        if length<35:
            cv2.circle(img, (cx, cy), 7, (0, 255, 255), cv2.FILLED)
        #Making a bar for volume and filling it with...volume
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f"FPS: {int(volPerc)} %", (20, 450), cv2.FONT_HERSHEY_PLAIN, 1, (150, 255, 255), 2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

    cv2.imshow("img", img)
    cv2.waitKey(1)