from file_handler import upload_files, process_file
from ocr import extract_text, extract_invoice_info
from excel_writer import write_to_excel
from utils import preprocess_image
import cv2

def main():
    file_paths = upload_files()
    if not file_paths:
        print("未选择文件")
        return

    for file_path in file_paths:
        try:
            images = process_file(file_path)
            for i, image in enumerate(images):
                processed_image = preprocess_image(image)
                text = extract_text(processed_image)
                print(f"OCR识别结果 - 页{i+1}:\n{text}")  # 添加调试信息
                invoice_data = extract_invoice_info(text)

                if invoice_data['发票号码']:
                    write_to_excel(invoice_data)
                else:
                    print(f"{file_path} - 页{i+1}未检测到发票号码，可能识别失败。")
        except Exception as e:
            print(f"处理文件 {file_path} 失败：{e}")

if __name__ == '__main__':
    main()
