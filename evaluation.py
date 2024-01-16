#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from collections import OrderedDict
from glob import glob

import SimpleITK as sitk
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

from util import read_img

smooth = 1.
eps = 1e-15


def dice_coef(y_true, y_pred):
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.sum(y_true_f * y_pred_f)
    return (2. * intersection + eps) / (np.sum(y_true_f) + np.sum(y_pred_f) + eps)


def computeQualityMeasures(lP, lT, only_mean_dice=True):
    """
    Binary [0,1]
    """
    quality = dict()
    try:
        labelPred = sitk.GetImageFromArray(lP, isVector=False)
        labelTrue = sitk.GetImageFromArray(lT, isVector=False)

        dicecomputer = sitk.LabelOverlapMeasuresImageFilter()
        dicecomputer.Execute(labelTrue > 0.5, labelPred > 0.5)
        quality["dice"] = dicecomputer.GetDiceCoefficient()

        if not only_mean_dice:
            hausdorffcomputer = sitk.HausdorffDistanceImageFilter()
            hausdorffcomputer.Execute(labelTrue > 0.5, labelPred > 0.5)
            quality["avgHausdorff"] = hausdorffcomputer.GetAverageHausdorffDistance()
            quality["Hausdorff"] = hausdorffcomputer.GetHausdorffDistance()

            quality['acc'] = accuracy_score(lT.reshape(-1), lP.reshape(-1))
            quality["pred_pixel_num"] = len(lP[lP == 1])
            quality["target_pixel_num"] = len(lT[lT == 1])
        return quality
    except Exception as e:
        quality = dict()
        print('Exception: ', e)
        if only_mean_dice:
            quality["dice"] = 1
            return quality
        quality["avgHausdorff"] = 0
        quality["Hausdorff"] = 0
        quality["acc"] = 0
        quality["pred_pixel_num"] = 0
        quality["target_pixel_num"] = 0
        return quality


def computeQualityMeasures_oneCases(pred, target, classes, only_mean_dice=True):
    one_case_qualities = OrderedDict()

    if classes is not None:
        range_right = classes + 1
    else:
        range_right = target.max() + 1
    for i in range(1, range_right):
        class_pred = np.zeros_like(pred)
        class_target = np.zeros_like(target)
        class_pred[pred == i] = 1
        class_target[target == i] = 1

        class_quality = computeQualityMeasures(class_pred, class_target, only_mean_dice)
        one_case_qualities[i] = class_quality

    if not only_mean_dice:
        pred[pred > 1] = 1
        target[target > classes] = 0
        target[target > 1] = 1
        assert len(np.unique(pred)) == 2
        assert len(np.unique(target)) == 2
        one_case_qualities['whole'] = computeQualityMeasures(pred, target)
    del pred, target

    dices = [one_case_qualities[i]["dice"] for i in range(1, range_right)]
    dices = np.array(dices)

    if not only_mean_dice:
        hausdorffs = [one_case_qualities[i]["Hausdorff"] for i in range(1, range_right)]
        hausdorffs = np.array(hausdorffs)

        accs = [one_case_qualities[i]["acc"] for i in range(1, range_right)]
        accs = np.array(accs)

        pixel_nums = [one_case_qualities[i]["target_pixel_num"] for i in range(1, range_right)]
        pixel_nums = np.array(pixel_nums)

    mean_dice = dices.mean()
    if not only_mean_dice:
        mean_hausdorff = hausdorffs.mean()
        weighted_mean_hausdorff = (pixel_nums * hausdorffs).sum() / pixel_nums.sum()
        weighted_mean_dice = (pixel_nums * dices).sum() / pixel_nums.sum()
        mean_acc = accs.mean()
        weighted_mean_acc = (pixel_nums * accs).sum() / pixel_nums.sum()

    one_case_qualities["mean_dice"] = mean_dice
    if not only_mean_dice:
        one_case_qualities["mean_hausdorff"] = mean_hausdorff
        one_case_qualities["mean_acc"] = mean_acc
        one_case_qualities["weighted_mean_hausdorff"] = weighted_mean_hausdorff
        one_case_qualities["weighted_mean_dice"] = weighted_mean_dice
        one_case_qualities["weighted_mean_acc"] = weighted_mean_acc

    # for i in range(range_right, 5):
    #     one_case_qualities[i] = dict()
    #     one_case_qualities[i]["Hausdorff"] = 0
    #     one_case_qualities[i]["dice"] = 1
    for i in range(1, range_right):
        print('{}: {}'.format(i, one_case_qualities[i]))

    print('mean_dice: ', one_case_qualities['mean_dice'])
    if not only_mean_dice:
        print('mean_hausdorff: ', one_case_qualities['mean_hausdorff'])
        print('mean_acc: ', one_case_qualities['mean_acc'])
    print('-' * 33, '\n')

    return one_case_qualities


def directory_dice(pred_path, target_path, classes, result_path, callback=None):
    """
    按顺序计算两个目录的dice

    :param pred_path: 预测目录
    :param target_path: 测试目录
    :param classes: 类别数量
    :param result_path: 保存的文件
    :param callback: 回调，callback(int),返回处理百分比
    """
    try:
        pred_files = glob(os.path.join(pred_path, '*'))
        target_files = glob(os.path.join(target_path, '*'))
        if len(pred_files) != len(target_files):
            return -1
        pred_files.sort()
        target_files.sort()
        columns = ['Image', 'Segmentation', 'Dice(%)']
        df = pd.DataFrame(
            columns=columns
        )
        cnt = 0
        total_dice = 0
        total_len = len(pred_files)
        for idx, (pred_file, target_file) in enumerate(zip(pred_files, target_files)):
            if not os.path.exists(pred_path) or not os.path.exists(target_file):
                continue
            cnt += 1
            pred = sitk.GetArrayFromImage(read_img(pred_file))
            target = sitk.GetArrayFromImage(read_img(target_file))
            one_case_qualities = computeQualityMeasures_oneCases(pred, target, classes)
            total_dice += one_case_qualities['mean_dice']
            df.loc[idx] = [
                os.path.basename(pred_file),
                os.path.basename(target_file),
                '{:.1f}'.format(one_case_qualities['mean_dice'] * 100)
            ]
            if idx + 1 < total_len and callback is not None:
                callback(100. * (idx + 1) // total_len)
        ext = os.path.splitext(result_path)[-1]

        average_row = [pd.NA] * len(df.columns)
        average_row[0] = 'Mean'
        average_row[-1] = '{:.1f}'.format(total_dice * 100. / cnt)
        df2 = pd.DataFrame(
            [average_row], columns=df.columns
        )

        df = pd.concat([df2, df])
        # df = df.append(pd.Series({
        #     columns[0]: 'mean',
        #     columns[-1]: '{:.1f}'.format(total_dice*100. / cnt)
        # }), ignore_index=True)
        # print(df)
        if '.csv' == ext:
            df.to_csv(result_path, index=False)
        elif ext in ['.xlsx', '.xls']:
            df.to_excel(result_path, index=False)
        return 0
    except:
        pass
    finally:
        if callback is not None:
            callback(100)


if __name__ == '__main__':
    pred = sitk.GetArrayFromImage(read_img('predict_label/pelvic/dataset5_1411226_Image.nii.gz'))
    target = sitk.GetArrayFromImage(read_img('img/dataset5_1411226_Image_mask_4label.nii.gz'))

    one_case_qualities = computeQualityMeasures_oneCases(pred, target, 3, only_mean_dice=False)
    print(one_case_qualities)
    print(one_case_qualities['mean_dice'])
