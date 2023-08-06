import cv2,os
import numpy as np

def taiac(img_path,imwrite_path=None):
    if not imwrite_path:
        imwrite_path='save_img.'+img_path.split('.')[-1]

    # 读取图片
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    # imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 转为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # 查找轮廓
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # 找到最大轮廓
    max_contour = max(contours, key=cv2.contourArea)

    # 计算最小外接矩形
    rect = cv2.minAreaRect(max_contour)

    # 获取旋转角度
    rect_3=rect[-1]
    if rect_3>45:
        angle = rect[-1] - 90
    elif rect_3<-45:
        angle = rect[-1] + 90
    else:
        angle = rect_3

    # 旋转图像
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    old_name='cv2imwrite.'+imwrite_path.split('.')[-1]
    cv2.imwrite(old_name, rotated)
    os.rename(old_name, imwrite_path)#解决cv2无法保存路径存在中文的问题