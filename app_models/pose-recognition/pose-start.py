import os
import warnings
import logging
import time
import cv2
import torch
from keypoints import extract_pose_landmarks_from_frame

# Устанавливаем уровень логирования
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)

# Загружаем предобученную модель
model = torch.load('app_models/pose-recognition/models/model.pt')

# Инициализация захвата видео
cap = cv2.VideoCapture(2)

# Устанавливаем более низкое разрешение видео
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # например, 640x480
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Счетчик кадров для уменьшения частоты обработки поз
frame_counter = 0
process_every_n_frames = 2  # Обрабатывать каждый второй кадр для увеличения FPS

while cap.isOpened():
    start_time = time.time()  # Начало замера для всего цикла

    # 1. Захват кадра
    ret, frame = cap.read()
    if not ret:
        print("Не удалось захватить кадр")
        break
    capture_time = time.time() - start_time  # Время на захват кадра

    # Обрабатываем только каждый n-й кадр
    if frame_counter % process_every_n_frames == 0:
        # 2. Извлечение позы
        pose_start_time = time.time()
        pose_data = extract_pose_landmarks_from_frame(frame, model_complexity=1)  # Снизили сложность модели
        pose_time = time.time() - pose_start_time  # Время на извлечение позы

        # 3. Предсказание
        prediction_time = 0
        if pose_data is not None:
            pred_start_time = time.time()
            prediction = model.predict(pose_data)
            prediction_time = time.time() - pred_start_time  # Время на предсказание
            print(f"Prediction: {prediction}")
        else:
            print("Нет данных позы для предсказания.")
    else:
        pose_time, prediction_time = 0, 0  # Пропускаем кадры без обработки

    # Отображение кадра
    display_start_time = time.time()
    cv2.imshow("Pose Detection", frame)
    display_time = time.time() - display_start_time  # Время на отображение кадра

    # Расчет общего времени цикла
    total_time = time.time() - start_time
    print(f"Время цикла: {total_time:.3f}s | Захват: {capture_time:.3f}s | Позы: {pose_time:.3f}s | Предсказание: {prediction_time:.3f}s | Отображение: {display_time:.3f}s")

    # Завершаем при нажатии 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_counter += 1  # Увеличиваем счетчик кадров

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
