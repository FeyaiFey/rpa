# OCR识别与发票信息提取
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'D:\Programs\Tesseract-OCR\tesseract.exe'

def extract_text(image):
    return pytesseract.image_to_string(image, lang='chi_sim')


def extract_invoice_info(text):
    info = {
        '发票号码': re.search(r'发票号码[:：]?\s*(\d+)', text),
        '发票日期': re.search(r'开票日期[:：]?\s*(\d{4}-\d{1,2}-\d{1,2})', text),
        '销售方': re.search(r'销售方[:：]?\s*([\u4e00-\u9fa5]+)', text),
        '金额': re.search(r'金额[:：]?\s*([\d,]+\.\d+)', text),
        '税率': re.search(r'税率[:：]?\s*([\d]+\%)', text),
        '税额': re.search(r'税额[:：]?\s*([\d,]+\.\d+)', text),
        '价税合计': re.search(r'价税合计[:：]?\s*([\d,]+\.\d+)', text)
    }
    return {k: (v.group(1) if v else '') for k, v in info.items()}
