from tkinter import Tk, filedialog
from pdf2image import convert_from_path
from PIL import Image

def upload_files():
    Tk().withdraw()
    file_paths = filedialog.askopenfilenames(
        filetypes=[("PDF and Image files", "*.pdf *.jpg *.jpeg *.png")]
    )
    return file_paths


def process_file(file_path):
    if file_path.endswith('.pdf'):
        return convert_from_path(file_path)  # 返回PDF所有页
    else:
        return [Image.open(file_path)]  # 统一返回列表
