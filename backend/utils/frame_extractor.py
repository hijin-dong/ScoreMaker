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
    crop_box: Tuple[int, int, int, int] = (0, 0, 1, 1),
    start_time_sec: int = 0,
    save_dir: str = None  # ✅ 새 인자 추가
) -> List[str]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"비디오 파일을 열 수 없습니다: {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_time_sec * fps)

    frame_interval = int(fps)
    count = 0
    saved_images = []
    last_saved = None

    if save_dir is None:
        save_dir = tempfile.gettempdir()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            height, width, _ = frame.shape

            frame_height, frame_width = frame.shape[:2]
            rel_x, rel_y, rel_w, rel_h = crop_box  # 0~1 값

            if not (0 <= rel_x <= 1 and 0 <= rel_y <= 1 and 0 <= rel_w <= 1 and 0 <= rel_h <= 1):
                rel_x, rel_y, rel_w, rel_h = 0, 0, 1, 1

            x = int(rel_x * frame_width)
            y = int(rel_y * frame_height)
            w = int(rel_w * frame_width)
            h = int(rel_h * frame_height)

            if w <= 0 or h <= 0 or x + w > frame_width or y + h > frame_height:
                print(f"잘못된 크롭 영역: x={x}, y={y}, w={w}, h={h}, frame={frame_width}x{frame_height}")
                count += 1
                continue

            cropped = frame[y:y+h, x:x+w]

            if last_saved is not None and is_similar(last_saved, cropped):
                count += 1
                continue

            last_saved = cropped.copy()
            img_path = os.path.join(save_dir, f"frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.jpg")
            cv2.imwrite(img_path, cropped)
            saved_images.append(img_path)

        count += 1

    cap.release()
    return saved_images

