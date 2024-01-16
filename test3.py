#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from cv2 import cv2


# 将某个文件夹下面的图片转化为一个视频
def png_to_video(dir_path, output_file):
    fps = 8
    size = (640, 512)
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MJPG'), fps,
                            size, True)
    for i in os.listdir(dir_path):
        if not i.endswith('.png'):
            continue
        img_path = os.path.join(dir_path, i)
        print(img_path)
        img = cv2.imread(img_path)
        video.write(img)


if __name__ == '__main__':
    path = r'target'
    png_to_video(path)
