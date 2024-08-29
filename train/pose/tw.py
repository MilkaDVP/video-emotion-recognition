import os
import pickle
from ultralytics import YOLO
import cv2
model = YOLO('app_models/pose-recognition/models/yolov8n-pose.pt')

'''capture = cv2.VideoCapture('video/20240828_110029.mp4')
frameNr = 0

while True:
    success, frame = capture.read()
    if success:
        cv2.imwrite(f'camera/fear/2/0frame_{frameNr}.jpg', frame)
    else:
        break
    frameNr = frameNr+1
    print(frameNr)
capture.release()'''

for i in (os.listdir('camera/sad')):
    for j in os.listdir(f'camera/sad/{i}'):
        results = model(f'camera/sad/{i}/{j}')
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            obb = result.obb  # Oriented boxes object for OBB outputs
            with open(f'keypoints/sad/{i}_{j}.txt','wb') as file:
                pickle.dump(keypoints.numpy(),file)