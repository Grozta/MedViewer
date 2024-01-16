#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from glob import glob

import numpy as np
from cv2 import cv2

if __name__ == '__main__':
    # img_dir = '/media/icml-hqu/My Passport/TDSNet-master/data/cropted_train/seq_1/instruments_masks'
    train_path = '/data/datasets/Robotic_Instrument_Segmentation_Challenge/train'
    # /media/icml-hqu/My Passport/datasets/Robotic_Instrument_Segmentation_Challenge/train/instrument_1_4_training
    ans = {None, 0, 10, 20, 30, 40}
    for cur_dir in glob(os.path.join(train_path, '*', 'ground_truth')):
        if 'instrument_dataset_7' in cur_dir:
            continue
        dirs = glob(os.path.join(cur_dir, '*'))
        fuse_dir = os.path.join(cur_dir, 'fuse')
        os.makedirs(fuse_dir, exist_ok=True)
        if fuse_dir in dirs:
            dirs.remove(fuse_dir)
        for i in [10, 20, 30]:
            os.makedirs(os.path.join(fuse_dir, str(i//10)), exist_ok=True)
        for file in os.listdir(dirs[0]):
            imgs = {
                10: np.zeros((1080, 1920, 3), dtype=np.uint8),
                20: np.zeros((1080, 1920, 3), dtype=np.uint8),
                30: np.zeros((1080, 1920, 3), dtype=np.uint8)
            }
            print(os.path.join(fuse_dir, file))
            for type_dir in dirs:
                cur_img = cv2.imread(os.path.join(type_dir, file))
                for k in imgs.keys():
                    imgs[k][cur_img == k] = k//10

            for k, v in imgs.items():
                cv2.imwrite(os.path.join(fuse_dir, str(k//10), file), v)
