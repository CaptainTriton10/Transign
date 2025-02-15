import tensorflow as tf
import numpy as np
import cv2 as cv
import mediapipe as mp
from os import listdir, path

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

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

def ProcessImages(data_path):
    x_landmarks = []
    y_landmarks = []

    data = []

    for img_folder in listdir(data_path):
        for image in listdir(path.join(data_path, img_folder)):
            extraction = ExtractLandmarks(image)

            if extraction[0].any():
                x_landmarks = extraction[1]
                y_landmarks = extraction[2]

                bottom_left = int(min(x_landmarks), min(y_landmarks))
                top_right = int(max(x_landmarks), max(y_landmarks))

                row

ProcessImages("Dataset\\Test_Alphabet")