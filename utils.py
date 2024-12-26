# 图像预处理模块
import cv2
import numpy as np

def preprocess_image(image):
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    image_cv = cv2.medianBlur(image_cv, 3)
    _, binary = cv2.threshold(image_cv, 150, 255, cv2.THRESH_BINARY)
    return binary
