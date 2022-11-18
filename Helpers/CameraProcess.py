from multiprocessing import Value, Array
from ctypes import c_int, c_bool


class CamProcess():
    def __init__(self,
                camID,
                camName,
                calibrationPath,
                modelPath,
                classesNamesPath,
                collectDataPath,
                framesQueue,
                ):
        
        #self.camID = Array('c',bytes(f'{camID}',encoding='utf-8'))
        self.camID = Value(c_int,camID )
        self.camName = Array('c',bytes(f'{camName}',encoding='utf-8'))
        self.calibrationPath = Array('c',bytes(f'{calibrationPath}',encoding='utf-8'))
        self.modelPath = Array('c',bytes(f'{modelPath}',encoding='utf-8'))
        self.switchPreview = Value(c_bool,False)
        self.switchMark = Value(c_bool,False)
        self.switchCollectData = Value(c_bool,False)
        self.framesQueue = framesQueue
        self.classesNamesPath = Array('c',bytes(f'{classesNamesPath}',encoding='utf-8'))
        self.collectDataPath = Array('c',bytes(f'{collectDataPath}',encoding='utf-8'))
        self.hasTurn = Value(c_bool,True)
        