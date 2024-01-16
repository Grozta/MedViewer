#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from multiprocessing import Pool
from typing import Iterable

import numpy as np

from models.nnUNet.nnunet.inference.predict import preprocess_multithreaded
from models.nnUNet.nnunet.inference.segmentation_export import save_segmentation_nifti_from_softmax
from models.nnUNet.nnunet.training.model_restore import load_model_and_checkpoint_files
from util import get_base_dir

base_dir = get_base_dir()


def seg_rib(img_path, do_tta=False, mixed_precision=False, save_path=None):
    # model = 'models/nnUNet/nnUNetTrainerV2__nnUNetPlansv2.1'
    model = os.path.join(base_dir, 'models/nnUNet/nnUNetTrainerV2__nnUNetPlansv2.1')
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
    num_threads_preprocessing = 6
    segs_from_prev_stage = None
    do_tta = False
    step_size = 0.9
    all_in_gpu = False
    mixed_precision = True
    trainer, params = load_model_and_checkpoint_files(model, None, mixed_precision=True,
                                                      checkpoint_name='model_final_checkpoint')
    params = [params[0]]

    pool = Pool(1)
    results = []
    if 'segmentation_export_params' in trainer.plans.keys():
        force_separate_z = trainer.plans['segmentation_export_params']['force_separate_z']
        interpolation_order = trainer.plans['segmentation_export_params']['interpolation_order']
        interpolation_order_z = trainer.plans['segmentation_export_params']['interpolation_order_z']
    else:
        force_separate_z = None
        interpolation_order = 1
        interpolation_order_z = 0
    print("starting preprocessing generator")

    preprocessing = preprocess_multithreaded(trainer, list_of_lists, cleaned_output_files, num_threads_preprocessing,
                                             segs_from_prev_stage)

    print("starting prediction...")
    all_output_files = []
    for preprocessed in preprocessing:
        output_filename, (d, dct) = preprocessed
        all_output_files.append(all_output_files)
        if isinstance(d, str):
            data = np.load(d)
            os.remove(d)
            d = data

        print("predicting", output_filename)
        trainer.load_checkpoint_ram(params[0], False)
        softmax = trainer.predict_preprocessed_data_return_seg_and_softmax(
            d, do_mirroring=do_tta, mirror_axes=trainer.data_aug_params['mirror_axes'], use_sliding_window=True,
            step_size=step_size, use_gaussian=True, all_in_gpu=all_in_gpu,
            mixed_precision=mixed_precision)[1]
        for p in params[1:]:
            trainer.load_checkpoint_ram(p, False)
            softmax += trainer.predict_preprocessed_data_return_seg_and_softmax(
                d, do_mirroring=do_tta, mirror_axes=trainer.data_aug_params['mirror_axes'], use_sliding_window=True,
                step_size=step_size, use_gaussian=True, all_in_gpu=all_in_gpu,
                mixed_precision=mixed_precision)[1]
        if len(params) > 1:
            softmax /= len(params)

        transpose_forward = trainer.plans.get('transpose_forward')
        if transpose_forward is not None:
            transpose_backward = trainer.plans.get('transpose_backward')
            softmax = softmax.transpose([0] + [i + 1 for i in transpose_backward])

            if hasattr(trainer, 'regions_class_order'):
                region_class_order = trainer.regions_class_order
            else:
                region_class_order = None

            """There is a problem with python process communication that prevents us from communicating obejcts 
            larger than 2 GB between processes (basically when the length of the pickle string that will be sent is 
            communicated by the multiprocessing.Pipe object then the placeholder (\%i I think) does not allow for long 
            enough strings (lol). This could be fixed by changing i to l (for long) but that would require manually 
            patching system python code. We circumvent that problem here by saving softmax_pred to a npy file that will 
            then be read (and finally deleted) by the Process. save_segmentation_nifti_from_softmax can take either 
            filename or np.ndarray and will handle this automatically"""
            bytes_per_voxel = 4
            if all_in_gpu:
                bytes_per_voxel = 2  # if all_in_gpu then the return value is half (float16)
            if np.prod(softmax.shape) > (2e9 / bytes_per_voxel * 0.85):  # * 0.85 just to be save
                print(
                    "This output is too large for python process-process communication. Saving output temporarily to disk")
                np.save(output_filename[:-7] + ".npy", softmax)
                softmax = output_filename[:-7] + ".npy"

            results.append(pool.starmap_async(save_segmentation_nifti_from_softmax,
                                              ((softmax, output_filename, dct, interpolation_order, region_class_order,
                                                None, None,
                                                None, None, force_separate_z, interpolation_order_z),)
                                              ))

        print("inference done. Now waiting for the segmentation export to finish...")

        pool.close()
        pool.join()
    print('end of seg_rib')


if __name__ == '__main__':
    import time

    path = os.path.join(base_dir, 'img/RibFrac101-image.nii.gz')
    begin = time.perf_counter()
    seg_rib(path)
    cost = time.perf_counter() - begin
    print('count: {}s'.format(cost))
