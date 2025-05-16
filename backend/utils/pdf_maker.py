from PIL import Image
from fpdf import FPDF
import os

def create_pdf_from_images(images: list, output_pdf_path: str, per_page=1):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    width, height = 210, 297

    for i in range(0, len(images), per_page):
        imgs = images[i:i + per_page]
        pdf.add_page()
        split_height = height / per_page

        for idx, img_path in enumerate(imgs):
            with Image.open(img_path) as img:
                img = img.convert("RGB")

                tmp_path = f"{img_path}_converted_{idx}.jpg"
                img.save(tmp_path, "JPEG")

                pdf.image(tmp_path, x=10, y=split_height * idx + 10, w=width - 20, h=split_height - 20)

                os.remove(tmp_path)

    pdf.output(output_pdf_path, "F")