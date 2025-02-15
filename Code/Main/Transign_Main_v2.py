import os

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

print("Loading dependencies")
import customtkinter as ctk
from PIL import Image
import mediapipe as mp
import cv2 as cv
import numpy as np
import time
import threading

# Webcam image size
IMG_WIDTH = 480
IMG_HEIGHT = 360

# Padding for all widgets
GLOBAL_PADX = 15
GLOBAL_PADY = 15

# Max number of reps needed (Upper slider limit)
MAX_REPS = 50

# .task model path
MODEL_PATH = r"C:\Computing\Transign\Models\asl_model_v3.task"

with open(MODEL_PATH, "rb") as file:
    model = file.read()

# Gets the letter from a mp_image
def GetLetter(result, output_image, timestamp_ms):
    if result is not None:
        for gesture in result.gestures:
            prediction = [category.category_name for category in gesture]
            if len(prediction) >= 1:
                if prediction[0] == "space":
                    app.after(0, app.UpdateLetter, " ")
                    
                else:
                    # Ensures the gui is updated in main thread (I think)
                    # Honestly I don't know why it works, it just does
                    app.after(0, app.UpdateLetter, prediction[0])

# Prerequisites for mediapipe gesture recognition
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Options for gesture recogniser
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_buffer=model),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=GetLetter)

# Unused, but crops image to hand with an offset
def CropToBounds(image, x_landmarks, y_landmarks):
    offset = 40
    
    # Gets pixel values of edge crops with added offset
    left = int(min(x_landmarks) * 640) - offset
    right = int(max(x_landmarks) * 640) + offset
    bottom = int(max(y_landmarks) * 480) + offset
    upper = int(min(y_landmarks) * 480) - offset

    cropped_image = image.crop((left, upper, right, bottom))
    return cropped_image

# Class for webcam image/label within the frame
class WebcamFrame(ctk.CTkFrame):
    def __init__(self, master, width=IMG_WIDTH, height=IMG_HEIGHT):
        super().__init__(master, width, height)

        # Label that is used to show image
        # Weirdly, it is not an image, but a label with the text set to ""
        self.cam = ctk.CTkLabel(self, text="", font=("TkDefaultFont", 56))
        self.cam.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="nsew")

        # Progress bar to show current number of reps
        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=1, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="ew")
        self.progress.set(0)

# Class for frame containing options for webcam/recogniser
class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Configure rows and columns expanding
        self.columnconfigure(0, weight=1)

        # Button to toggle webcam
        self.webcam_button = ctk.CTkButton(self, text="Start Webcam", height=42, command=lambda: App.ToggleWebcam(master))
        self.webcam_button.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="ew")

        # Label for sense_slider
        self.sense_label = ctk.CTkLabel(self, text="Sensitivity")
        self.sense_label.grid(row=2, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="ew")

        # Slider for controlling repetition sensitivity
        self.sense_slider = ctk.CTkSlider(self, number_of_steps=MAX_REPS)
        self.sense_slider.grid(row=3, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="ew")

# Class for showing output text
class OutputFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Literally just a font
        output_font = ctk.CTkFont(family="TkDefaultFont", size=56, weight="bold")
        
        # Label for showing recognition output
        self.output = ctk.CTkLabel(self, text="", font=output_font, wraplength=900)
        self.output.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="ew")

# Main app class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Creates gesture recogniser object
        self.recogniser = GestureRecognizer.create_from_options(options)

        # Creates window size and title
        self.geometry("1080x960")
        self.title("Transign")
        
        # Configure rows and columns
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Frame for webcam image
        self.webcam_frame = WebcamFrame(self)
        self.webcam_frame.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="nsew")

        # Frame for options
        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=0, column=1, padx=(0, GLOBAL_PADX), pady=GLOBAL_PADY, sticky="nsew")

        # Frame for output text
        self.output_frame = OutputFrame(self)
        self.output_frame.grid(row=1, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="nsew", columnspan=2)
        
        # Variables for update loop
        self.previous_letter = ""
        self.reps = 0
        self.cap = None
        self.phrase = ""
        self.is_running = False
        self.reps_needed = 15
        self.timestamp = 0

    # Toggles webcam
    def ToggleWebcam(self):
        # If the webcam isn't running, set it to running,
        if not self.is_running:
            print(self.timestamp)
            self.is_running = True

            # Clear the text from the webcam label
            self.webcam_frame.cam.configure(text="")
            self.options_frame.webcam_button.configure(text="Stop Webcam")
            self.cap = cv.VideoCapture(1)
            
            self.t_frame_loop = threading.Thread(target=self.UpdateFrame, daemon=True)
            self.t_frame_loop.start()
        else:
            self.is_running = False
            self.webcam_frame.cam.configure(text="Webcam Stopped")
            self.options_frame.webcam_button.configure(text="Start Webcam")
            self.cap.release()

    def UpdateFrame(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                self.timestamp += 1
                self.reps_needed = int(((1 - self.options_frame.sense_slider.get()) * MAX_REPS) + 1)

                image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                image = Image.fromarray(image_rgb)
                
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(frame))

                self.recogniser.recognize_async(mp_image, self.timestamp)

                self.after(0, self.UpdateGUI, image)

    def UpdateGUI(self, image):
        self.ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(IMG_WIDTH, IMG_HEIGHT))
        self.webcam_frame.cam.configure(image=self.ctk_image)

    def UpdateLetter(self, letter):
        if letter == self.previous_letter:
            self.reps += 1
            self.webcam_frame.progress.set(self.reps / self.reps_needed)
        else:
            self.reps = 0
            self.webcam_frame.progress.set(0)

        if self.reps >= self.reps_needed:
            self.phrase += letter
            self.output_frame.output.configure(text=self.phrase)
            self.reps = 0
            self.webcam_frame.progress.set(0)

        self.previous_letter = letter
    
app = App()
app.ToggleWebcam()
app.mainloop()

app.cap.release()