from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.youtube_download import download_youtube_video
from backend.utils.frame_extractor import extract_and_crop_frames
import tempfile
import base64
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/get-frame")
async def get_frame(request: Request):
    data = await request.json()
    url = data.get("url")
    start_time = data.get("startTime", 0)
    print(f"받은 유튜브 링크: {url}, 시작 시간: {start_time}")

    # 1. 임시 폴더에 유튜브 영상 다운로드
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = download_youtube_video(url, tmpdir)

        # 2. 첫 프레임 추출 (임시로 전체화면 크롭)
        crop_box = (0, 0, 1280, 720)  # → 임의로 전체화면으로 잡음
        frame_paths = extract_and_crop_frames(video_path, crop_box, start_time_sec=start_time)

        if not frame_paths:
            return {"error": "프레임 추출 실패!"}

        # 3. 첫 프레임을 base64로 변환
        frame_path = frame_paths[0]
        with open(frame_path, "rb") as f:
            img_bytes = f.read()
            base64_str = base64.b64encode(img_bytes).decode("utf-8")
            frame_url = f"data:image/jpeg;base64,{base64_str}"

        return {"frameUrl": frame_url}
