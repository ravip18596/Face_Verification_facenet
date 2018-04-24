#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
#from faceout import *

import numpy as np
import cv2

from tkinter import messagebox


class camCapture():

    def __init__(self, master,check,rollno,inf=None,stored_encoding=None):

        # self.fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
        self.inf = inf
        self.stored_encoding = stored_encoding
        self.cancel = False
        self.finish = False
        self.rollno = rollno
        self.camIndex = 0
        self.check = check
        self.cap = cv2.VideoCapture(self.camIndex)
        self.capWidth = self.cap.get(3)
        self.capHeight = self.cap.get(4)

        (self.success, self.frame) = self.cap.read()
        if not self.success:
            if self.camIndex == 0:
                print('Error, No webcam found!')
            else:

                # sys.exit(1)

                changeCam(nextCam=0)
                (self.success, self.frame) = self.cap.read()
                if not self.success:
                    print('Error, No webcam found!')

                     # sys.exit(1)

        self.mainWindow = tk.Toplevel(master)
        self.mainWindow.resizable(width=False, height=False)
        self.mainWindow.bind('<Escape>', lambda e: \
                             self.mainWindow.quit())
        self.lmain = tk.Label(self.mainWindow, compound=tk.CENTER,
                              anchor=tk.CENTER, relief=tk.RAISED)
        self.button = tk.Button(self.mainWindow, text='Capture',
                                command=self.prompt_ok)
        self.button_changeCam = tk.Button(self.mainWindow,
                text='Switch Camera', command=self.changeCam)

        self.lmain.pack()
        self.button.place(
            bordermode=tk.INSIDE,
            relx=0.5,
            rely=0.9,
            anchor=tk.CENTER,
            width=300,
            height=50,
            )
        self.button.focus()
        self.button_changeCam.place(
            bordermode=tk.INSIDE,
            relx=0.85,
            rely=0.1,
            anchor=tk.CENTER,
            width=150,
            height=50,
            )
        self.show_frame()

    # Function executes when capture image is clicked

    def getStatus(self):
        '''
        ret : bool
        '''
        return self.finish

    def prompt_ok(self, event=0):

        self.cancel = True

        self.button.place_forget()  # capture button disappers

        # Two new buttons are placed

        self.button1 = tk.Button(self.mainWindow, text='Good Image!',
                                 command=self.saveAndExit)
        self.button2 = tk.Button(self.mainWindow, text='Try Again',
                                 command=self.resume)
        self.button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9,
                           width=150, height=50)
        self.button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9,
                           width=150, height=50)
        self.button1.focus()

        self.show_frame()

    def open_database(self):
        import pickle
        handle = open("encoding.pickle","rb")
        self.database = pickle.load(handle)


    def close_database(self):
        import pickle
        handle = open("encoding.pickle","wb")
        pickle.dump(self.database,handle,protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()

    def image_preprocessing(self):
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        img = cv2.imread("cam.jpg")
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        face = faceCascade.detectMultiScale(gray,1.3,5)
        pad = 5
        if len(face)>0:
            for (x,y,w,h) in face:
                # cv2.imwrite("face.jpg",img[y-pad:y+h+pad, x-pad:x+w+pad])
                face = img[y-pad:y+h+pad, x-pad:x+w+pad]

            # img = cv2.imread("face.jpg")
            resize_img = cv2.resize(face,(96,96))
            if self.check == 1:
                messagebox.showinfo('Sucess', 'Your face has been captured')
                cv2.imwrite("face.jpg",resize_img)
                if self.check ==1 and self.inf is not None:
                    score = self.inf.verify("face.jpg",self.stored_encoding)
                    print("Score:-  {}".format(score))
                    if score<=0.7:
                        messagebox.showinfo("Success","Person Verified is "+str(self.rollno))
                    else:
                        messagebox.showinfo("Failure","Person is not "+str(self.rollno))
                return True
            elif self.check == 0:
                cv2.imwrite("images/"+self.rollno+".jpg",resize_img)
                self.open_database()

                if self.database.get(self.rollno,"") == "":
                    from fr_utils import img_to_encoding
                    FRmodel = self.inf.returnModel()
                    self.database[self.rollno] = img_to_encoding("images/"+self.rollno+".jpg",FRmodel)
                    messagebox.showinfo("Info","Face added to the database")
                    self.close_database()
                else :
                    messagebox.showinfo("Error","Roll No already exists")
                return True
            elif self.check == 2:
                cv2.imwrite("images/"+self.rollno+".jpg",resize_img)
                self.open_database()

                from fr_utils import img_to_encoding
                FRmodel = self.inf.returnModel()
                self.database[self.rollno] = img_to_encoding("images/"+self.rollno+".jpg",FRmodel)
                self.close_database()
                messagebox.showinfo("Success","{} face is updated".format(self.rollno))
                return True

            elif self.check == 3:
                messagebox.showinfo('Sucess', 'Your face has been captured')
                cv2.imwrite("face.jpg",resize_img)
                pr = self.inf.recognize("face.jpg")
                if pr is not None:
                    messagebox.showinfo("Success","The person is {}".format(pr))
                else:
                    messagebox.showinfo("Failure","This person is not in the database")
                return True

        else:
            messagebox.showinfo('Error',
                                'Take another picture with frontal face'
                                )
            return False

    def saveAndExit(self, event=0):

        # self.filepath=tk.filedialog.asksaveasfilename()

        self.filepath = 'cam.jpg'
        #print('Output file to: ' + self.filepath)
        self.prevImg.save(self.filepath)
        if self.image_preprocessing() == True:
            self.finish = True
            self.cap.release()
            self.mainWindow.destroy()


    def resume(self, event=0):

        self.cancel = False

        self.button1.place_forget()
        self.button2.place_forget()

        self.mainWindow.bind('<Return>', self.prompt_ok)
        self.button.place(
            bordermode=tk.INSIDE,
            relx=0.5,
            rely=0.9,
            anchor=tk.CENTER,
            width=300,
            height=50,
            )
        self.lmain.after(10, self.show_frame)

    def changeCam(self, event=0, nextCam=-1):

        if self.nextCam == -1:
            self.camIndex += 1
        else:
            self.camIndex = nextCam
        del self.cap
        self.cap = cv2.VideoCapture(self.camIndex)

        # try to get a frame, if it returns nothing

        (self.success, self.frame) = self.cap.read()
        if not self.success:
            self.camIndex = 0
            del self.cap
            self.cap = cv2.VideoCapture(self.camIndex)

        self.f = open(fileName, 'w')
        self.f.write(str(self.camIndex))
        self.f.close()

    def show_frame(self):
        (_, frame) = self.cap.read()

        # read frame from opencv camera capture

        self.cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # convert opencv image BGR to PIL RGB Image

        self.prevImg = Image.fromarray(self.cv2image)

        # convert PIL Image To Tkinter Image to show in label lmain

        self.imgtk = ImageTk.PhotoImage(image=self.prevImg)

        self.lmain.imgtk = self.imgtk
        self.lmain.configure(image=self.imgtk)
        if not self.cancel:
            self.lmain.after(10, self.show_frame)


    # def getoploc(self):
    #     if self.oploc==True:
    #         return self.prevImg
