import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

X = []
Y = []

def detectAndDraw(frame):
    with mp_hands.Hands(model_complexity=0,min_detection_confidence=0.5,max_num_hands = 1,min_tracking_confidence=0.5) as hands:
        image = frame
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        imgH, imgW, _ = image.shape
        global X
        global Y
        X = []
        Y = []
        if results.multi_hand_landmarks:
            #print(len(results.multi_hand_landmarks))
            for hand_landmarks in results.multi_hand_landmarks:
                #print(hand_landmarks.landmark)
                #print(len(hand_landmarks.landmark))
                #print(hand_landmarks.landmark[8])
                for i in range(0,len(hand_landmarks.landmark)):
                    X.append((hand_landmarks.landmark[i].x)*imgW)
                    Y.append((hand_landmarks.landmark[i].y)*imgH)

                #print(X,Y)
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        
    return image

def getCoordinates():
    return X,Y