from Application import Application
import cv2
from Helpers.Functions import *
import customtkinter
from multiprocessing import Event, Process, Manager
from Helpers.CameraProcess import CamProcess


def run():

    # TEST
    IS_CAMERA = True
    # GUI
    WIDTH = 1300
    HEIGHT = 615
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")

    imageDefault = cv2.imread(r"Data/imageDefault.png")
    infoTextPath = r"Data/InfoText.txt"
    imageDefault = cv2.resize(imageDefault, (640, 488),
                              interpolation=cv2.INTER_LANCZOS4)

    with Manager() as mg:

        IRFramesQueue = mg.Queue()
        RGBFrameQueue = mg.Queue()

        app = Application(WIDTH, HEIGHT, RGBFrameQueue,
                          IRFramesQueue, imageDefault, infoTextPath)

        if IS_CAMERA:
            # Camera
            classesNamesPath = r"Data/classes.names"
            calibrationPath = r"Data/calibration.xml"

            stopCamera = Event()
            app.stopCamera = stopCamera

            RGBModelPath = r"Data/Models/"
            RGBCollectDataPath = "Data/CollectedData/RGB/"
            camIDVideoRGB = r"Data/RGB.mp4"
            openedCamThreadRGB = CamProcess(2, "RGB", calibrationPath, RGBModelPath,
                                            classesNamesPath, RGBCollectDataPath, RGBFrameQueue)

            IRModelPath = r"Data/Models/"
            IRCollectDataPath = r"Data/CollectedData/IR/"
            camIDVideoIR = r"Data/IR.mp4"
            openedCamThreadIR = CamProcess(1, "IR", calibrationPath, IRModelPath, classesNamesPath,
                                           IRCollectDataPath, IRFramesQueue)

            app.openedCamThreadRGB = openedCamThreadRGB
            app.openedCamThreadIR = openedCamThreadIR

            ProcessRGB = Process(target=CamPreview, args=(openedCamThreadRGB.camID,
                                                                             openedCamThreadRGB.camName,
                                                                             openedCamThreadRGB.calibrationPath,
                                                                             openedCamThreadRGB.modelPath,
                                                                             openedCamThreadRGB.switchPreview,
                                                                             openedCamThreadRGB.switchMark,
                                                                             openedCamThreadRGB.switchCollectData,
                                                                             openedCamThreadRGB.classesNamesPath,
                                                                             openedCamThreadRGB.collectDataPath,
                                                                             openedCamThreadRGB.framesQueue,
                                                                             openedCamThreadIR.hasTurn,
                                                                             openedCamThreadRGB.hasTurn,
                                                                             stopCamera,
                                                                             app.isSynchro
                                                                             ))

            ProcessIR = Process(target=CamPreview, args=(openedCamThreadIR.camID,
                                                                             openedCamThreadIR.camName,
                                                                             openedCamThreadIR.calibrationPath,
                                                                             openedCamThreadIR.modelPath,
                                                                             openedCamThreadIR.switchPreview,
                                                                             openedCamThreadIR.switchMark,
                                                                             openedCamThreadIR.switchCollectData,
                                                                             openedCamThreadIR.classesNamesPath,
                                                                             openedCamThreadIR.collectDataPath,
                                                                             openedCamThreadIR.framesQueue,
                                                                             openedCamThreadRGB.hasTurn,
                                                                             openedCamThreadIR.hasTurn,
                                                                             stopCamera,
                                                                             app.isSynchro))

            processes = [ProcessRGB, ProcessIR]
            app.processes = processes
            for process in processes:
                process.start()

        app.mainloop()


if __name__ == "__main__":
    run()
