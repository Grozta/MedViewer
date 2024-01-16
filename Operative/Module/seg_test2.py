#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import time

import numpy as np
import torch
from albumentations import (Normalize, Compose)
from albumentations.pytorch.transforms import img_to_tensor
from cv2 import cv2
from tqdm import tqdm

from Operative.Module.draw_labels import mark as draw_labels_mark
from Operative.Module.parts_seg import CleanU_Net as parts_seg
from util import get_base_dir

base_dir = get_base_dir()
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_color_appliance = [[0, 0, 0], [0, 255, 0], [255, 255, 0], [255, 255, 255]]
class_color = [[0, 255, 0], [0, 255, 255], [125, 255, 12]]


def mask_overlay(image, mask, color=(0, 255, 0)):  # 将分割结果作为mask放入原图
    """
    Helper function to visualize mask on the top of the car
    """
    # mask = np.dstack((mask, mask, mask)) * np.array(color)
    mask = mask.astype(np.uint8) * 255
    weighted_sum = cv2.addWeighted(mask, 0.5, image, 0.5, 0.)
    img = image.copy()
    ind = mask[:, :, 1] > 0
    img[ind] = weighted_sum[ind]
    return img


def operative_load_model():
    model = parts_seg(in_channels=3, out_channels=4)
    model_path = os.path.join(base_dir, 'Operative', 'model', 'parts.pt')  # 多类别分割模型地址
    state = torch.load(str(model_path), map_location='cpu')
    state = {key.replace('module.', ''): value for key, value in state['model'].items()}
    model.load_state_dict(state)
    model.to(DEVICE)
    model.eval()
    return model


def deal_single_image(model, image):
    """
    处理单张图片
    :param model: 模型
    :param image: 图片(cv2,bgr)
    :return: 分割，原图，原图+分割
    """
    h, w, channel = image.shape
    mask = np.zeros(shape=(h, w))

    image_ori = image
    origin_seg = image_ori.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    aug = Compose([
        # PadIfNeeded(min_height=h, min_width=w, border_mode=cv2.BORDER_CONSTANT, value=0, p=1.0),  # padding到2的5次方的倍数
        Normalize(p=1)  # 归一化
    ])
    augmented = aug(image=image, mask=mask)
    image = augmented['image']
    image = img_to_tensor(image).unsqueeze(0).to(
        DEVICE)  # torch.from_numpy(img).unsqueeze(0).unsqueeze(0).float().to(DEVICE)  # 图像转为tensor格式
    output = model(image)  # 预测
    seg_mask = (output[0].data.cpu().numpy().argmax(axis=0)).astype(np.uint8)

    full_mask = np.zeros((h, w, 3))
    for mask_label, sub_color in enumerate(class_color_appliance):
        full_mask[seg_mask == mask_label] = sub_color[::-1]
    full_mask = draw_labels_mark(full_mask, show="None", thre=500, size=3, fontScale=1, size_=2,
                                 class_color=class_color)
    seg = mask_overlay(image_ori, (full_mask > 0)).astype(np.uint8)
    return seg_mask, origin_seg, seg


def deal_directory(data_path, result_path):
    model = operative_load_model()
    names = os.listdir(data_path)

    os.makedirs(os.path.join(result_path, 'origin_imgs'), exist_ok=True)
    os.makedirs(os.path.join(result_path, 'appliance_imgs'), exist_ok=True)
    os.makedirs(os.path.join(result_path, 'cover_imgs'), exist_ok=True)
    print('end of loading model')
    for i, name in tqdm(enumerate(names)):
        path_single = os.path.join(data_path, name)
        image = cv2.imread(str(path_single))
        t1 = time.time()
        seg_mask, origin_seg, seg = deal_single_image(model, image)
        t2 = time.time()
        print("time:", (t2 - t1))
        cv2.imwrite(os.path.join(result_path, 'appliance_imgs', '{}.png'.format(str(i).zfill(4))), seg_mask)
        cv2.imwrite(os.path.join(result_path, 'origin_imgs', '{}.png'.format(str(i).zfill(4))), origin_seg)
        cv2.imwrite(os.path.join(result_path, 'cover_imgs', '{}.png'.format(str(i).zfill(4))), seg)

    # save_video(result_path, result_path, h, w)  # 可以播放保存的视频展示分割结果
