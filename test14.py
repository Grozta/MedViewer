#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from glob import glob
from itertools import permutations

import pandas as pd
import numpy as np
from cv2 import cv2

from evaluation import dice_coef
from Operative.Module.seg_test2 import operative_load_model, deal_single_image

if __name__ == '__main__':
    height, width = 1024, 1280  # 1080 1920
    start_h, start_w = 28, 320
    end_h, end_w = start_h + height, start_w + width
    pixels = [1, 2, 3]
    combination_pixels = list(permutations(pixels, 3))

    operative_model = operative_load_model()
    print('end of load model')
    for cur_dir in glob(os.path.join('/data/datasets/Robotic_Instrument_Segmentation_Challenge/train', '*')):
        if not os.path.isdir(cur_dir) or 'instrument_dataset_7' in cur_dir:
            continue
        name = os.path.basename(cur_dir)
        img_dir = os.path.join(cur_dir, 'left_frames_resize')
        target_dir = os.path.join(cur_dir, 'ground_truth', 'fuse')
        predict_dir = os.path.join(cur_dir, 'predict2')
        os.makedirs(predict_dir, exist_ok=True)

        df = {}
        for combination_pixel in combination_pixels:
            k = '_'.join(map(str, combination_pixel))
            df[k] = pd.DataFrame(
                columns=['img', 'dice_1', 'dice_2', 'dice_3', 'mean_dice']
            )
            df[k + '_resize'] = pd.DataFrame(
                columns=['img', 'dice_1', 'dice_2', 'dice_3', 'mean_dice']
            )
        files = os.listdir(img_dir)
        files.sort()
        for idx, file in enumerate(files):
            print(os.path.join(img_dir, file))
            img = cv2.imread(os.path.join(img_dir, file))
            seg_mask, origin_seg, seg = deal_single_image(operative_model, img)
            seg_mask_resize = cv2.resize(seg_mask, (width, height), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(os.path.join(predict_dir, file), seg)
            for combination_pixel in combination_pixels:
                k = '_'.join(map(str, combination_pixel))
                dices = []
                for pixel in pixels:
                    target = cv2.imread(os.path.join(target_dir, k + '_resize', file), 0)
                    dice = dice_coef(target == pixel, seg_mask == pixel)
                    dices.append(dice)
                dices.append(sum(dices) / len(dices))
                data = [file] + dices
                df[k + '_resize'].loc[idx] = data

                dices = []
                for pixel in pixels:
                    target = cv2.imread(os.path.join(target_dir, k, file), 0)
                    dice = dice_coef(target == pixel, seg_mask_resize == pixel)
                    dices.append(dice)
                dices.append(sum(dices) / len(dices))
                data = [file] + dices
                df[k].loc[idx] = data

        excel_writer = pd.ExcelWriter(os.path.join(cur_dir, 'result.xlsx'))
        for combination_pixel in combination_pixels:
            k = '_'.join(map(str, combination_pixel))
            cols = list(df[k])
            cols.remove('img')
            col_mean = df[k][cols].mean()
            col_mean['img'] = 'average'
            df[k] = df[k].append(col_mean, ignore_index=True)
            df[k].to_excel(excel_writer, index=False, sheet_name=k)

            k += '_resize'
            col_mean = df[k][cols].mean()
            col_mean['img'] = 'average'
            df[k] = df[k].append(col_mean, ignore_index=True)
            df[k].to_excel(excel_writer, index=False, sheet_name=k)
        excel_writer.save()
