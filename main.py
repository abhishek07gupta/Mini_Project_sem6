from moviepy.editor import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from scipy.io import wavfile
import subprocess
import math


# GLOBALS
INPUT_FILES = []                            # List of input files (in local directory)
TEMP_FOLDER = 'tmp/'                        # Temp folder name
OUTPUT_FOLDER = 'output/'                   # Output folder name
OUTPUT_FILE_NAME = "output"                 # Output file name
SAMPLE_RATE = 24                            # Number of samples to take per second to check volume level
THRESHOLD = 5                               # Required # of consecutive highest indices needed to take priority
EXCEEDS_BY = 4                              # Percentage (in decimal form) other clip(s) must exceed volume by to overtake
NO_OVERLAP_AUDIO = True                     # Restricts audio overlapping (False = overlap audio)


# INTERNAL GLOBALS (DO NOT TOUCH)
checkpoints = []  # Global storing tuples of array length + associated index, sorted from min-max by array length
checkpoint_counter = 0  # Determines which checkpoint currently at
ul_x = 10
ul_y = 10


# GUI CREATION
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("AutoPodcastEditor")
        self.pack(fill=BOTH, expand=1)
        sync_notice = Label(self, text="Please ensure all input clips are in sync at start and don't go out of sync!")
        sync_notice.place(x=ul_x, y=ul_y)
        browseFileDir = Button(self, text="Add File", command=self.addFile)
        browseFileDir.place(x=ul_x, y=ul_y+25)

        sampleRateLabel = Label(self, text="Sample Rate")
        sampleRateLabel.place(x=ul_x, y=ul_y + 320)
        self.sampleRateEntry = Entry(self, width=3)
        self.sampleRateEntry.place(x=ul_x + 73, y=ul_y + 321)
        self.sampleRateEntry.insert(END, str(SAMPLE_RATE))

        thresholdLabel = Label(self, text="Threshold")
        thresholdLabel.place(x=ul_x + 120, y=ul_y + 320)
        self.thresholdEntry = Entry(self, width=3)
        self.thresholdEntry.place(x=ul_x + 65 + 120, y=ul_y + 321)
        self.thresholdEntry.insert(END, str(THRESHOLD))

        exceedsLabel = Label(self, text="Exceeds By")
        exceedsLabel.place(x=ul_x + 235, y=ul_y + 320)
        self.exceedsEntry = Entry(self, width=3)
        self.exceedsEntry.place(x=ul_x + 65 + 235, y=ul_y + 321)
        self.exceedsEntry.insert(END, str(EXCEEDS_BY))

        overlapAudioLabel = Label(self, text="Overlap Audio")
        overlapAudioLabel.place(x=ul_x + 345, y=ul_y + 320)
        self.overlapAudioBox = Checkbutton(self, command=self.toggleAudio)
        self.overlapAudioBox.place(x=ul_x + 65 + 360, y=ul_y + 319)

        outputNameLabel = Label(self, text="Output File Name")
        outputNameLabel.place(x=ul_x, y=ul_y + 345)
        self.outputNameEntry = Entry(self, width=57)
        self.outputNameEntry.place(x=ul_x + 102, y=ul_y + 346)
        self.outputNameEntry.insert(END, OUTPUT_FILE_NAME)

        processButton = Button(self, text="Process", command=self.confirmSettings, width=15, height=3)
        processButton.place(x=ul_x + 460, y=ul_y + 310)

    def confirmSettings(self):
        global SAMPLE_RATE
        SAMPLE_RATE = int(self.sampleRateEntry.get())
        global THRESHOLD
        THRESHOLD = int(self.thresholdEntry.get())
        global EXCEEDS_BY
        EXCEEDS_BY = float(self.exceedsEntry.get())
        global OUTPUT_FILE_NAME
        OUTPUT_FILE_NAME = self.outputNameEntry.get()

    def toggleAudio(self):
        global NO_OVERLAP_AUDIO
        NO_OVERLAP_AUDIO = not NO_OVERLAP_AUDIO

    def addFile(self):
        filename = askopenfilename()
        if filename != '':
            INPUT_FILES.append(filename)
            fileDir = Label(self, text=filename)
            fileDir.place(x=ul_x, y=ul_y+28+23*len(INPUT_FILES))


root = Tk()
root.geometry("600x400")
app = Window(root)
root.mainloop()