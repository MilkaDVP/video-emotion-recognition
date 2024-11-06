import cv2
import mediapipe as mp
import numpy as np

def extract_pose_landmarks_from_frame(frame, model_complexity=0):
    # Initialize Mediapipe Pose with adjustable model complexity
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, model_complexity=model_complexity, enable_segmentation=False, min_detection_confidence=0.5)

    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    def get_landmark_coords(landmark):
        return [landmark.x, landmark.y, landmark.z, 0, 0, 0]  # Positions (x, y, z) with dummy rotations

    # List of landmarks names and mapping to Mediapipe landmarks
    landmark_names = [
        'SpineBase', 'SpineMid', 'Neck', 'Head', 'ShoulderLeft', 'ElbowLeft', 'WristLeft', 'HandLeft',
        'ShoulderRight', 'ElbowRight', 'WristRight', 'HandRight', 'HipLeft', 'KneeLeft', 'AnkleLeft', 'FootLeft',
        'HipRight', 'KneeRight', 'AnkleRight', 'FootRight', 'SpineShoulder', 'HandTipLeft', 'ThumbLeft', 'HandTipRight', 'ThumbRight'
    ]
    landmark_mapping = {
        'SpineBase': mp_pose.PoseLandmark.LEFT_HIP, 'SpineMid': mp_pose.PoseLandmark.RIGHT_HIP,
        'Neck': mp_pose.PoseLandmark.LEFT_SHOULDER, 'Head': mp_pose.PoseLandmark.NOSE,
        'ShoulderLeft': mp_pose.PoseLandmark.LEFT_SHOULDER, 'ElbowLeft': mp_pose.PoseLandmark.LEFT_ELBOW,
        'WristLeft': mp_pose.PoseLandmark.LEFT_WRIST, 'HandLeft': mp_pose.PoseLandmark.LEFT_PINKY,
        'ShoulderRight': mp_pose.PoseLandmark.RIGHT_SHOULDER, 'ElbowRight': mp_pose.PoseLandmark.RIGHT_ELBOW,
        'WristRight': mp_pose.PoseLandmark.RIGHT_WRIST, 'HandRight': mp_pose.PoseLandmark.RIGHT_PINKY,
        'HipLeft': mp_pose.PoseLandmark.LEFT_HIP, 'KneeLeft': mp_pose.PoseLandmark.LEFT_KNEE,
        'AnkleLeft': mp_pose.PoseLandmark.LEFT_ANKLE, 'FootLeft': mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
        'HipRight': mp_pose.PoseLandmark.RIGHT_HIP, 'KneeRight': mp_pose.PoseLandmark.RIGHT_KNEE,
        'AnkleRight': mp_pose.PoseLandmark.RIGHT_ANKLE, 'FootRight': mp_pose.PoseLandmark.RIGHT_FOOT_INDEX,
        'SpineShoulder': mp_pose.PoseLandmark.LEFT_SHOULDER, 'HandTipLeft': mp_pose.PoseLandmark.LEFT_INDEX,
        'ThumbLeft': mp_pose.PoseLandmark.LEFT_THUMB, 'HandTipRight': mp_pose.PoseLandmark.RIGHT_INDEX,
        'ThumbRight': mp_pose.PoseLandmark.RIGHT_THUMB
    }

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        row = []
        for name in landmark_names:
            landmark_idx = landmark_mapping[name].value
            coords_and_rotation = get_landmark_coords(landmarks[landmark_idx])
            row.extend(coords_and_rotation)
        return np.array([row])
    else:
        print("No pose landmarks detected.")
        return None
