import os
from typing import Iterable

import SimpleITK as sitk
import nibabel as nib
import numpy as np
import torch
import torch.backends.cudnn as cudnn

from models.Rib_Segment_HDC_Net.HDC_Net import HDC_Net
from models.Rib_Segment_HDC_Net.predict_in_sliding_window import get_segmentation_and_classs_probabilities
from util import get_base_dir, read_img, save_img

base_dir = get_base_dir()

cudnn.benchmark = True


def normalize_image(image):
    # new_mean = 553.3240552983718
    # new_std = 308.01421958241514
    # image[image<202] = 0
    # image[image>1541] = 0
    # image = (image - new_mean)/new_std

    new_mean = 553.3240552983718
    new_std = 308.01421958241514
    input_ = image
    input_[input_ < 202] = 0
    input_[input_ > 1541] = 0
    input_ = (input_ - new_mean) / new_std
    return input_


def nib_load(file_name):
    if not os.path.exists(file_name):
        return np.array([1])

    proxy = nib.load(file_name)
    data = proxy.get_data()
    proxy.uncache()
    return data


def seg_rib(img_path, do_tta=False, mixed_precision=False, save_path=None):

    if img_path is None:
        return
    elif isinstance(img_path, str):
        list_of_lists = [[img_path]]
    elif isinstance(img_path, Iterable):
        list_of_lists = [list(img_path)]
    else:
        return
    # cleaned_output_files = None
    if save_path is None:
        cleaned_output_files = [os.path.join(base_dir, 'predict_label/rib',
                                             os.path.basename(path)) for path in list_of_lists[0]]
    elif isinstance(save_path, str):
        cleaned_output_files = [save_path]
    elif isinstance(save_path, Iterable):
        cleaned_output_files = list(save_path)
    else:
        return

    for path in cleaned_output_files:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    model = HDC_Net(1, 2, 32)
    model = model.cuda()

    checkpoint = torch.load(os.path.join(base_dir, 'models/Rib_Segment_HDC_Net/model_epoch_419_0.9307080876230142.pth'),
                            map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()

    for idx, img_path in enumerate(list_of_lists[0]):
        img = read_img(img_path)
        # spacing = img.GetSpacing()
        # origin = img.GetOrigin()
        # direction = img.GetDirection()
        img_ndarray = sitk.GetArrayFromImage(img).astype('float32')
        img_ndarray = np.transpose(img_ndarray, (2, 1, 0))
        img_ndarray = img_ndarray[..., None]
        img_ndarray = img_ndarray[None, ...]
        img_ndarray = np.ascontiguousarray(img_ndarray.transpose(0, 4, 1, 2, 3))
        img_ndarray = img_ndarray[0]
        input_ = normalize_image(img_ndarray)

        input_ = torch.from_numpy(input_)


        predicted_segmentation, class_probabilities = get_segmentation_and_classs_probabilities(input_,
                                                                                                patch_size=[128, 128, 128],
                                                                                                num_classes=2, model=model,
                                                                                                do_mirroring=False)
        print(predicted_segmentation.shape)
        predicted_segmentation = np.transpose(predicted_segmentation, (2, 1, 0))
        predicted_segmentation = sitk.GetImageFromArray(predicted_segmentation.astype('uint8'))
        save_img(cleaned_output_files[idx], predicted_segmentation, head_src=img, only_orient=True)
        # predicted_segmentation.SetSpacing(spacing)
        # predicted_segmentation.SetOrigin(origin)
        # predicted_segmentation.SetDirection(direction)
        # sitk.WriteImage(predicted_segmentation, save_path)
    print('end of seg_rib')


if __name__ == '__main__':
    import time

    path = os.path.join(base_dir, 'img/RibFrac101-image.nii.gz')
    begin = time.perf_counter()
    seg_rib(path)
    cost = time.perf_counter() - begin
    print('count: {}s'.format(cost))
