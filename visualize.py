###

import tkinter as tk
from tkinter import filedialog
import glob
import cv2
from PIL import Image, ImageTk
from paddlex.cls import transforms
import numpy as np
import os

width = 1280
height = 768

MW = tk.Tk()
MW.title('View Transform')
MW.geometry(str(width)+'x'+str(height))

ImagePath = None
CurrentIndex = 0

frame_l = tk.Frame(MW)
frame_l.place(x = 0, y = 0, anchor = 'nw')
frame_r = tk.Frame(MW)
frame_r.place(x = round(width*0.25), y = 0, anchor = 'nw')

var = tk.StringVar()
limg = tk.Label(frame_l, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
limg.pack()

LbImage = tk.Label(frame_r)
LbImage.pack()

globalimg = None
originimg = None
transimg = None
State = True
StateName = tk.StringVar() 
StateName.set('Origin')

def preimg(path):
    global globalimg
    global originimg
    tmpimg = cv2.imread(path)
    ss = tmpimg.shape
    xx = ss[0] / height
    yy = ss[1] / round(width * 0.75)
    #print(ss, xx, yy)
    if (ss[1] / xx) > round(width * 0.75):
        ss = (round(ss[1] / yy), height)
    else:
        ss= (round(width * 0.75), round(ss[0] / xx))
    #print(ss)
    tmpimg = cv2.resize(tmpimg,ss,interpolation=cv2.INTER_CUBIC) 
    globalimg = tmpimg.copy()
    cv2image = cv2.cvtColor(tmpimg, cv2.COLOR_BGR2RGBA)
    originimg = Image.fromarray(cv2image)
    
def draw_img(Imageimg):
    imgtk = ImageTk.PhotoImage(image=Imageimg)
    LbImage.imgtk = imgtk
    LbImage.config(image=imgtk)

def postimg():
    global globalimg
    global transimg
    #if BchangeState:
    timg = globalimg.astype(np.float32) / 255
    resimg = (AllCompose.__call__(timg)[0] * 255).astype('uint8')
    #BchangeState = False
    transimg = Image.fromarray(resimg)

def CBBtnSelectImgPath():
    global ImagePath
    SelectImgPath = filedialog.askdirectory()
    ImagePath = glob.glob(SelectImgPath + "/*.jpg")
    if ImagePath is not None and len(ImagePath) > 0:
        var.set(os.path.basename(ImagePath[CurrentIndex]))
        preimg(ImagePath[CurrentIndex])
        draw_img(originimg)
BtnSelectImgPath = tk.Button(frame_l, text='Select File Folder', font=('Arial', 12), width=20, height=2, command=CBBtnSelectImgPath)
BtnSelectImgPath.pack()

Brightness = 0.01
Contrastness = 0.01
Saturation = 0.01
Hue = 0
AllCompose = None
BchangeState = False

def CBGetNewCompose():
    global AllCompose
    global BchangeState
    BchangeState = True
    AllCompose = transforms.Compose([transforms.RandomDistort(brightness_range=Brightness, brightness_prob=1, contrast_range=Contrastness, contrast_prob=1, saturation_range=Saturation, saturation_prob=1, hue_range=Hue, hue_prob=1)])
    if globalimg is not None:
        if State is False:
            postimg()
            draw_img(transimg)
BtnFresh = tk.Button(frame_l, text='Refresh', font=('Arial', 12), width=20, height=2, command=CBGetNewCompose)
BtnFresh.pack()

## bright
varBright = tk.StringVar()
def CBBright(v):
    global Brightness
    Brightness = float(v)
    varBright.set("Brightness: "+v)
    CBGetNewCompose()
CBBright("0")
LBright = tk.Label(frame_l, textvariable=varBright, fg='black', font=('Arial', 12), width=30, height=2)
ScBrightRange = tk.Scale(frame_l, label="Brightness Range", from_=0, to=1, orient=tk.HORIZONTAL, length=250, showvalue=0.01,tickinterval=0.1, resolution=0.01, command=CBBright)
LBright.pack()
ScBrightRange.pack()

## constrast
varContrast = tk.StringVar()
def CBContrast(v):
    global Contrastness
    Contrastness = float(v)
    varContrast.set("Contrast: "+v)
    CBGetNewCompose()
CBContrast("0")
LContrast = tk.Label(frame_l, textvariable=varContrast, fg='black', font=('Arial', 12), width=30, height=2)
ScContrastRange = tk.Scale(frame_l, label="Contrast Range", from_=0, to=1, orient=tk.HORIZONTAL, length=250, showvalue=0.01,tickinterval=0.1, resolution=0.01, command=CBContrast)
LContrast.pack()
ScContrastRange.pack()

## Saturation
varSaturation = tk.StringVar()
def CBSaturation(v):
    global Saturation
    Saturation = float(v)
    varSaturation.set("Saturation: "+v)
    CBGetNewCompose()
CBSaturation("0")
LSaturation = tk.Label(frame_l, textvariable=varSaturation, fg='black', font=('Arial', 12), width=30, height=2)
ScSaturationRange = tk.Scale(frame_l, label="Saturation Range", from_=0, to=1, orient=tk.HORIZONTAL, length=250, showvalue=0.01,tickinterval=0.1, resolution=0.01, command=CBSaturation)
LSaturation.pack()
ScSaturationRange.pack()

## Hue
varHue = tk.StringVar()
def CBHue(v):
    global Hue
    Hue = int(v)
    varHue.set("Hue: "+v)
    CBGetNewCompose()
CBHue("0")
LHue = tk.Label(frame_l, textvariable=varHue, fg='black', font=('Arial', 12), width=30, height=2)
ScHueRange = tk.Scale(frame_l, label="Hue Range", from_=0, to=18, orient=tk.HORIZONTAL, length=250, showvalue=0,tickinterval=1, resolution=1, command=CBHue)
LHue.pack()
ScHueRange.pack()

## Last
def CBBtnLast():
    global CurrentIndex
    global BchangeState
    if ImagePath is not None:
        CurrentIndex = (CurrentIndex - 1) % len(ImagePath)
    BchangeState = True
    var.set(os.path.basename(ImagePath[CurrentIndex]))
    if State:
        preimg(ImagePath[CurrentIndex])
        draw_img(originimg)
    else:
        preimg(ImagePath[CurrentIndex])
        postimg()
        draw_img(transimg)
BtnLast = tk.Button(frame_l, text='Prev', font=('Arial', 12), width=20, height=2, command=CBBtnLast)
BtnLast.pack(side='bottom')


## next
def CBBtnNext():
    global CurrentIndex
    global BchangeState
    if ImagePath is not None:
        CurrentIndex = (CurrentIndex + 1) % len(ImagePath)
    BchangeState = True
    var.set(os.path.basename(ImagePath[CurrentIndex]))
    if State:
        preimg(ImagePath[CurrentIndex])
        draw_img(originimg)
    else:
        preimg(ImagePath[CurrentIndex])
        postimg()
        draw_img(transimg)
BtnNext = tk.Button(frame_l, text='Next', font=('Arial', 12), width=20, height=2, command=CBBtnNext)
BtnNext.pack(side='bottom')



def CBBtnChangeState():
    global State
    global StateName
    if State == False:
        State = True
        StateName.set('Origin')
        if originimg is None:
            preimg()
        draw_img(originimg)
    else:
        State = False
        StateName.set('Transformed')
        postimg()
        draw_img(transimg)
BtnChangeState = tk.Button(frame_l, textvariable=StateName, font=('Arial', 12), width=20, height=2, command=CBBtnChangeState)
BtnChangeState.pack()

CBGetNewCompose()

MW.mainloop()

cv2.destroyAllWindows()