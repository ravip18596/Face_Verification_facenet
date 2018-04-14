import cv2
import numpy as np
import os


def image_preprocessing():
	faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	img = cv2.imread("cam.jpg")
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	face = faceCascade.detectMultiScale(gray,1.3,5)
	pad = 5
	if len(face)>0:
		for (x,y,w,h) in face:
		    cv2.imwrite("face.jpg",img[y-pad:y+h+pad, x-pad:x+w+pad])


		img = cv2.imread("face.jpg")
		resize_img = cv2.resize(img,(96,96))
		cv2.imwrite("face.jpg",resize_img)
		return True
	else:
		return False
