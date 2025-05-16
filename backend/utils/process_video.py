import tempfile
from backend.utils.youtube_download import download_youtube_video
from backend.utils.frame_extractor import extract_and_crop_frames
from backend.utils.pdf_maker import create_pdf_from_images

def process_youtube_video_to_pdf(
    youtube_url: str,
    crop_box,
    output_pdf_path: str,
    start_time_sec: int = 0
):
    images = extract_and_crop_frames(youtube_url, crop_box, start_time_sec=start_time_sec)
    create_pdf_from_images(images, output_pdf_path)
