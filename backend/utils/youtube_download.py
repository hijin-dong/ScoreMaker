import os
import time
import gc
from pathlib import Path
from yt_dlp import YoutubeDL

def download_youtube_video(youtube_url: str, output_dir: str) -> str:
    """
    유튜브 영상을 다운로드하고 병합된 video.mp4 경로를 반환한다.
    이미 존재하면 다운로드 생략.
    """
    # 고정된 output 디렉토리 설정
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path_template = str(output_dir / "video.%(ext)s")
    archive_path = str(output_dir / "download_archive.txt")
    final_video_path = output_dir / "video.mp4"

    if final_video_path.exists():
        print(f"✔ 이미 다운로드된 영상 재사용: {final_video_path}")
        return str(final_video_path)

    ydl_opts = {
        "outtmpl": output_path_template,
        "format": "299+140",  # 고화질 영상 + 오디오
        "merge_output_format": "mp4",
        "download_archive": archive_path,  # 중복 다운로드 방지
        "quiet": True,
        "noplaylist": True,
        "nocheckcertificate": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # yt-dlp가 핸들을 제대로 닫지 않았을 수도 있어서 수동 정리
        del ydl
        gc.collect()

        # 영상 파일이 완전히 닫힐 때까지 대기 (최대 3초)
        for _ in range(30):
            try:
                with open(final_video_path, "rb") as f:
                    break  # 성공적으로 열렸으면 통과
            except PermissionError:
                time.sleep(0.1)

        return str(final_video_path)

    except Exception as e:
        print(f"❌ 유튜브 영상 다운로드 실패: {e}")
        raise
