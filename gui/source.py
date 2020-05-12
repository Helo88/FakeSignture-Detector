import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import os

file1=''
file2=''
file3=''
file4=''
file5=''



class Root(tk.Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Fake Signature Detector")
        self.minsize(1100, 500)


        self.filename1 = ''
        self.filename2 = ''
        self.filename3 = ''
        self.filename4 = ''
        self.filename5 = ''
        self.imgLabels= []
        for i in range(0,5):
            self.imgLabels.append(tk.Label(text=''))

        self.labelFrame = tk.LabelFrame(self ,text = "Insert first real signature ")
        self.labelFrame.grid(column = 0, row = 1,padx = 20, pady = 20)
        self.labelFrame2 = tk.LabelFrame(self, text="Insert second real signature ")
        self.labelFrame2.grid(column=3, row=1, padx=20, pady=20)
        self.labelFrame3 = tk.LabelFrame(self, text="Insert third real signature ")
        self.labelFrame3.grid(column=6, row=1, padx=20, pady=20)
        self.labelFrame4 = tk.LabelFrame(self, text="Insert fourth real signature ")
        self.labelFrame4.grid(column=9, row=1, padx=20, pady=20)
        self.labelFrame5 = tk.LabelFrame(self, text="Insert signature TO BE DETECTED ")
        self.labelFrame5.grid(column=12, row=1, padx=20, pady=20)
        self.labelFrame6 = tk.LabelFrame(self, text="")
        self.labelFrame6.grid(column=15, row=1, padx=20, pady=20, columnspan=2)
        self.restartLbl = tk.LabelFrame(self, text="")
        self.restartLbl.grid(column=15, row=2, padx=20, pady=20, columnspan=2)

        self.resultLbl = tk.Button(self, text="", font='Verdana')
        self.resultLbl.grid(row=20)
        self.resultLbl.grid_forget()
        self.button()



    def button(self):
        self.button = tk.Button(self.labelFrame, bg='#FFCCCC', borderwidth=1, fg='Black', text = "Browse A File",command=lambda: self.fileDialog(1))
        self.button.grid(column = 1, row = 1)

        self.button2 = tk.Button(self.labelFrame2,bg='#FFCCCC', borderwidth=1,text="Browse A File",  command=lambda: self.fileDialog(2))
        self.button2.grid(column=4, row=6)

        self.button3 = tk.Button(self.labelFrame3, bg='#FFCCCC', borderwidth=1, text="Browse A File", command=lambda: self.fileDialog(3))
        self.button3.grid(column=7, row=6)

        self.button4 = tk.Button(self.labelFrame4, bg='#FFCCCC', borderwidth=1, text="Browse A File",command=lambda: self.fileDialog(4))
        self.button4.grid(column=10, row=6)

        self.button5 = tk.Button(self.labelFrame5,bg='#CCFFFF',borderwidth=1, text="Browse A File", command=lambda: self.fileDialog(5))
        self.button5.grid(column=13, row=6)

        self.submitBtn = tk.Button(self.labelFrame6, borderwidth=1,text="Submit", command=self.submit)
        self.submitBtn.grid(column=16, row=2, columnspan=3 )

        self.restartBtn = tk.Button(self.restartLbl, borderwidth=1, text="Restart", command=self.restart)
        self.restartBtn.grid(column=16, row=3, columnspan=3)

        #self.resultBtn = tk.Button(self, borderwidth=1, text="Result")
        #self.resultBtn.grid(column=8, row=10, columnspan=3)

        

    def restart(self):
        self.filename1 = ''
        self.filename2 = ''
        self.filename3 = ''
        self.filename4 = ''
        self.filename5 = ''

        for i in range(0,5):
            self.imgLabels[i].config(image='')

        self.resultLbl.config(text="")
        self.resultLbl.grid_forget()




    def fileDialog(self,num):
        self.filename = filedialog.askopenfilename(initialdir = os.getcwd()+'/data', title = "Select A File", filetype =
        (("all files","*.*"),("jpeg files","*.jpg"),("png files", "*.png")) )
        self.label = tk.Label(self.labelFrame, text = "")
        if num == 1:
            colnum=0
            self.filename1=self.filename
            global file1
            file1=self.filename
        elif num == 2:
            colnum = 3
            self.filename2 = self.filename
            global file2
            file2 = self.filename
        elif num == 3:
            colnum = 6
            self.filename3 = self.filename
            global file3
            file3 = self.filename
        elif num == 4:
            colnum = 9
            self.filename4 = self.filename
            global file4
            file4 = self.filename
        elif num == 5:
            colnum = 12
            self.filename5 = self.filename
            global file5
            file5 = self.filename



        img = Image.open(self.filename)
        img = img.resize((150, 150))
        photo = ImageTk.PhotoImage(img)
        self.imgLabels[num-1].config(image=photo)

        self.imgLabels[num-1].image = photo
        self.imgLabels[num-1].grid(column=colnum, row=4)
        #self.label2 = tk.Label(image=photo)
        #self.label2.image = photo
        #self.label2.grid(column=colnum, row=4)







    def match_orb(self,img1, img2, thr):
        orb = cv.ORB_create()
        kp, des = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv.BFMatcher(cv.NORM_HAMMING)
        matches = bf.knnMatch(des, des2, k=2)
        good_points = []
        for m, n in matches:
            if m.distance < thr * n.distance:
                good_points.append(m)
        return len(good_points)

    def match_surf(self,img1, img2, thr):
        surf = cv.xfeatures2d.SURF_create()
        kp1, des1 = surf.detectAndCompute(img1, None)
        kp2, des2 = surf.detectAndCompute(img2, None)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        good_points = []
        for m, n in matches:
            if m.distance < thr * n.distance:
                good_points.append(m)
        return len(good_points)

    def submit(self):
        print("submit")
        self.resultLbl.config(text="")
        self.resultLbl.grid(row=10)
        if (self.filename1=='' or self.filename2=='' or self.filename3=='' or self.filename4==''):
            messagebox.showerror("Error", "Please insert all required images")
            return
        img1 = cv.imread(self.filename1, 0)
        img2 = cv.imread(self.filename2, 0)
        img3 = cv.imread(self.filename3, 0)
        img4 = cv.imread(self.filename4, 0)
        test = cv.imread(self.filename5, 0)

        lst_img = [img1, img2, img3, img4]
        good_orb = []
        good_surf = []
        test_orb = []
        test_surf = []
        i = 0
        th = 0.75
        result_orb = ''
        strength_orb = 0
        result_surf = ''
        strength_surf = 0

        while (i < len(lst_img) - 1):
            j = i + 1
            while (j < len(lst_img)):
                good_orb.append(self.match_orb(lst_img[i], lst_img[j], th))
                good_surf.append(self.match_surf(lst_img[i], lst_img[j], th))
                j += 1
            i += 1
        threshold_orb = sum(good_orb) / len(good_orb)
        threshold_surf = sum(good_surf) / len(good_surf)

        for img in lst_img:
            test_orb.append(self.match_orb(img, test, th))
            test_surf.append(self.match_surf(img, test, th))




        if (max(test_orb) >= threshold_orb):
            result_orb = 'Verified'
            strength_orb = (max(test_orb) - threshold_orb) / threshold_orb
        else:
            result_orb = 'Forged'
            strength_orb = (threshold_orb - max(test_orb)) / threshold_orb

        if (max(test_surf) >= threshold_surf):
            result_surf = 'Verified'
            strength_surf = (max(test_surf) - threshold_surf) / threshold_surf
        else:
            result_surf = 'Forged'
            strength_surf = (threshold_surf - max(test_surf)) / threshold_surf

        if (result_surf == result_orb):
            print(result_surf)
            #self.result= tk.Label(self,text=result_surf)
            #self.result.grid()
            self.resultLbl.config(text=result_surf)
        else:
            if (strength_surf > strength_orb):
                print(result_surf)
                #self.result = tk.Label(self,text=result_orb)
                #self.result.grid()
                self.resultLbl.config(text=result_orb)
            else:
                print(result_orb)
                #self.result = tk.Label(self,text=result_orb, font='Verdana')
                #self.result.grid()
                self.resultLbl.config(text=result_orb)


root = Root()
root.geometry()
root.mainloop()
