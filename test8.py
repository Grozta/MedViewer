#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from glob import glob

import pandas as pd
from cv2 import cv2

from Operative.Module.seg_test2 import operative_load_model, deal_single_image
from evaluation import dice_coef

if __name__ == '__main__':
    height, width = 1024, 1280  # 1080 1920
    start_h, start_w = 28, 320
    end_h, end_w = start_h + height, start_w + width
    pixels = [1, 2, 3]
    k = 3  # 1 h,w->h,w; 2 h/2,w/2 -> h/2,w/2; 3 h/2,w/2->h,w

    operative_model = operative_load_model()
    print('end of load model')
    for cur_dir in glob(os.path.join('/data/datasets/Robotic_Instrument_Segmentation_Challenge/train', '*')):
        if not os.path.isdir(cur_dir) or 'instrument_dataset_7' in cur_dir:
            continue
        name = os.path.basename(cur_dir)
        img_dir = os.path.join(cur_dir, 'left_frames')
        target_dir = os.path.join(cur_dir, 'ground_truth', 'fuse')
        predict_dir = os.path.join(cur_dir, f'predict{k}')
        os.makedirs(predict_dir, exist_ok=True)

        df = pd.DataFrame(
            columns=['img', 'dice_1', 'dice_2', 'dice_3', 'mean_dice']
        )
        files = os.listdir(img_dir)
        files.sort()
        for idx, file in enumerate(files):
            img = cv2.imread(os.path.join(img_dir, file))[start_h:end_h, start_w:end_w]
            if k != 1:
                img = cv2.resize(img, (width // 2, height // 2))
            seg_mask, origin_seg, seg = deal_single_image(operative_model, img)
            if 3 == k:
                seg_mask = cv2.resize(seg_mask, (width, height), interpolation=cv2.INTER_NEAREST)
            dices = []
            print(os.path.join(img_dir, file))
            for pixel in pixels:
                target = cv2.imread(os.path.join(target_dir, str(pixel), file), 0)[start_h:end_h, start_w:end_w]
                if 2 == k:
                    target = cv2.resize(target, (width // 2, height // 2), interpolation=cv2.INTER_NEAREST)
                dice = dice_coef(target == pixel, seg_mask == pixel)
                dices.append(dice)
            dices.append(sum(dices) / len(dices))
            data = [file] + dices
            df.loc[idx] = data
            cv2.imwrite(os.path.join(predict_dir, file), seg)
        cols = list(df)
        cols.remove('img')
        col_mean = df[cols].mean()
        col_mean['img'] = 'average'
        df = df.append(col_mean, ignore_index=True)
        df.to_csv(os.path.join(cur_dir, '{}_{}{}.csv'.format(name, 'offset', k)), index=False)
