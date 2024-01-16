import os
import time

import numpy as np
import torch
from albumentations import Resize
from albumentations.pytorch.functional import img_to_tensor
import cv2
from pytorch_grad_cam import GradCAM,FullGrad
from pytorch_grad_cam.utils.image import show_cam_on_image

from Classification.src_rct.model import TripleMRNet
from util import get_base_dir

base_dir = get_base_dir()


def load_and_process_image(path):
    img_resize = Resize(224, 224)

    files = os.listdir(path)
    image_paths = []
    image_names = []
    for i in files:
        if i.split('.')[-1] == 'png' or i.split('.')[-1] == 'PNG':
            image_names.append(os.path.join(path, i))
    if len(image_names) == 0:
        return None, None, None

    model2 = load_model()
    result = [0,0]
    heat_maps = []
    current_time = time.strftime('%Y_%m_%d_%I_%M_%S')
    save_path = os.path.join(base_dir, 'classification', current_time)

    image_names.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.png')[0]))
    n = 20 # 20图分一组
    image_grouped = [image_names[i:i + n] for i in range(0, len(image_names), n)]
    for group in image_grouped:
        images_processed = []
        for name in group:
            path = os.path.join(path, name)
            image_paths.append(path)
            img = cv2.imread(path, 0)
            img_cv = img_resize(image=img)
            img_cv = img_cv['image']
            img_cv = (img_cv - np.mean(img_cv)) / np.std(img_cv)
            img_cv = img_cv.astype(np.float32)
            img_cv = np.repeat(img_cv[:, :, np.newaxis], 3, axis=2)
            images_processed.append(img_cv)
        images_processed = np.array(images_processed)
        images_processed = images_processed.reshape(
            (
            images_processed.shape[0], images_processed.shape[3], images_processed.shape[1], images_processed.shape[2]))
        imag_tensor = img_to_tensor(images_processed)
        imag_tensor = imag_tensor.permute(1, 2, 0, 3)

        abnormal_logit = model2.forward(imag_tensor)
        abnormal_pred = torch.sigmoid(abnormal_logit)
        if abnormal_pred < 0.5:
            result[0]+=1
        else:
            result[1]+=1

        target_layers = [model2.net[-2]]
        cam = FullGrad(model=model2, target_layers=target_layers, use_cuda=False)
        grayscale_cam = cam(input_tensor=imag_tensor, targets=None)

        save_images = []
        for i, img_path in enumerate(group):
            os.makedirs(save_path, exist_ok=True)
            img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
            img = (img - img.min()) / (img.max() - img.min())
            gc = grayscale_cam[i, :]
            gc = cv2.resize(gc, (img.shape[0], img.shape[0]))
            visualization = show_cam_on_image(img, gc, use_rgb=True)
            save_images.append(os.path.join(save_path, os.path.basename(img_path)))
            cv2.imwrite(os.path.join(save_path, os.path.basename(img_path)),
                        cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))
        heat_maps += save_images
    r = 1 if result[1]>= result[0] else 0
    return heat_maps,image_names,str(r)



    # for i,name in enumerate(image_names):
    #     if i!=0 and i%16!=0:
    #         path = os.path.join(path, name)
    #         image_paths.append(path)
    #         img = cv2.imread(path, 0)
    #         img_cv = img_resize(image=img)
    #         img_cv = img_cv['image']
    #         img_cv = (img_cv - np.mean(img_cv)) / np.std(img_cv)
    #         img_cv = img_cv.astype(np.float32)
    #         img_cv = np.repeat(img_cv[:, :, np.newaxis], 3, axis=2)
    #         images_processed.append(img_cv)
    #         i += 1
    # # 16 224 224 3
    # # 16 3 224 224 reshape
    # # torch.Size([224, 16, 3, 224])  to tensor
    #
    #
    # return imag_tensor, image_paths


def load_model():
    path2 = os.path.join(base_dir, 'models/classify/test0.8512_tset0.8984_epoch78')
    model2 = TripleMRNet(backbone='vgg16')
    state_dict = torch.load(path2, map_location=torch.device('cpu'))
    model2.load_state_dict(state_dict)
    model2 = model2
    model2.eval()
    return model2


def classify_and_get_heatmap(input_tensor, images):
    model2 = load_model()

    result = None
    # stage1
    abnormal_logit = model2.forward(input_tensor)
    abnormal_pred = torch.sigmoid(abnormal_logit)

    if abnormal_pred < 0.5:
        result = 0
    else:
        result = 1

    target_layers = [model2.net[-5]]
    cam = GradCAM(model=model2, target_layers=target_layers, use_cuda=False)
    grayscale_cam = cam(input_tensor=input_tensor, targets=None)

    current_time = time.strftime('%Y_%m_%d_%I_%M_%S')
    save_path = os.path.join(base_dir, 'classification', current_time)

    for i, img_path in enumerate(images):
        os.makedirs(save_path, exist_ok=True)
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
        img = (img - img.min()) / (img.max() - img.min())
        gc = grayscale_cam[i, :]
        gc = cv2.resize(gc, (img.shape[0], img.shape[0]))
        visualization = show_cam_on_image(img, gc, use_rgb=True)
        cv2.imwrite(os.path.join(save_path, os.path.basename(img_path)),
                    cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))
    return save_path, str(result)


if __name__ == '__main__':
    inputs_tensor, images = load_and_process_image(r'F:\cam\val\0\30')
    classify_and_get_heatmap(inputs_tensor, images)
    print(base_dir)
