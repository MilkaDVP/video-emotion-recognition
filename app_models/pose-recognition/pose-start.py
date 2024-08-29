import pickle
from ultralytics import YOLO

model = YOLO('models/yolov8n-pose.pt')

with open('models/nn', 'rb') as file:
    network = pickle.load(file)

result = model(f'photo_5368434800895057164_y.jpg')[0]
keypoints = result.keypoints.numpy().xyn.flatten().tolist()
print(network.predict(keypoints))  # Keypoints object for pose outputs

