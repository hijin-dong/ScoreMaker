from PIL import Image
from fpdf import FPDF
import os

def create_pdf_from_images(images: list, output_pdf_path: str, per_page=1):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    page_width, page_height = 210, 297
    margin = 10
    usable_width = page_width - 2 * margin
    usable_height = page_height - 2 * margin
    slot_height = usable_height / per_page

    for i in range(0, len(images), per_page):
        imgs = images[i:i + per_page]
        pdf.add_page()

        for idx, img_path in enumerate(imgs):
            with Image.open(img_path) as img:
                img = img.convert("RGB")
                img.save("test.png")

                # 이미지의 비율 계산
                img_aspect = img.width / img.height
                slot_aspect = usable_width / slot_height

                # 비율 유지하며 축소
                if img_aspect > slot_aspect:
                    # 이미지가 더 넓을 때 → 너비 맞춤
                    final_width = usable_width
                    final_height = final_width / img_aspect
                else:
                    # 이미지가 더 세로로 길 때 → 높이 맞춤
                    final_height = slot_height
                    final_width = final_height * img_aspect

                # 위치 계산 (중앙 정렬)
                x = (page_width - final_width) / 2
                y = margin + idx * slot_height + (slot_height - final_height) / 2

                # 임시 저장
                tmp_path = f"{img_path}_converted_{idx}.jpg"
                img.resize((int(final_width * 4), int(final_height * 4)), Image.LANCZOS).save(tmp_path, "JPEG")

                pdf.image(tmp_path, x=x, y=y, w=final_width, h=final_height)
                os.remove(tmp_path)

    pdf.output(output_pdf_path, "F")
