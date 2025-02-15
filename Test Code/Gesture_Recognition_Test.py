import mediapipe as mp
import numpy as np
from PIL import Image
import cv2 as cv

MODEL_PATH = r"Models\asl_model_v3.task"
IMAGE_PATH = r"Dataset\Test_Alphabet\L\0f6670c7-584f-4e71-b33a-54c77e549f5a.rgb_0000.png"

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE)

cap = cv.VideoCapture(1)

recogniser = GestureRecognizer.create_from_options(options)
# numpy_img = np.array(Image.open(IMAGE_PATH))
# mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_img)

# result = recogniser.recognize(mp_image)

# for gesture in result.gestures:
#     prediction = [category.category_name for category in gesture]
#     print(prediction[0])
while cap.isOpened():
    ret, frame = cap.read()
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(frame))

    result = recogniser.recognize(mp_image)

    cv.imshow('Gesture Test', frame)

    for gesture in result.gestures:
        prediction = [category.category_name for category in gesture]
        print(prediction[0])

    if cv.waitKey(1) & 0xFF == ord('q'):
        break   

cap.release()
cv.destroyAllWindows()