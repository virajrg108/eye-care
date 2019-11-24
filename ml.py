import sys
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy as np
import os
import csv
image = cv2.imread(os.path.join(os.getcwd(),'uploads',sys.argv[1]))
image=cv2.resize(image,(800,615))
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
b,green_fundus,r = cv2.split(image)

green_fundus = cv2.bitwise_not(green_fundus)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(1,1))
contrast_enhanced_green_fundus = clahe.apply(green_fundus)
#c
r1 = cv2.morphologyEx(contrast_enhanced_green_fundus, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(30,30)), iterations = 1)
thresh31 = cv2.adaptiveThreshold(r1,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
R1 = cv2.morphologyEx(r1, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(30,30)), iterations = 1)


f4 = cv2.subtract(contrast_enhanced_green_fundus,r1)

#median = cv2.medianBlur(f4, 5)
median = cv2.medianBlur(f4, 5)


thresh = cv2.threshold(median, 40, 255, cv2.THRESH_BINARY)[1]





f5= cv2.subtract(contrast_enhanced_green_fundus,R1)

(score, diff) = compare_ssim(contrast_enhanced_green_fundus, r1, full=True)
diff = (diff * 255).astype("uint8")
# print("SSIM: {}".format(score))
diff2=cv2.subtract(contrast_enhanced_green_fundus,r1)
h=thresh.shape[0]
w=thresh.shape[1]

count=0
for y in range(0, h):
    for x in range(0, w):
            if thresh[y,x] == 1:
                count=count+1
#thresh = cv2.threshold(diff, 0, 255,
#	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
k=0;
median = cv2.medianBlur(diff2, 5)
h=median.shape[0]
w=median.shape[1]
count=0
for y in range(0, h):
    for x in range(0, w):
            if median[y,x] == 1:
                count=count+1
for c in cnts:
    k=k+1
	# compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
	#(x, y, w, h) = cv2.boundingRect(c)
	#cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 1)
	#cv2.rectangle(r1, (x, y), (x + w, y + h), (0, 0, 255), 1)

#print(k)
#print(count)

# show the output images
#cv2.imshow("Original", image)
#cv2.imshow("Modified", contrast_enhanced_green_fundus)
#cv2.imshow("Diff", f4)
cv2.imwrite(os.path.join(os.getcwd(),'img',"1-"+sys.argv[1]), thresh)
print("1-"+sys.argv[1])
#cv2.imshow("R1", r1)
#cv2.imshow("new thresh", th3)
# cv2.waitKey(0)