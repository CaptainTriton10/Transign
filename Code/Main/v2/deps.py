from mediapipe import tasks

GLOBALS = {
    "IMG_WIDTH" : 480,
    "IMG_HEIGHT" : 360,
    "WINDOW_WIDTH" : 1080,
    "WINDOW_HEIGHT" : 720,
    "PADX" : 15,
    "PADY" : 15,
    "MAX_REPS" : 50,
    "CURSOR_CHAR" : "▌",
    "CAM_NUMBERS" : [
        "0",
        "1",
    ]
}

COLOURS = {
    "MED_GREY" : "#383C3C",
    "LIGHT_GREY" : "#C0C0C0"
}

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

#region Mediapipe

# .task model path
MODEL_PATH = r"Models\asl_model_v3.task"

with open(MODEL_PATH, "rb") as file:
    model = file.read()

# Prerequisites for mediapipe gesture recognition
BaseOptions = tasks.BaseOptions
GestureRecognizer = tasks.vision.GestureRecognizer
GestureRecognizerOptions = tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = tasks.vision.GestureRecognizerResult
VisionRunningMode = tasks.vision.RunningMode

def GetOptions(callback):
    # Options for gesture recogniser
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=model),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=callback
    )

    return options

#endregion