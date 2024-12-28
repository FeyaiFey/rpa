from tkinter import Tk, filedialog
from pdf2image import convert_from_path
from PIL import Image
import os

def upload_files():
    Tk().withdraw()
    file_paths = filedialog.askopenfilenames(
        filetypes=[("PDF and Image files", "*.pdf *.jpg *.jpeg *.png")]
    )
    return file_paths

def process_file(file_path):
    output_dir = 'processed_images'
    os.makedirs(output_dir, exist_ok=True)

    if file_path.endswith('.pdf'):
        images = convert_from_path(file_path)
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f"{os.path.basename(file_path)}_page_{i+1}.png")
            image.save(image_path)
        return images
    else:
        image = Image.open(file_path)
        image_path = os.path.join(output_dir, os.path.basename(file_path))
        image.save(image_path)
        return [image]
