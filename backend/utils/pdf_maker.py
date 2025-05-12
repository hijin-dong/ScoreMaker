from img2pdf import convert as img2pdf_convert

def create_pdf_from_images(image_paths: list, output_pdf_path: str):
    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf_convert(image_paths))
