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
import traceback

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

    video_path = download_youtube_video(url, "./downloads")

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

from fastapi.responses import StreamingResponse
from io import BytesIO

@app.post("/api/generate-pdf")
async def generate_pdf(request: Request):
    form = await request.form()

    url = form["url"]
    start_time = int(form["startTime"])
    crop_box = json.loads(form["cropBox"])
    image = form["image"]

    # 여기도 영상 다운로드
    video_path = download_youtube_video(url, "./downloads")

    output_pdf_path = os.path.join("./downloads", "output.pdf")
    try:
        process_youtube_video_to_pdf(
            youtube_url=video_path,
            crop_box=crop_box,
            output_pdf_path=output_pdf_path,
            start_time_sec=start_time,
        )
    except Exception as e:
        print("PDF 생성 실패:", e)
        traceback.print_exc()
        return {"error": "PDF 생성 중 오류 발생!"}

    # PDF를 메모리로 읽어서 전송
    with open(output_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=sheet.pdf"
    })
