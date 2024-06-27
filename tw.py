from ultralytics import YOLO
import time
# Load a model
model = YOLO('models/yolo/yolov8n-pose.pt')

# Predict with the model
a=time.time()
results = model('image.jpg')
print(time.time()-a)
# Extract keypoint
print(results[0].keypoints.xyn.cpu().numpy())