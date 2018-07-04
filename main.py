import os
from tkinter import *
from tkinter import messagebox
from ravi import *
from inference import FaceNetModel
from fr_utils import img_to_encoding
import time
from PIL import Image, ImageTk, ImageFilter

class face_recog:

    def __init__(self,master,FRmodel,inf):
        master.title("Face Recognition")
        master.geometry("600x400")
        self.master = master
        # self.create_database()
        self.isOpenDB = False
        self.open_database()
        self.FRmodel = FRmodel

        ### Title Frame ###
        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP,fill=X)

        self.titleLabel = Label(self.titleFrame,bg="red",fg="yellow",text = "Face Recognition Based Attendence System",font=(None, 15, "bold"),padx=5,pady=5,width=400,height=2)
        self.titleLabel.pack(side=TOP,fill=X)


        ### Main Frame ###
        self.mainFrame = Frame(master,height=5,width=400)
        self.mainFrame.pack(fill=X)
        self.firstLabel = Label(self.mainFrame,text="Enter your Roll No",font=(None,10,"italic"),padx=2)
        self.firstLabel.pack(side=LEFT)
        self.entrywidget = Entry(self.mainFrame)
        self.entrywidget.pack(side=LEFT,padx = 2)
        self.entrywidget.insert(0, "like 322CO14")

        ### Registered People ###
        self.secondFrame = Frame(master)
        self.secondFrame.pack()

        self.func()
        '''
        for key,_ in self.database.items():
            #self.secondLabel = Label(self.secondFrame,text = key)
            #self.secondLabel.pack(side=LEFT,padx = 2,pady = 2)
            cwd = os.getcwd()
            dir1 = os.path.join(cwd,"images")
            filepath = str(key)+".png"
            dir2 = os.path.join(dir1,filepath)
            load = Image.open(dir2)
            photo = ImageTk.PhotoImage(load)
            self.photoLabel = Label(self.secondFrame,image=photo,text=key,compound=BOTTOM)
            self.photoLabel.image = photo
            self.photoLabel.pack(side=LEFT,padx=2)

        '''
        ### Submit Frame ###
        self.submitFrame = Frame(master)
        self.submitFrame.pack(side=LEFT,fill=X)

        self.submitBtn = Button(self.submitFrame,text="SUBMIT",command=self.submit)
        self.submitBtn.pack(side=LEFT,padx=2)

        self.addNewFaceBtn = Button(self.submitFrame,text="ADD NEW FACE",command = self.add_new_image)
        self.addNewFaceBtn.pack(side=LEFT ,padx = 2)

        self.updateBtn = Button(self.submitFrame,text="UPDATE",command=self.update_database)
        self.updateBtn.pack(side=LEFT,padx =2)

        self.deleteBtn = Button(self.submitFrame,text="DELETE",command=self.delete_face)
        self.deleteBtn.pack(side=LEFT,padx=2)

        self.recogBtn = Button(self.submitFrame,text='RECOG',command = self.recog)
        self.recogBtn.pack(side=LEFT,padx=2)

        self.refreshBtn = Button(self.submitFrame,text='Refresh',command=self.refresh)
        self.refreshBtn.pack(side=LEFT,padx=2)

        self.exitBtn = Button(self.submitFrame, text = "EXIT" , command = self.exit1)
        self.exitBtn.pack(side = LEFT , padx = 2)





    def func(self):
        for key,_ in self.database.items():
            #self.secondLabel = Label(self.secondFrame,text = key)
            #self.secondLabel.pack(side=LEFT,padx = 2,pady = 2)
            cwd = os.getcwd()
            dir1 = os.path.join(cwd,"images")
            filepath = str(key)+".png"
            dir2 = os.path.join(dir1,filepath)
            load = Image.open(dir2)
            photo = ImageTk.PhotoImage(load)
            self.photoLabel = Label(self.secondFrame,image=photo,text=key,compound=BOTTOM)
            self.photoLabel.image = photo
            self.photoLabel.pack(side=LEFT,padx=2)

    def refresh(self):
        for widget in self.secondFrame.winfo_children():
            widget.destroy()
        self.func()
        
    def recog(self):
        if self.isOpenDB == True:
            self.close_database()
        self.rollno = self.entrywidget.get()

        ob3 = camCapture(root,3,self.rollno,inf)


    def submit(self):
        if self.isOpenDB == False:
            self.open_database()
        self.rollno = self.entrywidget.get()

        ob1 = camCapture(root,1,self.rollno,inf,self.database[self.rollno])

    '''
        score = inf.verify("face.png",self.rollno,self.database,self.FRmodel)
        print("Score:-{}".format(score))
        if score<=0.7:
            messagebox.showinfo("Success","Person Verified is "+str(self.rollno))
        else:
            messagebox.showinfo("Failure","Person is not "+str(self.rollno))
            '''


    def create_database(self):
        self.database = {}
        import pickle

        handle = open("encoding.pickle","wb")
        pickle.dump(self.database,handle,protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()

    def open_database(self):
        import pickle
        handle = open("encoding.pickle","rb")
        self.database = pickle.load(handle)
        self.isOpenDB = True

    def delete_face(self):
        self.rollno = self.entrywidget.get()

        if self.isOpenDB == False:
            open_database()
        del self.database[self.rollno]
        os.remove("images/"+str(self.rollno)+".png")
        for widget in self.secondFrame.winfo_children():
            widget.destroy()
        self.func()

    def update_database(self):
        '''
        update the database
        '''
        self.rollno = self.entrywidget.get()
        self.close_database()
        ob2 = camCapture(root,2,self.rollno,inf)

        for widget in self.secondFrame.winfo_children():
            widget.destroy()
        self.func()

    def close_database(self):
        import pickle
        handle = open("encoding.pickle","wb")
        pickle.dump(self.database,handle,protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()
        self.isOpenDB = False

    def exit1(self):
        if self.isOpenDB == True:
            self.close_database()
        self.master.quit()
        self.master.destroy()

    def add_new_image(self):
        self.rollno = self.entrywidget.get()
        self.close_database()
        ob1 = camCapture(root,0,self.rollno,inf)
        for widget in self.secondFrame.winfo_children():
            widget.destroy()
        self.func()

        '''
        if self.database.get(self.rollno,"") == "":
            self.database[self.rollno] = img_to_encoding("images/"+self.rollno+".png",self.FRmodel)
            messagebox.showinfo("Info","Face added to the database")
        '''





if __name__ == "__main__":
    root = Tk()
    inf = FaceNetModel()
    FRmodel = inf.returnModel()
    obj = face_recog(root,FRmodel,inf)
    root.mainloop()
