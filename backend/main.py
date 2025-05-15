from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend.utils.youtube_download import download_youtube_video
from backend.utils.frame_extractor import extract_and_crop_frames
from backend.utils.process_video import process_youtube_video_to_pdf
import tempfile
import base64
import cv2
import json
import os

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

    # 임시 폴더에 유튜브 영상 다운로드
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = download_youtube_video(url, tmpdir)

        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        crop_box = (0, 0, width, height)

        frame_paths = extract_and_crop_frames(video_path, crop_box, start_time_sec=start_time)

        if not frame_paths:
            return {"error": "프레임 추출 실패!"}

        # 첫 프레임을 base64로 변환
        frame_path = frame_paths[0]
        with open(frame_path, "rb") as f:
            img_bytes = f.read()
            base64_str = base64.b64encode(img_bytes).decode("utf-8")
            frame_url = f"data:image/jpeg;base64,{base64_str}"

        return {"frameUrl": frame_url}

@app.post("/api/generate-pdf")
async def generate_pdf(request: Request):
    form = await request.form()

    # 폼데이터에서 항목 추출
    url = form["url"]
    start_time = int(form["startTime"])
    crop_box = json.loads(form["cropBox"])  # [x, y, w, h]
    
    # 이미지 파일은 "image" 키로 전달됨
    image = form["image"]  # 현재는 업로드만 받고 사용 안 함

    with tempfile.TemporaryDirectory() as tmpdir:
        output_pdf_path = os.path.join(tmpdir, "output.pdf")
        try:
            process_youtube_video_to_pdf(
                youtube_url=url,
                crop_box=crop_box,
                output_pdf_path=output_pdf_path,
                start_time_sec=start_time,
            )
        except Exception as e:
            print("PDF 생성 실패:", e)
            return {"error": "PDF 생성 중 오류 발생!"}

        return FileResponse(output_pdf_path, media_type="application/pdf", filename="sheet.pdf")
