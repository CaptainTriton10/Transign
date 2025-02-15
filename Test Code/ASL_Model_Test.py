import tensorflow as tf
import numpy as np
import cv2 as cv
import mediapipe as mp

model = tf.keras.models.load_model("asl_model_trained.keras", compile=False)

mp_hands = mp.solutions.hands  
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

def ExtractLandmarks(image):
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
    
    return np.array(landmarks)

def Predict(landmarks):
    if len(landmarks) == 0:
        return "No hand detected"
    
    prediction = model.predict(np.array([landmarks]))
    return chr(prediction.argmax() + 65)

cap = cv.VideoCapture(1)

index = 0
while True:
    ret, frame = cap.read()
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(img)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    landmarks = ExtractLandmarks(frame)
    print(Predict(landmarks))
    
    cv.imshow('frame', frame)
    
    if cv.waitKey(1) == ord('q'):
        break
    
    index += 1

cap.release()
cv.destroyAllWindows()