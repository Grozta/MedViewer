#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from scipy import ndimage
from skimage.measure import label


def del_threshold(empt, thre: int):
    empts = label(empt)
    for j in range(1, empts.max() + 1):
        if np.count_nonzero(empts == j) < thre:
            empt[empts == j] = 0
    return empt.astype(np.uint8)


def pre_proc(img):
    if len(img.shape) == 3:
        img = img.astype(np.uint8)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif len(img.shape) == 2:
        gray = img
    else:
        print("img mistake!!!!!")

    # OpenCV定义的结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    # 膨胀图像
    gray = cv2.dilate(gray, kernel)
    # 腐蚀图像
    gray = cv2.erode(gray, kernel)
    return gray


def mark(img, class_color, show="None", thre=500, size=2, fontScale=0.8, size_=2):
    """
    show="rect" or "min_rect" or "contours" or "None"
    thre "Discard the connected region less than the threshold"
    size "thickness of the line"
    size_ "thickness of the text"
    fontScale "size of the text"
    """
    gray = pre_proc(img)
    # print(gray)
    labs = list(np.unique(gray))
    # print(labs)
    labs.remove(0)
    if 1 in labs or 2 in labs or 3 in labs:
        class_ = labs
    else:
        class_ = ([i // 85 for i in labs])

    for i, c in enumerate(class_):
        if c == 1:
            class_[i] = "柄"
        elif c == 2:
            class_[i] = "铰链"
        elif c == 3:
            class_[i] = "夹子"

    # print(class_)
    contours_list = []
    for index, lab in enumerate(labs):
        empt = np.zeros(shape=gray.shape)
        empt[gray == lab] = 255
        empt = ndimage.binary_fill_holes(empt).astype(np.uint8)
        empts = del_threshold(empt, thre)
        # print(np.unique(empts))
        contours, hierarchy = cv2.findContours(empts, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_list.append(contours)
        # print(len(contours))
        # for i in range(len(contours)):
        #
        #     if show == "min_rect":  # 画最小外接矩形
        #         min_rect = cv2.minAreaRect(np.array(contours[i]))
        #         box = cv2.boxPoints(min_rect)  # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
        #         box = np.int0(box)
        #         cv2.drawContours(img, [box], 0, class_color[index], size)
        #
        #         left_point_x = np.min(box[:, 0])
        #         right_point_x = np.max(box[:, 0])
        #         top_point_y = np.min(box[:, 1])
        #         bottom_point_y = np.max(box[:, 1])
        #         point = ((right_point_x - left_point_x) // 2 + left_point_x, top_point_y - size_ * 5)
        #
        #     elif show == "rect":  # 画外接矩形
        #         x, y, w, h = cv2.boundingRect(contours[i])
        #         img = cv2.rectangle(img, (x, y), (x + w, y + h), class_color[index], size)
        #         point = ((x + w // 2), y - size_ * 5)
        #
        #     elif show == "contours":  # 画轮廓
        #         img = cv2.drawContours(img.copy(), contours, i, class_color[index], size)
        #         x, y, w, h = cv2.boundingRect(contours[i])
        #         point = ((x + w // 2), y - size_ * 5)
        #     else:  # 不做操作
        #         x, y, w, h = cv2.boundingRect(contours[i])
        #         point = ((x + w // 2), y - size_ * 5)
        #
        #     font = cv2.FONT_HERSHEY_SIMPLEX
        #     text = class_[index]
        #     # print(index, text, type(text))
        #     img = cv2.putText(img, text, point, font, fontScale, class_color[index], size_)  # 标出器械名字

    img = Image.fromarray(cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB))
    fontStyle = ImageFont.truetype(
        "simsun.ttc", 20, encoding="utf-8")
    for index, label in enumerate(labs):
        contours = contours_list[index]
        for i in range(len(contours)):
            if show == "min_rect":  # 画最小外接矩形
                min_rect = cv2.minAreaRect(np.array(contours[i]))
                box = cv2.boxPoints(min_rect)  # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, class_color[index], size)

                left_point_x = np.min(box[:, 0])
                right_point_x = np.max(box[:, 0])
                top_point_y = np.min(box[:, 1])
                bottom_point_y = np.max(box[:, 1])
                point = ((right_point_x - left_point_x) // 2 + left_point_x, top_point_y - size_ * 5)

            elif show == "rect":  # 画外接矩形
                x, y, w, h = cv2.boundingRect(contours[i])
                img = cv2.rectangle(img, (x, y), (x + w, y + h), class_color[index], size)
                point = ((x + w // 2), y - size_ * 5)

            elif show == "contours":  # 画轮廓
                img = cv2.drawContours(img.copy(), contours, i, class_color[index], size)
                x, y, w, h = cv2.boundingRect(contours[i])
                point = ((x + w // 2), y - size_ * 5)
            else:  # 不做操作
                x, y, w, h = cv2.boundingRect(contours[i])
                point = ((x + w // 2), y - size_ * 5)

            # font = cv2.FONT_HERSHEY_SIMPLEX
            text = class_[index]
            # print(index, text, type(text))
            # img = cv2.putText(img, text, point, font, fontScale, class_color[index], size_)  # 标出器械名字
            draw = ImageDraw.Draw(img)
            draw.text(point, text, tuple(class_color[index][::-1]), font=fontStyle)

    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img


if __name__ == "__main__":
    class_color = [[0, 0, 205], [255, 255, 0], [125, 255, 12],
                   [255, 55, 0], [24, 55, 125], [187, 155, 25], [0, 255, 125], [255, 255, 125],
                   [123, 15, 175], [124, 155, 5], [12, 255, 141]]

    img = cv2.imread(r"test.png")
    img = mark(img, show="None", thre=500, size=3, fontScale=0.7, size_=2, class_color=class_color)
    cv2.imshow("draw_img0", img)
    # print(cv2.getWindowImageRect(img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
