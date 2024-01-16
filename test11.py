#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from glob import glob

from cv2 import cv2

if __name__ == '__main__':
    train_path = '/data/datasets/Robotic_Instrument_Segmentation_Challenge/train'
    height, width = 1024, 1280  # 1080 1920
    start_h, start_w = 28, 320
    end_h, end_w = start_h + height, start_w + width
    for cur_dir in glob(os.path.join(train_path, '*', 'left_frames')):
        if 'instrument_dataset_7' in cur_dir:
            continue
        target_dir = cur_dir + '_resize'
        os.makedirs(target_dir, exist_ok=True)
        for file in os.listdir(cur_dir):
            print(os.path.join(cur_dir, file))
            img = cv2.imread(os.path.join(cur_dir, file))[start_h:end_h, start_w:end_w]
            img = cv2.resize(img, (640, 512))
            cv2.imwrite(os.path.join(target_dir, file), img)
