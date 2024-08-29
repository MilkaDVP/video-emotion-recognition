from ultralytics import YOLO
import time
import os
import pickle
import cv2
# Load a model
model = YOLO('models/yolo/yolov8n-pose.pt')

'''capture = cv2.VideoCapture('video/video3.mp4')
frameNr = 0

while (True):
    success, frame = capture.read()
    if success:
        cv2.imwrite(f'camera/3frame_{frameNr}.jpg', frame)
    else:
        break
    frameNr = frameNr+1
    print(frameNr)
capture.release()'''

for i in (os.listdir('camera/')):
    results = model('camera/'+i)
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        result.save(filename=f"results/{i}")  # save to disk
        with open(f'keypoints/{i}.txt','wb') as file:
            pickle.dump(keypoints.numpy(),file)