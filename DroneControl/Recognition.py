import cv2
import numpy
from time import time
from threading import Thread

class Recognition(object):
    def __init__(self, camera):
        self.timestamp = None
        self.processedImage = None
        self.cam = camera

        self.processThread = Thread(target = self.process)
        self.processThread.start()

    def process(self):
        while self.cam.image is None: pass
        while True:
            processed = self.processImage(self.cam.image)
            if processed is not None:
                self.processedImage = processed
                self.timestamp = time()

    def _sortCorners(self, corners, center):
        top = []
        bot = []
        for i in range(len(corners)):
            #print(corners[i])

            if corners[i][1] < center[1]:
                top.append(corners[i])
            else:
                bot.append(corners[i])

        if len(top) != 2:
            return 0

        if top[0][0] > top[1][0]:
            tr, tl = top
        else:
            tl, tr = top
    
        if bot[0][0] > bot[1][0]:
            br, bl = bot
        else:
            bl, br = bot

        return [tl, tr, br, bl]

    def compareImage(self, img1, img2):
        minDiff = 12000

        diffImg = cv2.bitwise_xor(img1, img2)
        kernal = numpy.ones((5,5),numpy.uint8)
        diffImg = cv2.erode(diffImg, kernal, iterations = 1)
        diff = cv2.countNonZero(diffImg)
        if diff < 12000:
            return None
        else:
            return diff

   


    def processImage(self, img1):       #search for squares in img1, compares content of square with img2
        cv2.imshow('main', img1)
        grayImg = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)                #returns amount of white pixels
    
        grayImg = cv2.GaussianBlur(grayImg, (15,15), 2, 2)

        thresh = cv2.getTrackbarPos("Min Threshold:", "A")

        canny_output = cv2.Canny(grayImg, thresh, thresh *3, 3);

        im2, contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE,\
            cv2.CHAIN_APPROX_SIMPLE)

        for i in range(len(contours)):
            approxRect = cv2.approxPolyDP(contours[i], cv2.arcLength(contours[i], True) * 0.05, True)
            #print(len(approxRect))
            if len(approxRect) == 4:

                area = cv2.contourArea(contours[i])
                if area > 10000:
                    corners = [tuple()]*4
                    for j in range(4):
                        vertex = tuple(approxRect[j][0])
                        corners[j] = vertex

                        vertex = tuple(approxRect[j][0])
                        corners[j] = vertex

                        vertex = tuple(approxRect[j][0])
                        corners[j] = vertex

                        vertex = tuple(approxRect[j][0])
                        corners[j] = vertex

                    mu = cv2.moments(grayImg, False)

                    if mu['m00'] == 0.0:
                        continue
                    corners = self._sortCorners(corners, (mu['m10']/mu['m00'], mu['m01']/mu['m00']))
                    if type(corners) == int:
                        continue

                    dst = numpy.array([(0,0),
                                      (195, 0),
                                      (195, 271),
                                      (0, 271)],
                                      numpy.float32)

                    src = numpy.array(corners, numpy.float32)

                
                    transmtx = cv2.getPerspectiveTransform(src, dst)

                    correctedImg = cv2.warpPerspective(img1, transmtx, (271, 195))

                    correctedImgBin = cv2.cvtColor(correctedImg, cv2.COLOR_RGB2GRAY)
                    new_image = correctedImgBin.copy()

                    correctedImgBin = cv2.threshold(correctedImgBin, 140, 255, 0)

                    min, max = cv2.minMaxLoc(new_image)[:2]
                    medVal = (max-min)//2
                    _, new_image = cv2.threshold(new_image, medVal, 255, 0)

                    return new_image
                    
               