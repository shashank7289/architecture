'''
Created on Dec 5, 2016

@author: uid38420
'''
from cv2 import VideoCapture,putText,FONT_HERSHEY_SIMPLEX,imshow,waitKey
from winsound import Beep
from heapq import nlargest
from helper.findFace import findFace
from helper.findLandmarks import faceObj

import numpy as np

class face:
    def __init__(self):
        self.x = 5
        self.leftArr = [0] * self.x
        self.rightArr = [0] * self.x
        self.counter = 0

    def fxn(self,val):
        self.leftArr[(self.counter%self.x)] = val
        self.rightArr[(self.counter%self.x)] = val
        self.counter = self.counter + 1
    
def distance(faceImg,fObj):
    #distance between upper and lower points of left eye
    leftEyeUpper = faceObj.leftEye[1]
    leftEyeLower = faceObj.leftEye[5]
    yDiffLeftEye = leftEyeLower[1] - leftEyeUpper[1]

    #distance between upper and lower points of right eye
    rightEyeUpper = faceObj.rightEye[1]
    rightEyeLower = faceObj.rightEye[5]
    yDiffRightEye = rightEyeLower[1] - rightEyeUpper[1]
    
    fObj.fxn(yDiffLeftEye)
    fObj.fxn(yDiffRightEye)
    speedFactor = 1.45 #detection performance decreases with increasing speed factor
    avgFactor = 1.5 #detection performance increases with reducing speed factor
    
    #condition to reject someone moving with speed
    if ((np.amax(fObj.leftArr, 0) - np.amin(fObj.leftArr, 0)) > (np.amax(fObj.leftArr, 0)/speedFactor)) or (np.amax(fObj.rightArr, 0) - np.amin(fObj.rightArr, 0) > (np.amax(fObj.rightArr, 0)/speedFactor)):
        leftAvg = np.average(nlargest(2,fObj.leftArr))
        rightAvg = np.average(nlargest(2,fObj.rightArr))
        
        #condition to include gradual changes in user position
        if yDiffLeftEye < (leftAvg/avgFactor) or yDiffRightEye < (rightAvg/avgFactor):
            putText(faceImg, 'Blink Detected', (10, 30),FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            Beep(1000, 250) # frequency, duration

def blinkDetection(faceCascade,predictor):

    fObj = face()
    cap = VideoCapture(0)
    
    while True:
        ret,img = cap.read()
        
        #detect face
        faceImg = findFace(img,faceCascade,predictor)
        
        #distance between upper and lower points of eyes
        distance(faceImg,fObj)
                    
        imshow('Blinking Detection',img)
        waitKey(1)