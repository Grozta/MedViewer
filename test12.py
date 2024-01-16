#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from glob import glob

from cv2 import cv2


def png_to_video(dir_path, output_file, fps=8, size=(640, 512)):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MJPG'), fps,
                            size, True)
    files = glob(os.path.join(dir_path, '*.png'))
    files.sort()
    for file in files:
        img = cv2.imread(file)
        video.write(img)


if __name__ == '__main__':
    train_path = '/data/datasets/Robotic_Instrument_Segmentation_Challenge/train'
    for cur_dir in glob(os.path.join(train_path, '*', 'left_frames_resize')):
        if 'instrument_dataset_7' in cur_dir:
            continue
        filename = os.path.basename(os.path.dirname(cur_dir))
        print(filename)
        target_dir = os.path.join(os.path.dirname(cur_dir), filename + '.avi')
        png_to_video(cur_dir, target_dir)
