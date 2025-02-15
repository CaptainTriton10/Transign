import os
import cv2 as cv
import mediapipe as mp
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

def ExtractLandmarks(image):
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z
                })
    
    return np.array(landmarks).flatten()

def ProcessImages(img_folder, save_path="image_data.csv"):
    data = []
    
    # Loop through each label folder
    for label in os.listdir(img_folder): 
        label_path = os.path.join(img_folder, label) 
        print("Processing:", label)

        if not os.path.isdir(label_path):
            print(label_path, "is not a directory")
            continue
        
        # Loop through each image in the label folder
        for img_name in os.listdir(label_path):
            img_path = os.path.join(label_path, img_name)
            print("Processing:", img_name)
            img = cv.imread(img_path)
            if img is None:
                print("Invalid image", img_path)
                continue

            landmarks = ExtractLandmarks(img)
            if landmarks.any():
                flat_landmarks = []
                for landmark in landmarks:
                    flat_landmarks.extend([landmark['x'], landmark['y'], landmark['z']])

                row = flat_landmarks + [label]
                data.append(row)

            else:
                print("No landmarks found for", img_name)

    df = pd.DataFrame(data)
    df.to_csv(save_path, index=False, header=False)

def TrainModel(data_path, save_path="model.keras"):
    df = pd.read_csv(data_path, header=None)

    if df.empty:
        print("No data available for training.")
        return

    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values

    print(X)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(len(label_encoder.classes_), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    model.save(save_path)
    print("Model saved")

# ProcessImages("Dataset\\Train_Alphabet", save_path="Image Data\\asl_model_v2_image_data.csv")
TrainModel("Image Data\\asl_model_v2_image_data.csv", "Models\\asl_model_v2.keras")