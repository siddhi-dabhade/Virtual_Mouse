import cv2      # used to open our video camera
import mediapipe as mp      # to detect the hand
import pyautogui

cap = cv2.VideoCapture(0)       # to capture the video
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils      # used to draw landmarks on ur hand
screen_width , screen_height = pyautogui.size()
index_y = 0

while True:
    _, frame = cap.read()       # to read the video continously
    frame = cv2.flip(frame, 1)      # to flip the frame on the y-axis to mirror our movements exactly
    frame_height , frame_width , _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        # using rgb frame for the video : cv2.BGR2RGB       
    output = hand_detector.process(rgb_frame)       # to detect hand
    hands = output.multi_hand_landmarks
    if hands:       # for all the landmarks on your hand(21 landmarks)
        for hand in hands:      # goes through every landmark on ur hand
            drawing_utils.draw_landmarks(frame, hand)       # to draw every landmark on ur hand and dispays it on the frame
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):       # to try searching for the index finger
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if(id == 8):        # for the tip of the index finger
                    cv2.circle(img=frame , center=(x,y) , radius=10 , color=(0, 255, 255))      # draw circle around the index fingers
                    index_x = screen_width/frame_width * x
                    index_y = screen_height/frame_height * y
                    pyautogui.moveTo(index_x, index_y)

                if(id == 4):        # for the tip of the thumb to check for the clicking action
                    cv2.circle(img=frame , center=(x,y) , radius=10 , color=(0, 255, 255))      # draw circle around the index fingers
                    thumb_x = screen_width/frame_width * x
                    thumb_y = screen_height/frame_height * y
                    print('outside', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 20:     # if difference between thumb and index is less than 20 than click fucntion is done
                        pyautogui.click()
                        pyautogui.doubleClick()
                        pyautogui.sleep(1)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
