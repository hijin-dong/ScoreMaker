import cv2
import os
import tempfile
from typing import Tuple

def extract_and_crop_frames(
    video_path: str,
    crop_box: Tuple[int, int, int, int],
    start_time_sec: int = 0,
    frame_interval: int = 30
) -> list:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_time_sec * fps)

    count = 0
    saved_images = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            x, y, w, h = crop_box
            cropped = frame[y:y+h, x:x+w]
            img_path = os.path.join(tempfile.gettempdir(), f"frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.jpg")
            cv2.imwrite(img_path, cropped)
            saved_images.append(img_path)
        count += 1

    cap.release()
    return saved_images
