import os
from PIL import Image
from pdf2image import convert_from_path

def process_file(file_path):
    output_dir = r"D:\PythonProject\train\invoice"
    os.makedirs(output_dir, exist_ok=True)

    if file_path.endswith('.pdf'):
        images = convert_from_path(file_path)
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f"{os.path.basename(file_path)}_page_{i+1}.png")
            image.save(image_path)
        return images
    else:
        # image = Image.open(file_path)
        # image_path = os.path.join(output_dir, os.path.basename(file_path))
        # image.save(image_path)
        return 

path = r"D:\PythonProject\train\电子发票"

def get_file_path(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

file_list = get_file_path(path)
for file in file_list:
    process_file(file)