import os
import time

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Package dependencies
print("Loading dependencies")
start_time = time.time()

import customtkinter as ctk
from PIL import Image
import mediapipe as mp
import cv2 as cv
import numpy as np
import threading
from deps import *

print(f"Done! [{round(time.time() - start_time, 3)}s elapsed]")

# Settings:
# Theme
#  - Light/Dark
#  - Colour dropdown
#  - High contrast

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


def ChangeWebcamNumber(choice):
    try:
        app.cap = cv.VideoCapture(int(choice))

    except Exception as e:
        print("Something went wrong:", e)
        print(choice)

#region Webcam Tab

# Class for webcam image/label within the frame
class WebcamFrame(ctk.CTkFrame):
    def __init__(self, master, width=GLOBALS["IMG_WIDTH"], height=GLOBALS["IMG_HEIGHT"], fg_color=COLOURS["MED_GREY"]):
        super().__init__(master, width, height, fg_color=COLOURS["MED_GREY"])

        self.rowconfigure((0,1), weight=1)
        self.columnconfigure(0, weight=1)

        # Label that is used to show image
        # Weirdly, it is not an image, but a label with the text set to ""
        self.cam = ctk.CTkLabel(self, text="", font=("TkDefaultFont", 56))
        self.cam.grid(row=0, column=0, padx=GLOBALS["PADX"], pady=GLOBALS["PADY"], sticky="nsew")

        # Progress bar to show current number of reps
        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=1, column=0, padx=GLOBALS["PADX"], pady=(0, GLOBALS["PADY"]), sticky="ew")
        self.progress.set(0)


# Class for frame containing options for webcam/recogniser
class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master, fg_color=COLOURS["MED_GREY"]):
        super().__init__(master, fg_color=COLOURS["MED_GREY"])

        # Configure rows and columns expanding
        self.columnconfigure(0, weight=1)

        # Button to toggle webcam
        self.webcam_button = ctk.CTkButton(self, text="Start Webcam", height=42, command=lambda: App.ToggleWebcam(app))
        self.webcam_button.grid(row=0, column=0, padx=GLOBALS["PADX"], pady=GLOBALS["PADY"], sticky="ew")

        # Option box for selecting webcam
        self.webcam_number = ctk.StringVar(value=GLOBALS["CAM_NUMBERS"][1])
        self.webcam_options = ctk.CTkOptionMenu(self, values=GLOBALS["CAM_NUMBERS"], variable=self.webcam_number, command=ChangeWebcamNumber)
        self.webcam_options.grid(row=1, column=0, padx=GLOBALS["PADX"], pady=(0, GLOBALS["PADY"]), sticky="ew")

        # Label for sense_slider
        self.sense_label = ctk.CTkLabel(self, text="Sensitivity")
        self.sense_label.grid(row=2, column=0, padx=GLOBALS["PADX"], pady=(0, GLOBALS["PADY"]), sticky="ew")

        # Slider for controlling repetition sensitivity
        self.sense_slider = ctk.CTkSlider(self, number_of_steps=GLOBALS["MAX_REPS"])
        self.sense_slider.grid(row=3, column=0, padx=GLOBALS["PADX"], pady=(0, GLOBALS["PADY"]), sticky="ew")

        # Button for clearing
        self.clear_button = ctk.CTkButton(self, text="Clear", height=42, command=lambda: App.ClearOutput(app))
        self.clear_button.grid(row=4, column=0, padx=GLOBALS["PADX"], pady=(0, GLOBALS["PADY"]), sticky="nsew")


# Class for showing output text
class OutputFrame(ctk.CTkFrame):
    def __init__(self, master, fg_color=COLOURS["MED_GREY"]):
        super().__init__(master, fg_color=COLOURS["MED_GREY"])

        # Literally just a font
        output_font = ctk.CTkFont(family="TkDefaultFont", size=56, weight="bold")

        # Label for showing recognition output
        self.output = ctk.CTkLabel(self, text=GLOBALS["CURSOR_CHAR"], font=output_font, wraplength=900)
        self.output.grid(row=0, column=0, padx=GLOBALS["PADX"], pady=GLOBALS["PADY"], sticky="ew")

#endregion

#region Settings Tab

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.title_font = ctk.CTkFont(family="TkDefaultFont", size=42, weight="bold")

        self.title = ctk.CTkLabel(self, text="Theme", font=self.title_font)
        self.title.grid(row=0, column=0, padx=GLOBALS["PADX"], pady=GLOBALS["PADY"], sticky="w")

        self.colour_mode = ctk.CTkSwitch(self, text="Light Mode")
        self.colour_mode.grid(row=1, column=0, padx=GLOBALS["PADX"], pady=(0, GLOBALS["PADY"]), sticky="w")

#endregion

# Class for tab view
class Tabs(ctk.CTkTabview):
    def __init__(self, master, width=GLOBALS["WINDOW_WIDTH"], height=GLOBALS["WINDOW_HEIGHT"]):
        super().__init__(master, width, height)

        # Tab objects
        self.webcam_tab = self.add("Webcam")
        self.settings_tab = self.add("Settings")

        # Configure rows/columns for tabs
        self.webcam_tab.columnconfigure(0, weight=1)
        self.webcam_tab.rowconfigure((0, 1), weight=1)

        #region Webcam Tab

        #Frame for webcam image
        self.webcam_frame = WebcamFrame(self.webcam_tab)
        self.webcam_frame.grid(row=0, column=0, padx=GLOBALS["PADX"], pady=GLOBALS["PADY"], sticky="nsew")

        # Frame for options
        self.options_frame = OptionsFrame(self.webcam_tab)
        self.options_frame.grid(row=0, column=1, padx=(0, GLOBALS["PADX"]), pady=GLOBALS["PADY"], sticky="nsew")

        # Frame for output text
        self.output_frame = OutputFrame(self.webcam_tab)
        self.output_frame.grid(row=1, column=0, padx=GLOBALS["PADX"], pady=(0, GLOBALS["PADY"]), sticky="nsew", columnspan=2)

        #endregion

        #region Settings Tab

        self.settings_frame = SettingsFrame(self.settings_tab)
        self.settings_frame.grid(row=0, column=0, padx=GLOBALS["PADX"], pady=GLOBALS["PADY"], sticky="nsew")

        #endregion


# Main app class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Creates gesture recogniser object
        self.recogniser = GestureRecognizer.create_from_options(GetOptions(GetLetter))

        # Creates window size and title
        self.geometry(f"{GLOBALS['WINDOW_WIDTH']}x{GLOBALS['WINDOW_HEIGHT']}")
        self.title("Transign")

        # Configure rows and columns
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # CTkTabView for page tabs
        self.tabs = Tabs(self)
        self.tabs.pack(expand=True, padx=GLOBALS["PADX"], pady=GLOBALS["PADY"])

        # Variables for update loop
        self.previous_letter = ""
        self.reps = 0
        self.cap = None
        self.phrase = ""
        self.is_running = False
        self.reps_needed = 20
        self.timestamp = 0

    # Toggles webcam
    def ToggleWebcam(self):
        # If the webcam isn't running, set it to running,
        if not self.is_running:
            # Starts webcam
            self.is_running = True

            # Clear the text from the webcam label
            self.tabs.webcam_frame.cam.configure(text="")
            self.tabs.options_frame.webcam_button.configure(text="Stop Webcam")
            self.cap = cv.VideoCapture(int(self.tabs.options_frame.webcam_number.get()))

            # Creates a separate thread for getting the webcam, so the GUI isn't blocked
            self.t_frame_loop = threading.Thread(target=self.UpdateFrame, daemon=True)
            self.t_frame_loop.start()

        else:
            # Stops webcam + changes text
            self.is_running = False
            self.tabs.webcam_frame.cam.configure(text="Webcam Stopped")
            self.tabs.options_frame.webcam_button.configure(text="Start Webcam")
            self.cap.release()

    def UpdateFrame(self):
        while self.cap.isOpened():
            # Gets image from camera
            ret, frame = self.cap.read()

            if ret:
                # Increments timestamp and updates number of repetitions needed from slider
                self.timestamp += 1
                self.reps_needed = int(((1 - self.tabs.options_frame.sense_slider.get()) * GLOBALS["MAX_REPS"]) + 1)

                # RGB image from frame and array from RGB image
                image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                image = Image.fromarray(image_rgb)

                # Converts frame to a mediapipe image to be processed by the recogniser
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(frame))

                # Runs the recogniser asynchronously using the mp_image and frame number (timestamp)
                self.recogniser.recognize_async(mp_image, self.timestamp)

                # Updates the GUI using the image array using self.after to avoid blocking the main thread
                self.after(0, self.UpdateGUI, image)

    def UpdateGUI(self, image):
        # Updates the webcam label
        self.ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(GLOBALS["IMG_WIDTH"], GLOBALS["IMG_HEIGHT"]))
        self.tabs.webcam_frame.cam.configure(image=self.ctk_image)

    def UpdateLetter(self, letter):
        # Increments reps if the last letter is the same as the current letter
        if letter == self.previous_letter:
            self.reps += 1
            self.tabs.webcam_frame.progress.set(self.reps / self.reps_needed)

        # Resets reps count if the last letter isn't the same as the current letter
        else:
            self.reps = 0
            self.tabs.webcam_frame.progress.set(0)

        # When the number of reps reaches the threshold, add it to the phrase and updates the output text
        if self.reps >= self.reps_needed:
            self.phrase += f"{letter}"
            self.tabs.output_frame.output.configure(text=f"{self.phrase}{GLOBALS['CURSOR_CHAR']}")
            self.reps = 0
            self.tabs.webcam_frame.progress.set(0)

        self.previous_letter = letter

    def ClearOutput(self):
        # Clear all variables
        self.phrase = ""
        self.reps = 0
        self.tabs.webcam_frame.progress.set(0)

        self.tabs.output_frame.output.configure(text=GLOBALS["CURSOR_CHAR"])

# Creates the app class and starts the webcam
app = App()
app.ToggleWebcam()
app.mainloop()

# Releases the webcam once the program terminates
app.cap.release()