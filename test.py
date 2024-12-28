import cv2
import numpy as np

def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 对四个点进行排序
def order_points(pts):
    rect = np.zeros((4, 2), dtype='float32') # 初始化一个矩形
    # 按顺序找到对应坐标
    s = np.sum(pts, axis=1) # 对pts矩阵的每一行求和
    rect[0] = pts[np.argmin(s)] # 求和最小的是左上角
    rect[2] = pts[np.argmax(s)] # 求和最大的是右下角
    diff = np.diff(pts, axis=1) # 对pts矩阵的每一行求差
    rect[1] = pts[np.argmin(diff)] # 求差最小的是右上角
    rect[3] = pts[np.argmax(diff)] # 求差最大的是左下角
    return rect

# 透视变换
def four_point_transform(image, pts):
    # 获取输入坐标点
    rect = order_points(pts)
    (tl, tr, br, bl) = rect # 左上 右上 右下 左下
    # 计算两个可能的宽度，取这两个宽度的最大值作为新图像的宽度
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2)) # 右下角和左下角的距离
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2)) # 右上角和左上角的距离
    maxWidth = max(int(widthA), int(widthB)) # 取两个宽度的最大值
    # 计算两个可能的高度，取这两个高度的最大值作为新图像的高度
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2)) # 右上角和右下角的距离
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2)) # 左上角和左下角的距离
    maxHeight = max(int(heightA), int(heightB)) # 取两个高度的最大值
    # 变换后对应坐标位置
    dst = np.array([
        [0, 0], # 左上角
        [maxWidth - 1, 0], # 右上角
        [maxWidth - 1, maxHeight - 1], # 右下角
        [0, maxHeight - 1] # 左下角
    ], dtype='float32')
    # 计算变换矩阵
    M = cv2.getPerspectiveTransform(rect, dst)
    # 进行变换
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # 返回变换后结果
    return warped

# 缩小图片
def resize_image(image, width=None, height=None):
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    else:
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

image = cv2.imread('test.png')
cv_show('img', image)

ratio = image.shape[0] / 500.0
orig = image.copy()
resized_image = resize_image(orig, width=800)
cv_show('1', resized_image)


# 轮廓检测
print('step 1 : 轮廓检测')
gray = cv2.cvtColor(resized_image,cv2.COLOR_BGR2GRAY)  # 灰度图
#二值化处理
edged = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 自动寻找网值二位化
#检测二值化图像中的轮廓。
cnts = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[1]

if cnts:
    # 绘制轮廓
    image_contours = cv2.drawContours(resized_image.copy(), cnts, -1, (0, 0, 255), 1)
    cv_show('image_contours', image_contours)
else:
    print("未检测到任何轮廓")
#绘制轮廓
# image_contours = cv2.drawContours(resized_image.copy(),cnts,-1,(0,0,255),1)
# cv_show('image_contours',image_contours)

"""
# 轮廓检测
print('轮廓检测')
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY) # 灰度图
cv_show('gray', gray)
# 二值化处理
edged = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] # 二值化 自动寻找网值二位化
cv_show('edged', edged)
# 检测二值化图像的轮廓
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1] # 寻找轮廓
# 绘制轮廓
image_contours = cv2.drawContours(resized_image.copy(), cnts, -1, (0, 255, 0), 2) # 绘制轮廓
cv_show('contours', image_contours)
"""
"""
# 转换为灰度图
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
# 高斯模糊（去除噪声）
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 二值化
_, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

# 轮廓检测
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍历轮廓，筛选合适的矩形区域
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    
    # 过滤小区域，只保留较大矩形
    if w > 100 and h > 50:  # 调整阈值适配发票区域
        cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绿色框

# 显示结果
cv2.imshow('Detected Areas', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""