import customtkinter
from Helpers.Functions import *


class Application(customtkinter.CTk):

    def __init__(self, WIDTH, HEIGHT, RGBFramesQueue, IRFramesQueue, imageDefault, infoTextPath):
        super().__init__()

        self.title("People detection app")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.Exit)
        self.RGBFramesQueue = RGBFramesQueue
        self.IRFramesQueue = IRFramesQueue
        self.imageDefault = imageDefault
        self.infoTextPath = infoTextPath
        self.stopCamera = None
        self.openedCamThreadRGB = None
        self.openedCamThreadIR = None
        self.processes = []
        #list to send bool as reference
        self.isSynchro = [False]


# Main Frame

        self.Previews = customtkinter.CTkFrame(
            master=self, corner_radius=10)
        self.Previews.grid(row=0, column=0, sticky="nswe", pady=10, padx=10)

        self.ProgressStorage = customtkinter.CTkFrame(
            master=self, corner_radius=20)
        self.ProgressStorage.grid(
            row=1, column=0, sticky="nswe", padx=10)
        self.ProgressStorage.columnconfigure((0, 2), weight=0)
        self.ProgressStorage.columnconfigure(1, weight=10)


# Previews Frame

        self.RGBColumn = customtkinter.CTkFrame(
            master=self.Previews)
        self.RGBColumn.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.IRColumn = customtkinter.CTkFrame(master=self.Previews)
        self.IRColumn.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.OptionColumn = customtkinter.CTkFrame(
            master=self.Previews)

        self.OptionColumn.rowconfigure((0,1), weight=1)
        self.OptionColumn.rowconfigure(5, weight=5)
        self.OptionColumn.rowconfigure((2,3,4), weight=10)

        self.OptionColumn.grid(
            row=0, column=2, sticky="nswe", padx=10, pady=10)

# RGB Frame

        self.RGBLabel = customtkinter.CTkLabel(
            master=self.RGBColumn, text="RGB", text_font=("Roboto Medium", -16))
        self.RGBLabel.grid(row=0, column=0, pady=10, padx=10)

        self.RGBFrame = customtkinter.CTkLabel(master=self.RGBColumn)
        self.RGBFrame.after(100, lambda: PreviewImage(
            self.RGBFrame, self.RGBFramesQueue, self.RGBSwitchPreview, self.imageDefault))
        self.RGBFrame.grid(row=1, column=0, sticky="nswe")

        self.RGBSwitchesGroup = customtkinter.CTkFrame(master=self.RGBColumn)
        self.RGBSwitchesGroup.grid(row=2, column=0, sticky="nswe")
        self.RGBSwitchesGroup.columnconfigure((0,1,2), weight=5)

        self.RGBSwitchPreview = customtkinter.CTkSwitch(
            master=self.RGBSwitchesGroup, text="RGB Preview", command=lambda: ChangeSwitchPreview(
                self.RGBSwitchPreview, self.RGBSwitchMark, self.openedCamThreadRGB))

        self.RGBSwitchPreview.grid(
            row=0, column=0, pady=10, padx=20, sticky="we")

        self.RGBSwitchMark = customtkinter.CTkSwitch(
            master=self.RGBSwitchesGroup, text="RGB Mark", command=lambda: ChangeSwitchMark(self.RGBSwitchMark, self.RGBSwitchPreview, self.openedCamThreadRGB))
        self.RGBSwitchMark.grid(
            row=0, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.RGBSwitchCollectData = customtkinter.CTkSwitch(
            master=self.RGBSwitchesGroup, text="RGB Collect Data", command=lambda: ChangeSwitchCollectData(self.RGBSwitchCollectData, self.openedCamThreadRGB))
        self.RGBSwitchCollectData.grid(
            row=0, column=2, columnspan=1, pady=10, padx=20, sticky="we")

# IR Frame

        self.IRLabel = customtkinter.CTkLabel(
            master=self.IRColumn, text="IR", text_font=("Roboto Medium", -16))
        self.IRLabel.grid(row=0, column=0, pady=10, padx=10)

        self.IRFrame = customtkinter.CTkLabel(master=self.IRColumn)
        self.IRFrame.after(100, lambda: PreviewImage(
            self.IRFrame, self.IRFramesQueue, self.IRSwitchPreview, self.imageDefault))
        self.IRFrame.grid(row=1, column=0, sticky="nswe")

        self.IRSwitchesGroup = customtkinter.CTkFrame(master=self.IRColumn)
        self.IRSwitchesGroup.grid(row=2, column=0, sticky="nswe")
        self.IRSwitchesGroup.columnconfigure((0,1,2), weight=5)

        self.IRSwitchPreview = customtkinter.CTkSwitch(
            master=self.IRSwitchesGroup, text="IR Preview", command=lambda: ChangeSwitchPreview(self.IRSwitchPreview, self.IRSwitchMark, self.openedCamThreadIR))
        self.IRSwitchPreview.grid(
            row=0, column=0, columnspan=1, pady=10, padx=20, sticky="we")

        self.IRSwitchMark = customtkinter.CTkSwitch(
            master=self.IRSwitchesGroup, text="IR Mark", command=lambda: ChangeSwitchMark(self.IRSwitchMark, self.IRSwitchPreview, self.openedCamThreadIR))
        self.IRSwitchMark.grid(row=0, column=1, columnspan=1,
                               pady=10, padx=20, sticky="we")

        self.IRSwitchCollectData = customtkinter.CTkSwitch(
            master=self.IRSwitchesGroup, text="IR Collect Data", command=lambda: ChangeSwitchCollectData(self.IRSwitchCollectData, self.openedCamThreadIR))
        self.IRSwitchCollectData.grid(
            row=0, column=2, columnspan=1, pady=10, padx=20, sticky="we")

# Option Frame

        self.InfoButton = customtkinter.CTkButton(
            master=self.OptionColumn, text="Info", command=lambda: OpenPopUpInfoWindow(self.infoTextPath))
        self.InfoButton.grid(row=0, column=0, pady=8, padx=10)

        self.SwitchesOptionFrame = customtkinter.CTkFrame(master=self.OptionColumn)
        self.SwitchesOptionFrame.grid(row=1, column = 0, sticky="n")

        self.OptionLabel = customtkinter.CTkLabel(
            master=self.SwitchesOptionFrame, text="Global switches", text_font=("Roboto Medium", -16))
        self.OptionLabel.after(100, lambda: CheckSynchro(self.OptionLabel,self.RGBSwitchPreview, self.IRSwitchPreview, self.isSynchro))
        self.OptionLabel.grid(row=0, column=0, pady=10, padx=10)

        self.GlobalSwitchesGroup = customtkinter.CTkFrame(master=self.SwitchesOptionFrame)
        self.GlobalSwitchesGroup.grid(row=1, column=0, pady=10, padx=10)
        self.GlobalSwitchesGroup.columnconfigure(0, weight=0)
        self.GlobalSwitchesGroup.columnconfigure(1, weight=10)

        self.GlobalSwitchPreview = customtkinter.CTkSwitch(
            master=self.GlobalSwitchesGroup, text="Global Preview", command=lambda: ChangeStateGlobalPreview(
                self.GlobalSwitchPreview, self.RGBSwitchPreview, self.IRSwitchPreview, self.GlobalSwitchMark, self.RGBSwitchMark, 
                self.IRSwitchMark, self.openedCamThreadRGB, self.openedCamThreadIR))
        
        self.GlobalSwitchPreview.grid(row=0, column=0, pady=10, padx=10,sticky="w")

        self.GlobalSwitchMark = customtkinter.CTkSwitch(
            master=self.GlobalSwitchesGroup, text="Global Mark", command=lambda: ChangeStateGlobalMark(
                self.GlobalSwitchMark,self.RGBSwitchMark, self.IRSwitchMark, self.RGBSwitchPreview, self.IRSwitchPreview,
                self.openedCamThreadRGB, self.openedCamThreadIR))

        self.GlobalSwitchMark.grid(row=1, column=0, pady=10, padx=10,sticky="w")

        self.GlobalSwitchCollectData = customtkinter.CTkSwitch(
            master=self.GlobalSwitchesGroup, text="Global Collect Data", command=lambda: ChangeStateGlobalCollectData(
                self.GlobalSwitchCollectData, self.RGBSwitchCollectData, self.IRSwitchCollectData, self.openedCamThreadRGB, 
                self.openedCamThreadIR))

        self.GlobalSwitchCollectData.grid(row=2, column=0, pady=10, padx=10,sticky="w")

        self.OffButton = customtkinter.CTkButton(
            master=self.OptionColumn, text="Exit", command=self.Exit)
        self.OffButton.grid(row=5, column=0, pady=10, padx=10, sticky = "s")

# ProgressStorage

        self.StorageLabel = customtkinter.CTkLabel(
            master=self.ProgressStorage, text="Used Disk", text_font=("Roboto Medium", -16))
        self.StorageLabel.after(1000, lambda: AlmostFullDisk(self.StorageLabel, self.ProgressStorageBar,
                                [self.GlobalSwitchCollectData, self.RGBSwitchCollectData, self.IRSwitchCollectData]))
        self.StorageLabel.grid(row=0, column=1, sticky="ew", padx=15, pady=8)

        self.ProgressStorageBar = customtkinter.CTkProgressBar(
            master=self.ProgressStorage)
        self.ProgressStorageBar.grid(
            row=1, column=1, sticky="ew", padx=15, pady=15)

# Functions

    def Exit(self, event=0):
        self.openedCamThreadRGB.switchCollectData.value = False
        self.openedCamThreadIR.switchCollectData.value = False
        self.stopCamera.set()
        for process in self.processes:
            process.join()
        self.destroy()

