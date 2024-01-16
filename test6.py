#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from cv2 import cv2

if __name__ == '__main__':
    path = r'G:\data\cropted_train\seq_1\images'
    target = 'target'
    os.makedirs(target, exist_ok=True)

    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file))
        result = cv2.resize(img, (640, 512))
        cv2.imwrite(os.path.join(target, file), result)
