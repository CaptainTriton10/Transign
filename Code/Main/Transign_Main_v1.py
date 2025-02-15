print("Loading dependancies")
import customtkinter as ctk
from PIL import Image
from mediapipe import solutions
from keras.models import load_model 
import cv2 as cv
import numpy as np

IMG_WIDTH = 480
IMG_HEIGHT = 360

GLOBAL_PADX = 15
GLOBAL_PADY = 15

model = load_model("Models\\asl_model_v1.keras", compile=False)

mp_hands = solutions.hands  
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = solutions.drawing_utils

def ExtractLandmarks(image):
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    landmarks = []
    x_landmarks = []
    y_landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
                x_landmarks.append(landmark.x)
                y_landmarks.append(landmark.y)

    
    return np.array(landmarks), x_landmarks, y_landmarks

def Predict(landmarks):
    if len(landmarks) == 0:
        return "No hand detected"
    
    prediction = model.predict(np.array([landmarks]))
    return chr(prediction.argmax() + 65)

def CropToBounds(image, x_landmarks, y_landmarks):
    offset = 40
    
    left = int(min(x_landmarks) * 640) - offset
    right = int(max(x_landmarks) * 640) + offset
    bottom = int(max(y_landmarks) * 480) + offset
    upper = int(min(y_landmarks) * 480) - offset

    cropped_image = image.crop((left, upper, right, bottom))
    return cropped_image

class WebcamFrame(ctk.CTkFrame):
    def __init__(self, master, width=IMG_WIDTH, height=IMG_HEIGHT):
        super().__init__(master, width, height)

        self.cam = ctk.CTkLabel(self, text="", font=("TkDefaultFont", 56))
        self.cam.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="nsew")

        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=1, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="ew")
        self.progress.set(0)

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.webcam_button = ctk.CTkButton(self, text="Start Webcam", height=42, command=lambda: App.ToggleWebcam(master))
        self.webcam_button.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="ew")

        self.crop_button = ctk.CTkSwitch(self, text="Crop Video")
        self.crop_button.grid(row=1, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="w")

        self.sense_label = ctk.CTkLabel(self, text="Sensetivity")
        self.sense_label.grid(row=2, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="ew")

        self.sense_slider = ctk.CTkSlider(self, number_of_steps=9)
        self.sense_slider.grid(row=3, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="ew")

class OutputFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        output_font = ctk.CTkFont(family="TkDefaultFont", size=56, weight="bold")
        
        self.output = ctk.CTkLabel(self, text="", font=output_font, wraplength=900)
        self.output.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="ew")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1080x960")
        self.title("Transign")
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.webcam_frame = WebcamFrame(self)
        self.webcam_frame.grid(row=0, column=0, padx=GLOBAL_PADX, pady=GLOBAL_PADY, sticky="nsew")

        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=0, column=1, padx=(0, GLOBAL_PADX), pady=GLOBAL_PADY, sticky="nsew")

        self.output_frame = OutputFrame(self)
        self.output_frame.grid(row=1, column=0, padx=GLOBAL_PADX, pady=(0, GLOBAL_PADY), sticky="nsew", columnspan=2)

        self.previous_letter = ""
        self.reps = 0
        self.cap = None
        self.phrase = ""
        self.is_running = False
        self.reps_needed = 5

    def ToggleWebcam(self):
        if not self.is_running:
            self.is_running = True
            self.webcam_frame.cam.configure(text="")
            self.options_frame.webcam_button.configure(text="Stop Webcam")
            self.cap = cv.VideoCapture(1)
            self.UpdateFrame()
        else:
            self.is_running = False
            self.webcam_frame.cam.configure(text="Webcam Stopped")
            self.options_frame.webcam_button.configure(text="Start Webcam")
            self.cap.release()

    def UpdateFrame(self):
        ret, frame = self.cap.read()
        if ret:

            self.reps_needed = int(10 - ((self.options_frame.sense_slider.get() * 8) + 1))
            image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image_rgb, landmarks, mp_hands.HAND_CONNECTIONS)
            
            image = Image.fromarray(image_rgb)
            cropped_image = self.GetLetter(image_rgb, image)

            if cropped_image == None:
                self.ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(IMG_WIDTH, IMG_HEIGHT))
            else:
                self.ctk_image = ctk.CTkImage(light_image=cropped_image, dark_image=cropped_image, size=(IMG_WIDTH, IMG_HEIGHT))
                
            self.webcam_frame.cam.configure(image=self.ctk_image)
            
            self.after(1, self.UpdateFrame)

    def GetLetter(self, array_image, image):
        extraction = ExtractLandmarks(array_image)
        landmarks = extraction[0]
        x_landmarks = extraction[1]
        y_landmarks = extraction[2]

        if landmarks.any():
            letter = Predict(landmarks)
            if self.options_frame.crop_button.get() == 1:
                cropped_image = CropToBounds(image, x_landmarks, y_landmarks)
            else:
                cropped_image = None

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

            return cropped_image
    
app = App()
app.ToggleWebcam()
app.mainloop()