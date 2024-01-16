#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import SimpleITK as sitk
import nibabel as nib
import numpy as np

if __name__ == '__main__':
    # fixed_path = 'img/dataset5_1411226_Image.nii.gz'
    # moving_path = 'img/dataset5_1614236_Image.nii.gz'
    # fixed_image = read_img(fixed_path)
    # moving_image = read_img(moving_path)
    #
    # fixed_image = sitk_image_to_itk_image(fixed_image)
    # moving_image = sitk_image_to_itk_image(moving_image)
    # # fixed_image = itk.imread(fixed_path)
    # # moving_image = itk.imread(moving_path)
    # # direction = fixed_image.GetDirection()
    #
    # # Call registration function
    # result_image, result_transform_parameters = registration_by_itk_elastix(moving_image, fixed_image, 'rigid',
    #                                                                         'test.nii.gz')
    # print('hello world2')
    # print(itk.GetArrayFromImage(result_image).min())
    img = sitk.ReadImage(r'/media/y/TOSHIBA_EXT/visualizer_pyqt5_2022_5_4/models/Rib_Segment_HDC_Net/test.nii.gz')
    img = sitk.GetArrayFromImage(img).astype('uint8')
    img = sitk.GetImageFromArray(img)
    sitk.WriteImage(img,'test1.nii.gz')
    print("W")
    # img = img.astype('float64')
    # l = img
    #
    # img_ = nib.load(r'F:\test\ribfrac-test-images\RibFrac501-image.nii.gz')
    # img_ = img_.get_fdata()
    # img = np.transpose(img,(2,1,0))
    # t = (img==img_)
    # print('ww')


# sitk 转 nib np.transpose(img,(2,1,0))
# 转回去 np.transpose(img,(2,1,0))

