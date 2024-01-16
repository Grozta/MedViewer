#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import multiprocessing
import os
from multiprocessing import Pool
from typing import Iterable

import numpy as np
import torch
from skimage.measure import regionprops

from models.CTPelvic1K_CS_Net.nnunet.inference.predict import preprocess_multithreaded
from models.CTPelvic1K_CS_Net.nnunet.inference.segmentation_export import save_segmentation_nifti_from_softmax
from models.CTPelvic1K_CS_Net.nnunet.training.model_restore import load_model_and_checkpoint_files
from models.CTPelvic1K_CS_Net.postprocessing import newsdf_post_processor
from models.CTPelvic1K_CS_Net.utils import _sitk_Image_reader, _sitk_image_writer
from util import get_base_dir

base_dir = get_base_dir()


def pelvic_segment_cs_net(img_path, do_cut=False, save_path=None):
    """
    用unet+hdd盆骨分割

    :param img_path: 图片路径
    :param do_cut: 最后做裁剪
    :param save_path 保存路径
    """
    model = os.path.join(base_dir, 'models/CTPelvic1K_CS_Net/nnUNetTrainer__nnUNetPlans')
    # list_of_lists = []
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
        cleaned_output_files = [os.path.join(base_dir, 'predict_label/pelvic_CS_Net',
                                             os.path.basename(path)) for path in list_of_lists[0]]
    elif isinstance(save_path, str):
        cleaned_output_files = [save_path]
    elif isinstance(save_path, Iterable):
        cleaned_output_files = list(save_path)
    else:
        return
    for path in cleaned_output_files:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    folds = [5]
    save_npz = False
    num_threads_preprocessing = 1
    num_threads_nifti_save = 1
    segs_from_prev_stage = None
    do_tta = False
    # overwrite_existing = True
    steps = 2

    prman = Pool(num_threads_nifti_save)
    results = []

    ### begin predict!!! ###
    print("emptying cuda cache!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    torch.cuda.empty_cache()

    print("loading parameters for folds,", folds)
    trainer, params = load_model_and_checkpoint_files(model, folds)

    print("starting preprocessing generator")
    ### ??? SO what is this ??? ###
    preprocessing = preprocess_multithreaded(trainer, list_of_lists, cleaned_output_files, num_threads_preprocessing,
                                             segs_from_prev_stage)
    print("starting prediction...")
    for preprocessed in preprocessing:
        output_filename, (d, dct) = preprocessed
        if isinstance(d, str):
            data = np.load(d)
            os.remove(d)
            d = data

        print("predicting", output_filename)

        softmax = []
        for p in params:
            trainer.load_checkpoint_ram(p, False)
            softmax.append(trainer.predict_preprocessed_data_return_softmax(d,
                                                                            do_tta,
                                                                            1,
                                                                            False,
                                                                            1,
                                                                            trainer.data_aug_params['mirror_axes'],
                                                                            True,
                                                                            True,
                                                                            steps,  # TODO step
                                                                            trainer.patch_size,
                                                                            True)[None])

        softmax = np.vstack(softmax)
        softmax_mean = np.mean(softmax, 0)

        transpose_forward = trainer.plans.get('transpose_forward')
        if transpose_forward is not None:
            transpose_backward = trainer.plans.get('transpose_backward')
            softmax_mean = softmax_mean.transpose([0] + [i + 1 for i in transpose_backward])

        if save_npz:
            npz_file = output_filename[:-7] + ".npz"
        else:
            npz_file = None

        """There is a problem with python process communication that prevents us from communicating obejcts 
        larger than 2 GB between processes (basically when the length of the pickle string that will be sent is 
        communicated by the multiprocessing.Pipe object then the placeholder (\%i I think) does not allow for long 
        enough strings (lol). This could be fixed by changing i to l (for long) but that would require manually 
        patching system python code. We circumvent that problem here by saving softmax_pred to a npy file that will 
        then be read (and finally deleted) by the Process. 
        save_segmentation_nifti_from_softmax can take either filename or np.ndarray and will handle this automatically"""

        if np.prod(softmax_mean.shape) > (2e9 / 4 * 0.9):  # *0.9 just to be save
            print \
                    (
                    "This output is too large for python process-process communication. Saving output temporarily to disk. {}".format(
                        output_filename[:-7] + ".npy"
                    ))
            np.save(output_filename[:-7] + ".npy", softmax_mean)
            softmax_mean = output_filename[:-7] + ".npy"

        results.append(prman.starmap_async(save_segmentation_nifti_from_softmax,
                                           ((softmax_mean, output_filename, dct, 1, None, None, None, npz_file),)
                                           ))

    _ = [i.get() for i in results]

    for file in cleaned_output_files:
        _, pred, meta = _sitk_Image_reader(file)
        pred_sdf = newsdf_post_processor(pred, sdf_th=0.4, region_th=2000)
        if do_cut:
            print(pred_sdf.shape, np.unique(pred_sdf))

            region_properties = regionprops(pred_sdf)
            other_min_x, other_max_x = pred.shape[0], 0
            min_x, max_x = pred.shape[0], 0
            for region in region_properties:
                x, y, z = region.coords[0]
                label = pred_sdf[x, y, z]
                if label == 4:
                    min_x, _, _, max_x, _, _ = region.bbox
                else:
                    x1, _, _, x2, _, _ = region.bbox
                    other_min_x = min(other_min_x, x1)
                    other_max_x = max(other_max_x, x2)
            pred_sdf[max(other_max_x + 12, min_x) + 1:] = 0
        _sitk_image_writer(pred_sdf, meta, file)
    print('end of post-process')


if __name__ == '__main__':
    label_file = os.path.join(base_dir, 'predict_label/pelvic', 'dataset3_colon_025_data.nii.gz')
    # pelvic_segment(self.image_path, do_cut=do_cut, save_path=label_file)
    pelvic_segment_cs_net(('img/pelvic/pelvic_img/dataset3_colon_025_data.nii.gz'), False, save_path=(label_file))
