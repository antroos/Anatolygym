import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def extract_key_frames(video_path, step=10):
    """
    Извлекает каждый step-й кадр из видео для упрощённого анализа.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % step == 0:
            frames.append(frame)

        frame_count += 1

    cap.release()
    return frames


def calculate_angle(a, b, c):
    """
    Считает угол (в градусах) между векторами AB и BC, где a, b, c — это [x, y].
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ab = b - a
    bc = c - b

    # Защита от деления на ноль
    if np.linalg.norm(ab) == 0 or np.linalg.norm(bc) == 0:
        return 0.0

    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle


def calculate_angles(landmarks):
    """
    Пример: вычисляем угол (плечо-локоть-запястье) для левой руки.
    В реальном проекте можно добавлять и другие углы (колено, бедро и т.д.).
    """
    left_shoulder = [
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
    ]
    left_elbow = [
        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
    ]
    left_wrist = [
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
    ]

    angle_sew_left = calculate_angle(left_shoulder, left_elbow, left_wrist)

    # Аналогично можно добавить вычисление hip-knee-ankle и т.д.
    # Пока возвращаем пример, где храним один ключ
    return {
        "shoulder-elbow-wrist-left": angle_sew_left
    }
def compare_angles_lists(trainer_angles, client_angles):
    """
    trainer_angles и client_angles — это списки, возвращённые analyze_video().
    Сравниваем их покадрово (по минимальному количеству кадров),
    и считаем разницу углов.
    Возвращаем список словарей вида:
    [
      {
        "shoulder-elbow-wrist-left": {
          "trainer_angle": 165.12,
          "client_angle": 160.34,
          "difference": 4.78
        }
      },
      ...
    ]
    """
    # Определяем, сколько кадров сравним (берём минимальную длину)
    min_len = min(len(trainer_angles), len(client_angles))

    comparison_results = []

    for i in range(min_len):
        frame_diff = {}
        trainer_frame = trainer_angles[i]
        client_frame = client_angles[i]

        # Проходим по всем углам, которые есть в trainer_frame
        for angle_name, trainer_value in trainer_frame.items():
            client_value = client_frame.get(angle_name, None)
            if client_value is not None:
                diff = abs(trainer_value - client_value)
                frame_diff[angle_name] = {
                    "trainer_angle": trainer_value,
                    "client_angle": client_value,
                    "difference": diff
                }
        comparison_results.append(frame_diff)

    return comparison_results


def analyze_video(video_path):
    """
    Извлекает ключевые кадры, считает углы и возвращает список словарей (по кадрам).
    """
    frames = extract_key_frames(video_path, step=10)
    results = []

    with mp_pose.Pose() as pose:
        for frame in frames:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb_frame)

            if result.pose_landmarks:
                lm = result.pose_landmarks.landmark
                angles = calculate_angles(lm)
                results.append(angles)

    return results
