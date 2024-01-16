#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import time

import SimpleITK as sitk
import pandas as pd

from evaluation import computeQualityMeasures_oneCases
from util import read_img


def batch_segmentation(path, root, seg_method, save_path, result_path, classes, callback=None):
    """
    批量分割,并计算dice

    :param path: 待处理路径（支持csv,xls,xlsx）
    :param root: 根目录
    :param seg_method 分割方法（要求第一个参数是图片路径，并且有save_path参数,其他参数必须有默认值）
    :param save_path: 保存路径
    :param result_path: 结果excel路径（支持csv,xls,xlsx）
    :param classes: 类别个数
    :param callback: 回调，callback(int),返回处理百分比
    """
    try:
        ext = os.path.splitext(path)[-1]
        if '.csv' == ext:
            df = pd.read_csv(path)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(path)
        else:
            print('unsupported input type')
            return -1
        # if not os.path.isdir(save_path):
        #     print('not a directory')
        #     return -2
        os.makedirs(save_path, exist_ok=True)
        ext = os.path.splitext(result_path)[-1]
        if ext not in ['.csv', '.xlsx', '.xls']:
            print('unsupported output type')
            return -3
        if seg_method is None:
            return -4
        columns = list(df.columns)
        if 0 == len(columns):
            return 0
        elif 1 == len(columns):
            image_index, seg_index = columns[0], None
        else:
            image_index, seg_index = columns[:2]
        # df[['result', 'time', 'dice']] = pd.DataFrame([[pd.NA] * 3], index=df.index)
        cnt = 0
        total_dice = 0
        total_time = 0
        total_cnt = 0
        total_len = len(df)
        for idx, data in df.iterrows():
            total_cnt += 1
            # df.loc[idx, ['result', 'time', 'dice']] = [1, 2, 3]
            image_path = os.path.join(root, data[image_index])
            if not os.path.exists(image_path):
                continue
            label_path = os.path.join(save_path, data[image_index])
            begin = time.perf_counter()
            seg_method(image_path, save_path=label_path)
            cost_time = time.perf_counter() - begin
            total_time += cost_time
            df.loc[idx, 'Result'] = data[image_index]
            df.loc[idx, 'Time(s)'] = '{:.3f}'.format(cost_time)
            if seg_index is not None:
                seg_path = os.path.join(root, data[seg_index])
                if not os.path.exists(seg_path):
                    continue
                pred = sitk.GetArrayFromImage(read_img(label_path))
                target = sitk.GetArrayFromImage(read_img(seg_path))
                one_case_qualities = computeQualityMeasures_oneCases(pred, target, classes)
                # if seg_method == pelvic_segment:
                #     one_case_qualities = computeQualityMeasures_oneCases(pred, target, 3)
                # if seg_method == seg_rib:
                #     one_case_qualities = computeQualityMeasures_oneCases(pred, target, 1)
                cnt += 1
                total_dice += one_case_qualities['mean_dice']
                df.loc[idx, 'Dice(%)'] = '{:.1f}'.format(100 * one_case_qualities['mean_dice'])
            if idx + 1 < total_len and callback is not None:
                callback(100. * (idx + 1) // total_len)

        # 求平均
        if seg_index is not None:
            average_row = [pd.NA] * len(df.columns)
            average_row[0] = 'Mean'
            average_row[-2] = '{:.3f}'.format(total_time / cnt)
            average_row[-1] = '{:.1f}'.format(total_dice * 100. / cnt)
            df2 = pd.DataFrame(
                [average_row], columns=df.columns
            )
            df = pd.concat([df2, df])

            # df = df.append(pd.Series({
            #     image_index: '平均',
            #     'dice': '{:.3f}'.format(total_dice / total_cnt)
            # }), ignore_index=True)
            # s = pd.Series({'lib': randint(-1, 1), 'qty1': randint(-1, 1), 'qty2': randint(-1, 1)})
            # 这里 Series 必须是 dict-like 类型
            # df = df.append(s, ignore_index=True)
            # df.loc[total_cnt, image_index] = 'mean'
            # df.loc[total_cnt, 'dice'] = '{:.3f}'.format(total_dice / total_cnt)
        # 删除原来的列
        # df.drop(labels=columns, axis=1, inplace=True)
        if os.path.isabs(result_path):
            os.makedirs(os.path.dirname(result_path), exist_ok=True)
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
