import cv2
import os
import tempfile
import numpy as np
from typing import Tuple, List

def is_similar(img1, img2, threshold=30):
    """Returns True if two images are visually similar based on pixel-wise difference."""
    diff = cv2.absdiff(img1, img2)
    mean_diff = np.mean(diff)
    return mean_diff < threshold

def extract_and_crop_frames(
    video_path: str,
    crop_box: Tuple[int, int, int, int],
    start_time_sec: int = 0,
) -> List[str]:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_time_sec * fps)

    frame_interval = int(fps)  # 매 1초마다 프레임 추출
    count = 0
    saved_images = []
    last_saved = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            x, y, w, h = crop_box
            cropped = frame[y:y+h, x:x+w]

            if last_saved is not None and is_similar(last_saved, cropped):
                count += 1
                continue

            last_saved = cropped.copy()
            img_path = os.path.join(tempfile.gettempdir(), f"frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.jpg")
            cv2.imwrite(img_path, cropped)
            saved_images.append(img_path)

        count += 1

    cap.release()
    return saved_images
