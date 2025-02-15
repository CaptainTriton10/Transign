import mediapipe as mp
import cv2 as cv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=5, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

capture = cv.VideoCapture(1)

while capture.isOpened():
    ret, frame = capture.read()

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv.imshow('Hand Tracking', frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break   

capture.release()
cv.destroyAllWindows()