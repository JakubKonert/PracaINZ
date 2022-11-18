import cv2
import PIL
from PIL import ImageTk
import tkinter
import tkinter.messagebox
import psutil
import io
from zipfile import ZipFile
import datetime
import numpy as np


def GetImage(framesQueue):
    image = None

    if not framesQueue.empty():
        image = framesQueue.get()
    return image


def PreviewImage(labelFrame, framesQueue, switchPreview, imageDefault):
    if switchPreview.check_state:
        image = GetImage(framesQueue)
        if image is not None:
            image = PIL.Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=image)
            labelFrame.imgtk = imgtk
            labelFrame.configure(image=imgtk)
    else:
        image = PIL.Image.fromarray(imageDefault)
        imgtk = ImageTk.PhotoImage(image=image)
        labelFrame.imgtk = imgtk
        labelFrame.configure(image=imgtk)
    labelFrame.after(40, lambda: PreviewImage(
        labelFrame, framesQueue, switchPreview, imageDefault))


def GetUsageOfDisk():
    #disk = psutil.disk_usage('/')
    disk = psutil.disk_usage('/media/INZ')
    return disk


def UpdateUsingOfDiskStatus(progressStorageBar, diskNormalized):
    progressStorageBar.set(diskNormalized)


def ChangeStateGlobalCollectData(switchGlobal, rgbSwitchCollectData, irSwitchCollectData, classObjectRGB, classObjectIR):
    if switchGlobal.check_state:
        if not rgbSwitchCollectData.check_state:
            rgbSwitchCollectData.toggle()
            classObjectRGB.switchCollectData.value = True
        else:
            classObjectRGB.switchCollectData.value = False

        if not irSwitchCollectData.check_state:
            irSwitchCollectData.toggle()
            classObjectIR.switchCollectData.value = True
        else:
            classObjectIR.switchCollectData.value = False
    else:
        if rgbSwitchCollectData.check_state:
            rgbSwitchCollectData.toggle()
            classObjectRGB.switchCollectData.value = False
        else:
            classObjectRGB.switchCollectData.value = True
            
        if irSwitchCollectData.check_state:
            irSwitchCollectData.toggle()
            classObjectIR.switchCollectData.value = False
        else:
            classObjectIR.switchCollectData.value = True


def ChangeStateGlobalPreview(switchGlobal,switchPreviewRGB,switchPreviewIR, switchGlobalMark, switchMarkRGB, switchMarkIR,
 objectClassRGB, objectClassIR):

    if switchGlobal.check_state:
        if not switchPreviewRGB.check_state:
            switchPreviewRGB.toggle()
            objectClassRGB.switchPreview.value = True
        else:
            objectClassRGB.switchPreview.value = False

        if not switchPreviewIR.check_state:
            switchPreviewIR.toggle()
            objectClassIR.switchPreview.value = True
        else:
            objectClassIR.switchPreview.value = False

    else:
        if  switchPreviewRGB.check_state:
            switchPreviewRGB.toggle()
            objectClassRGB.switchPreview.value = False
        else:
            objectClassRGB.switchPreview.value = True

        if switchPreviewIR.check_state:
            switchPreviewIR.toggle()
            objectClassIR.switchPreview.value = False
        else:
            objectClassIR.switchPreview.value = True 

        if switchMarkRGB.check_state:
            switchMarkRGB.toggle()
            objectClassRGB.switchMark.value = False
        else:
            objectClassRGB.switchMark.value = True

        if switchMarkIR.check_state:
            switchMarkIR.toggle()
            objectClassIR.switchMark.value = False
        else:
            objectClassIR.switchMark.value = True

        if switchGlobalMark.check_state:
            switchGlobalMark.toggle()        


def ChangeStateGlobalMark(switchGlobal, switchMarkRGB, switchMarkIR, switchPreviewRGB, switchPreviewIR, classObjectRGB, classObjectIR):
    if switchGlobal.check_state:
        if not switchMarkRGB.check_state:
            switchMarkRGB.toggle()
            classObjectRGB.switchMark.value = True
        else:
            classObjectRGB.switchMark.value = False

        if not switchMarkIR.check_state:
            switchMarkIR.toggle()
            classObjectIR.switchMark.value = True
        else:
            classObjectIR.switchMark.value = False

        if not switchPreviewRGB.check_state:
            switchPreviewRGB.toggle()
            classObjectRGB.switchMark.value = True
        else:
            classObjectRGB.switchMark.value = False

        if not switchPreviewIR.check_state:
            switchPreviewIR.toggle()
            classObjectIR.switchMark.value = True
        else:
            classObjectIR.switchMark.value = False

    else:
        if switchMarkRGB.check_state:
            switchMarkRGB.toggle()
            classObjectRGB.switchMark.value = False
        else:
            classObjectRGB.switchMark.value = True

        if switchMarkIR.check_state:
            switchMarkIR.toggle()
            classObjectIR.switchMark.value = False
        else:
            classObjectIR.switchMark.value = True

def ChangeSwitchPreview(mainSwitchPreview, switchMark, classObject):

    if mainSwitchPreview.check_state:
        classObject.switchPreview.value = True
    else:
        classObject.switchPreview.value = False
        if switchMark.check_state:
            switchMark.toggle()
            classObject.switchMark.value = False  
        else:
            classObject.switchMark.value = False


def ChangeSwitchCollectData(switchCollectData, classObject):

    if switchCollectData.check_state:
        classObject.switchCollectData.value = True
    else:
        classObject.switchCollectData.value = False



def ChangeSwitchMark(mainSwitch, switch, classObject):
  
    if mainSwitch.check_state and not switch.check_state:
        switch.toggle()
        if switch.check_state:
            classObject.switchMark.value = True
            classObject.switchPreview.value = True
        else:
            classObject.switchMark.value = False


def AlmostFullDisk(label, progressStorageBar, args):
    disk = GetUsageOfDisk()
    diskNormalized = disk.used/disk.total
    UpdateUsingOfDiskStatus(progressStorageBar, diskNormalized)
    diskPercent = round(diskNormalized*100, 0)
    if diskNormalized >= 0.9:
        label.configure(text=f"Disk is almost full {diskPercent}%")
        for switch in args:
            if switch.check_state:
                switch.toogle()
            switch.configure(fg_color="#FF0000", button_color="#FF0000")
            switch.state = tkinter.DISABLED
    else:
        label.configure(text=f"Used Disk {diskPercent}%")
        for switch in args:
            switch.configure(fg_color=None, button_color=None)
            switch.state = tkinter.NORMAL
    label.after(1000, lambda: AlmostFullDisk(
        label, progressStorageBar,[arg for arg in args] ))

def LoadInfoText(infoTextPath):
    text = ""
    with open(infoTextPath) as info:
        lines = info.readlines()
    for line in lines:
        text += line
    return text

def OpenPopUpInfoWindow(infoTextPath):
    text = LoadInfoText(infoTextPath)
    tkinter.messagebox.showinfo("Information", text)


def CollectData(imagesCollectList, camName,counter,collectDataPath):
    zipFileBytes = io.BytesIO()
    recordTime = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
    with ZipFile(zipFileBytes, 'w') as zipFile:
        for id, image in enumerate(imagesCollectList):
            _, buffer = cv2.imencode(".jpg", image)
            ioBuf = io.BytesIO(buffer)
            zipFile.writestr(camName + str(id)+".jpg", ioBuf.getvalue())

    with open(collectDataPath+ camName + recordTime + '.zip', 'wb') as f:
        f.write(zipFileBytes.getvalue())

    imagesCollectList = []
    counter = 0
    return imagesCollectList,  counter


#Master function
def CamPreview(camID,camName,calibrationPath,modelPath,switchPreview,
        switchMark,switchCollectData,classesNamesPath,collectDataPath,framesQueue,otherTurn,hasTurn,stopCamera,isSynchro):
    
    camName = camName.value.decode("utf-8")
    #camID = camID.value.decode("utf-8")
    calibrationPath = calibrationPath.value.decode("utf-8")
    modelPath = modelPath.value.decode("utf-8")
    classesNamesPath = classesNamesPath.value.decode("utf-8")
    collectDataPath = collectDataPath.value.decode("utf-8")

    stereoMap_x, stereoMap_y = LoadCalibrations(calibrationPath, camName)
    imagesCollectList = []

    cam = cv2.VideoCapture(camID.value)
    
    counter = 0

    classesList, colorList = LoadClasses(classesNamesPath)
    while True:
        if stopCamera.is_set():
            break
        if cam.isOpened():
            rval, frame = cam.read()
        else:
            rval = False

        while rval:
            if stopCamera.is_set():
                break
            
            if switchPreview.value or switchCollectData.value:

                frame  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resize = cv2.resize(frame, (640, 488),
                                    interpolation=cv2.INTER_LANCZOS4)
                frame = cv2.remap(resize, stereoMap_x,
                                stereoMap_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                if camName in "RGB":
                    frame = ReMap(frame)

                if switchCollectData.value:
                    imagesCollectList.append(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    counter +=1
                    if counter >= 18000:
                        imagesCollectList, counter = CollectData(imagesCollectList,camName,counter,collectDataPath)
                else:
                    if len(imagesCollectList) > 0:
                        imagesCollectList, counter = CollectData(imagesCollectList,camName,counter,collectDataPath)


                if switchMark.value:
                    pass

                if switchPreview.value:
                    recordTime = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
                    cv2.putText(frame,recordTime , (50, 50),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255,125,125), 2)
                    
                    if isSynchro[0]:
                        if hasTurn.value:
                            framesQueue.put(frame)
                            hasTurn.value = False
                            otherTurn.value = True
                    else:
                        framesQueue.put(frame)

            rval, frame = cam.read()



def LoadClasses(path):
    classesList = []
    with open(path, 'r') as f:
        classesList = f.read().splitlines()

    colorList = np.random.uniform(
        low=0, high=255, size=(len(classesList), 3))

    return classesList, colorList

def ReMap(frame):
    translate_x, translate_y = -45, -40
    rows, cols = 488, 640
    M = np.float32([[1, 0, translate_x], [0, 1, translate_y]])
    frame = cv2.warpAffine(frame, M, (cols, rows))
    frame = frame[15:488 - 63, 15:640 - 68]
    frame = cv2.resize(frame, (640, 488), interpolation=cv2.INTER_AREA)
    return frame

def LoadCalibrations(path, camName):
    cvFile = cv2.FileStorage()
    cvFile.open(path, cv2.FileStorage_READ)
    stereoMap_x = cvFile.getNode(f'stereoMap{camName}_x').mat()
    stereoMap_y = cvFile.getNode(f'stereoMap{camName}_y').mat()
    return stereoMap_x, stereoMap_y
    
def CheckSynchro(label, RGBSwitchPreview, IRSwitchPreview, isSynchro):
    isSynchro[0] = True if RGBSwitchPreview.check_state and IRSwitchPreview.check_state else False
    label.after(200, lambda: CheckSynchro(
        label, RGBSwitchPreview, IRSwitchPreview, isSynchro))