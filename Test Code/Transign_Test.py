import mediapipe as mp
from tkinter_webcam import webcam
import cv2 as cv
import customtkinter as ctk
from PIL import Image, ImageTk

cap = cv.VideoCapture(0)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("960x540")
        self.title("Transign Test")

        self.cam = ctk.CTkLabel(self)

    def OpenCamera(self):
        ret, frame = cap.read()

        opencv_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(imge=captured_image)
        self.cam

app = App()
app.bind('<escape>', lambda e: app.quit())
app.mainloop()