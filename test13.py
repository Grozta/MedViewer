#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from glob import glob
from itertools import permutations
import numpy as np
from cv2 import cv2

if __name__ == '__main__':
    pixels = [1, 2, 3]
    combination_pixels = list(permutations(pixels, 3))

    train_path = '/data/datasets/Robotic_Instrument_Segmentation_Challenge/train'
    height, width = 1024, 1280  # 1080 1920
    start_h, start_w = 28, 320
    end_h, end_w = start_h + height, start_w + width
    for cur_dir in glob(os.path.join(train_path, '*', 'ground_truth', 'fuse')):
        if 'instrument_dataset_7' in cur_dir:
            continue
        for combination_pixel in combination_pixels:
            os.makedirs(os.path.join(cur_dir, '_'.join(map(str, combination_pixel))), exist_ok=True)
            os.makedirs(os.path.join(cur_dir, '_'.join(map(str, combination_pixel)) + '_resize'), exist_ok=True)
        for file in os.listdir(os.path.join(cur_dir, '1')):
            print(os.path.join(cur_dir, file))
            for combination_pixel in combination_pixels:
                result = np.zeros((height, width), dtype=np.uint8)
                for pixel in combination_pixel:
                    img = cv2.imread(os.path.join(cur_dir, str(pixel), file), 0)[start_h:end_h, start_w:end_w]
                    result[img != 0] = pixel
                cv2.imwrite(os.path.join(cur_dir, '_'.join(map(str, combination_pixel)), file), result)
                result = cv2.resize(result, (width//2, height//2), interpolation=cv2.INTER_NEAREST)
                cv2.imwrite(os.path.join(cur_dir, '_'.join(map(str, combination_pixel)) + '_resize', file), result)
