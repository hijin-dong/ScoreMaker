import os
import yt_dlp

def download_youtube_video(url: str, output_path: str) -> str:
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(output_path, 'video.%(ext)s'),
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir(output_path):
        if file.endswith('.mp4'):
            return os.path.join(output_path, file)
    raise FileNotFoundError("Video not downloaded")
