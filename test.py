#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import SimpleITK as sitk

from util import read_img, save_img


def registration(moving_image, fixed_image):
    """
    配准

    :param moving_image: 浮动图片
    :param fixed_image: 参考图片
    :return: 配准后的图片，最终
    """

    origin_pixel_id = moving_image.GetPixelID()
    moving_image = sitk.Cast(moving_image, sitk.sitkFloat32)
    fixed_image = sitk.Cast(fixed_image, sitk.sitkFloat32)

    filter = sitk.MinimumMaximumImageFilter()
    filter.Execute(moving_image)
    min_value = filter.GetMinimum()

    initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                          moving_image,
                                                          sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)

    # moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0,
    #                                  moving_image.GetPixelID())

    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)

    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                      convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=False)

    final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                  sitk.Cast(moving_image, sitk.sitkFloat32))

    moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, min_value,
                                     origin_pixel_id)
    return moving_resampled, final_transform


if __name__ == '__main__':
    fixed_path = 'img/T1_brain.nii.gz'
    moving_path = 'img/T2_brain.nii.gz'
    fixed_image = read_img(fixed_path)
    moving_image = read_img(moving_path)

    moving_resampled, final_transform = registration(moving_image, fixed_image)
    save_img('test.nii.gz', moving_resampled)
    #
    # # moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0,
    # #                                  moving_image.GetPixelID())
    #
    # registration_method = sitk.ImageRegistrationMethod()
    #
    # # Similarity metric settings.
    # registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    # registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    # registration_method.SetMetricSamplingPercentage(0.01)
    #
    # registration_method.SetInterpolator(sitk.sitkLinear)
    #
    # # Optimizer settings.
    # registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
    #                                                   convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    # registration_method.SetOptimizerScalesFromPhysicalShift()
    #
    # # Setup for the multi-resolution framework.
    # registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    # registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    # registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
    #
    # # Don't optimize in-place, we would possibly like to run this cell multiple times.
    # registration_method.SetInitialTransform(initial_transform, inPlace=False)
    #
    # final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
    #                                               sitk.Cast(moving_image, sitk.sitkFloat32))
    #
    # moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0,
    #                                  moving_image.GetPixelID())
    #
    # # interact(display_images_with_alpha, image_z=(0, fixed_image.GetSize()[2]), alpha=(0.0, 1.0, 0.05),
    # #          fixed=fixed(fixed_image), moving=fixed(moving_resampled));
    #
    # sitk.WriteImage(moving_resampled, 'test.nii.gz')
    # # sitk.WriteTransform(final_transform, os.path.join(OUTPUT_DIR, 'RIRE_training_001_CT_2_mr_T1.tfm'))
