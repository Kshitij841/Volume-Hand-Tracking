import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False, maxHands = 2, complexity = 1, detectionConfidence = 0.5, trackConfidence = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img

    def findPosition(self, img, handNo = 0, draw = True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            #checking that bottom is zero..... top is highest
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm) #to print in decimal values
                #height, width, channel
                h, w, c = img.shape
                #multiplying landmark x and y co-ordinates with the hegiht and width decimal to convert them to pixels
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        
        return lmList

def main():
    #For FPS counter
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[0])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 25), cv2.FONT_HERSHEY_PLAIN, 2 ,(255, 0, 255), 3)

        cv2.imshow("image", img)
        cv2.waitKey(1)

if __name__ == "__main__" :
    main()