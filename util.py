#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import sys

import SimpleITK as sitk
import itk
import numpy as np
import vtkmodules.all as vtk
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QIcon
import cv2


def get_base_dir():
    if getattr(sys, 'frozen', None):
        return sys._MEIPASS
    return os.path.dirname(os.path.realpath(__file__))


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


def sitk_image_to_itk_image(sitk_image):
    return numpy_to_itk_image(sitk.GetArrayFromImage(sitk_image),
                              sitk_image.GetSpacing(),
                              sitk_image.GetOrigin(),
                              sitk_image.GetDirection())


def numpy_to_itk_image(np_image, spacing, origin, direction):
    result = itk.GetImageFromArray(np_image)
    result.SetSpacing(spacing)
    result.SetOrigin(origin)
    result.SetDirection(itk.GetMatrixFromArray(np.array(direction).reshape(3, 3)))
    return result


def registration_by_itk_elastix(moving_image, fixed_image, parameter_map='rigid', output_path=None):
    if isinstance(moving_image, itk.Image):
        moving_image_np = itk.GetArrayFromImage(moving_image)
    else:
        raise Exception('unsupported type')

    origin_pixel_id = moving_image.dtype
    # elastix只支持float
    fixed_image = fixed_image.astype(itk.F)
    moving_image = moving_image.astype(itk.F)
    default_pixel_value = moving_image_np.min()

    parameter_object = itk.ParameterObject.New()
    default_rigid_parameter_map = parameter_object.GetDefaultParameterMap(parameter_map)
    parameter_object.AddParameterMap(default_rigid_parameter_map)
    parameter_object.SetParameter('DefaultPixelValue', str(default_pixel_value))
    # 能不能配准成功，与初始变换有很大的关系
    parameter_object.SetParameter('AutomaticTransformInitialization', 'true')
    print(parameter_object)
    print('---------------------------------------------')
    # Call registration function
    result_image, result_transform_parameters = itk.elastix_registration_method(
        fixed_image, moving_image,
        parameter_object=parameter_object,
        # log_to_console=True,
        # log_to_file=True,
        # LogFileName='test.log',
        # OutputDirectory='.'
    )
    result_image = result_image.astype(origin_pixel_id)
    # itk.imwrite(result_image.astype(origin_pixel_id), 'pre.nii.gz')
    # print(itk.GetArrayFromImage(result_image).min())

    dimension = moving_image.GetImageDimension()
    composite_transform = itk.CompositeTransform[itk.D, dimension].New()
    # print(result_transform_parameters.GetNumberOfParameterMaps())
    # 先做的后加
    for index in range(result_transform_parameters.GetNumberOfParameterMaps() - 1, -1, -1):
        if 'rigid' == parameter_map:
            euler_transform = itk.Euler3DTransform[itk.D].New()

            pm0 = result_transform_parameters.GetParameterMap(index)

            center = [float(p) for p in pm0['CenterOfRotationPoint']]
            fixed_parameters = itk.OptimizerParameters[itk.D](len(center))
            for i, p in enumerate(center):
                fixed_parameters[i] = p
            euler_transform.SetFixedParameters(fixed_parameters)

            elx_parameters = [float(p) for p in pm0['TransformParameters']]
            itk_parameters = itk.OptimizerParameters[itk.D](len(elx_parameters))
            for i, p in enumerate(elx_parameters):
                itk_parameters[i] = p
            euler_transform.SetParameters(itk_parameters)
            composite_transform.AddTransform(euler_transform)
        elif 'affine' == parameter_map:
            affine_transform = itk.AffineTransform[itk.D, dimension].New()

            pm1 = result_transform_parameters.GetParameterMap(index)

            center = [float(p) for p in pm1['CenterOfRotationPoint']]
            fixed_parameters = itk.OptimizerParameters[itk.D](len(center))
            for i, p in enumerate(center):
                fixed_parameters[i] = p
            affine_transform.SetFixedParameters(fixed_parameters)

            elx_parameters = [float(p) for p in pm1['TransformParameters']]
            itk_parameters = itk.OptimizerParameters[itk.D](len(elx_parameters))
            for i, p in enumerate(elx_parameters):
                itk_parameters[i] = p
            affine_transform.SetParameters(itk_parameters)
            composite_transform.AddTransform(affine_transform)
        else:
            raise Exception('unsupported transform')

    # When creating the composite transform for itk,
    # take into account that elastix uses T2(T1(x)) while itk does this the other way around.
    # So to get the correct composite transform, add the last transform in elastix first in itk.
    # composite_transform = itk.CompositeTransform[itk.D, dimension].New()
    # composite_transform.AddTransform(affine_transform)
    # composite_transform.AddTransform(euler_transform)
    result_image_itk = itk.resample_image_filter(moving_image,
                                                 transform=composite_transform,
                                                 default_pixel_value=float(default_pixel_value),
                                                 use_reference_image=True,
                                                 reference_image=fixed_image)
    result_image_itk = result_image_itk.astype(origin_pixel_id)
    if output_path is not None:
        itk.imwrite(result_image_itk, output_path)
    return result_image_itk, composite_transform


def numpy2vtkImageImport(source_numpy, spacing=None, origin=None, direction=None, as_uint8=False):
    """
    numpy转成vtkImageImport

    :param source_numpy: numpy格式的图片（z,y,x）(A,C,S)
    :param spacing: 像素的间隔
    :param origin: 图片的原点
    :param direction: 方向
    :param as_uint8: 转成uint8
    :return: vtkImageImport
    """
    importer = vtk.vtkImageImport()
    origin_type = source_numpy.dtype
    if as_uint8:
        origin_type = np.uint8
        source_numpy = source_numpy.astype('uint8')
    # else:
    #     source_numpy = source_numpy.astype('int32')
    img_string = source_numpy.tobytes()
    dim = source_numpy.shape  # (z,y,x),(A,C,S)

    importer.CopyImportVoidPointer(img_string, len(img_string))
    if as_uint8:
        importer.SetDataScalarTypeToUnsignedChar()
    elif np.int16 == origin_type:
        importer.SetDataScalarTypeToShort()
    elif np.float32 == origin_type:
        importer.SetDataScalarTypeToFloat()
    else:
        importer.SetDataScalarTypeToInt()
    importer.SetNumberOfScalarComponents(1)

    extent = importer.GetDataExtent()  # 0,0,0,0,0,0
    # 图像的维度=(extent[1]-extent[0]+1) * (extent[3]-extent[2]+1) * (extent[5]-DataExtent[4]+1)=(x,y,z)=(S,C,A)
    importer.SetDataExtent(extent[0], extent[0] + dim[2] - 1,
                           extent[2], extent[2] + dim[1] - 1,
                           extent[4], extent[4] + dim[0] - 1)
    importer.SetWholeExtent(extent[0], extent[0] + dim[2] - 1,
                            extent[2], extent[2] + dim[1] - 1,
                            extent[4], extent[4] + dim[0] - 1)
    if spacing is not None:
        importer.SetDataSpacing(*spacing)
    if origin is not None:
        importer.SetDataOrigin(*origin)
    if direction is not None:
        importer.SetDataDirection(direction)
    return importer


def resliceByOrient(vtk_data, center, ori):
    """
    重采样

    :param vtk_data: vtk的数据
    :param center: 采样中心(S,C,A)(x,y,z)
    :param ori: 1:S(x),2:C(y),0:A(z)
    :return: 重采样的数据
    """
    if 1 == ori:
        # 矢状面（sagittal plane）S(x)
        elements = [
            0, 0, -1, 0,
            1, 0, 0, 0,
            0, -1, 0, 0,
            0, 0, 0, 1
        ]
    elif 2 == ori:
        # 冠状面（coronal plane）C(y)
        elements = [
            1, 0, 0, 0,
            0, 0, 1, 0,
            0, -1, 0, 0,
            0, 0, 0, 1
        ]
    elif 0 == ori:
        # 横断面（transverse plane）A(z)
        elements = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ]
    else:
        # 斜切切片
        elements = [
            1, 0, 0, 0,
            0, 0, 8.66025, -0.5, 0,
            0, 0.5, 0.866025, 0,
            0, 0, 0, 1
        ]
    resliceAxes = vtk.vtkMatrix4x4()
    resliceAxes.DeepCopy(elements)
    for i in range(3):
        resliceAxes.SetElement(i, 3, center[i])
        # resliceAxes.SetElement(i, 3, int(center[i]))
    reslice = vtk.vtkImageReslice()
    reslice.SetInputConnection(vtk_data.GetOutputPort())
    reslice.SetOutputDimensionality(2)
    reslice.SetResliceAxes(resliceAxes)
    reslice.SetInterpolationModeToLinear()
    reslice.Update()
    return reslice


def get_color_table(is_image, minimum=None, maximum=None, window=None, level=None):
    """
    获取颜色映射表

    :param is_image: 是否为图像
    :param minimum: 最小值
    :param maximum: 最大值
    :param window: 窗宽
    :param level: 窗位
    :return: 颜色映射表
    """
    colorTable = vtk.vtkLookupTable()
    if is_image:
        if minimum is None and maximum is None and window is not None and level is not None:
            minimum = (2 * level - window) / 2.0 + 0.5
            maximum = (2 * level + window) / 2.0 + 0.5
        elif minimum is None or maximum is None:
            raise Exception("can't get right min max")

        # 像素最小值到最大值，（可以根据窗宽窗位计算出像素范围）
        colorTable.SetRange(minimum, maximum)
        colorTable.SetValueRange(0.0, 1.0)
        colorTable.SetSaturationRange(0.0, 0.0)
        colorTable.SetRampToLinear()
    else:
        # TODO 改成正常的颜色
        colorTable.SetNumberOfTableValues(5)
        colorTable.SetRange(0.0, 4.0)
        colorTable.SetTableValue(0, 0, 0.0, 0.0, 0.0)
        colorTable.SetTableValue(1, 0.0, 1.0, 0.0, 0.4)
        colorTable.SetTableValue(2, 1.0, 0.0, 0.0, 0.4)
        colorTable.SetTableValue(3, 0.0, 0.0, 1.0, 0.4)
        colorTable.SetTableValue(4, 0.0, 0.0, 1.0, 0.4)
    colorTable.Build()
    return colorTable


def CreateColorBoxIcon(w, h, r, g, b):
    rect = QRect(2, 2, w - 5, w - 5)
    pix = QPixmap(w, h)
    pix.fill(QColor(0, 0, 0, 0))
    paint = QPainter(pix)
    paint.setPen(QColor(0, 0, 0))
    paint.setBrush(QColor(r, g, b))
    paint.drawRect(rect)
    paint.end()
    return QIcon(pix)


def numpy2QImage(src, fmt=QImage.Format_Grayscale8):
    """
    numpy转QImage

    :param src: numpy格式(gray/rgb,hw或hwc)
    :param fmt: QImage的格式
    :return: QImage
    """
    if 3 != len(src.shape):
        return QImage(src.data.tobytes(), src.shape[1], src.shape[0], src.shape[1], fmt)
    return QImage(src.data, src.shape[1], src.shape[0], src.shape[1] * src.shape[2], fmt)


def numpy2QPixmap(src, shape, fmt=QImage.Format_Grayscale8):
    """
    numpy转QPixmap

    :param src: numpy格式(gray/rgb,hw或hwc)
    :param shape: pixmap的shape（h*w）
    :param fmt: QImage的格式
    :return: QPixmap
    """
    return QPixmap(numpy2QImage(src, fmt)).scaled(shape[1], shape[0])


def normalize(src, window=None, level=None):
    """
    归一化

    :param src: 原图
    :param window: 窗宽
    :param level: 窗位
    :return: 归一化后的图片
    """
    img_min = src.min()
    img_max = src.max()
    if window is None:
        window = img_max - img_min
    if level is None:
        level = (img_min + img_max) // 2

    win_min = (2 * level - window) / 2.0 + 0.5
    win_max = (2 * level + window) / 2.0 + 0.5
    src = np.clip(src, win_min, win_max)
    cv2.normalize(src, src, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    return src.astype(np.uint8)


def read_img(path):
    """
    读取文件，如果是dicom，则读取整个序列

    :param path: 文件路径
    :return: image
    """
    if not os.path.exists(path):
        return None

    try:
        if '.dcm' == os.path.splitext(path)[-1]:
            # TODO dicom格式需要判断序列号

            # 获取该文件下的所有序列ID，每个序列对应一个ID， 返回的series_IDs为一个列表
            # series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(os.path.dirname(path))
            # series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(os.path.dirname(path), series_IDs[0])

            # 读取这个dicom所在的目录，找到所有dicom格式
            series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(os.path.dirname(path))

            # 新建一个ImageSeriesReader对象
            series_reader = sitk.ImageSeriesReader()
            series_reader.MetaDataDictionaryArrayUpdateOn()  # 这一步是加载公开的元信息
            series_reader.LoadPrivateTagsOn()
            # 通过之前获取到的序列的切片路径来读取该序列
            series_reader.SetFileNames(series_file_names)

            # reader = sitk.ImageFileReader()
            # reader.SetFileName(series_file_names[0])
            # reader.LoadPrivateTagsOn()
            #
            # reader.ReadImageInformation()
            #
            # for k in reader.GetMetaDataKeys():  # 获取 key
            #     print(k, reader.GetMetaData(k))  # 获取 key 对应的 MetaData

            # 获取该序列对应的3D图像
            image = series_reader.Execute()
        else:
            # Width: 宽度，X轴，矢状面 S
            # Height: 高度，Y轴，冠状面 C
            # Depth: 深度， Z轴，横断面 A
            image = sitk.ReadImage(path)  # x,y,z
        return image
        # return sitk.GetArrayFromImage(image)  # z, y, x
    except:
        return None


def save_img(path, img, head_src=None, only_orient=False):
    """
    保存图片

    :param path:保存路径
    :param img: 保存的图片
    :param head_src: 头部信息的图片（image）
    :param only_orient: 只保存方向信息
    """
    # TODO 不能保存dicom
    if isinstance(img, np.ndarray):
        result = sitk.GetImageFromArray(img)
    else:
        result = img
    if head_src:
        if not only_orient:
            for key in head_src.GetMetaDataKeys():
                result.SetMetaData(key, head_src.GetMetaData(key))
        result.SetSpacing(head_src.GetSpacing())
        result.SetOrigin(head_src.GetOrigin())
        result.SetDirection(head_src.GetDirection())

    os.makedirs(os.path.dirname(path), exist_ok=True)
    sitk.WriteImage(result, path)


def cross_hair_actors(line_ver, line_hor, ori):
    color = vtk.vtkNamedColors()

    mapper_ver = vtk.vtkPolyDataMapper()
    mapper_hor = vtk.vtkPolyDataMapper()
    mapper_hor.SetInputConnection(line_ver.GetOutputPort())
    mapper_ver.SetInputConnection(line_hor.GetOutputPort())

    actor_ver = vtk.vtkActor()
    actor_hor = vtk.vtkActor()
    actor_ver.SetMapper(mapper_ver)
    actor_hor.SetMapper(mapper_hor)

    # 在事件中根据color的不同来区分视图
    if ori == 0:
        actor_ver.GetProperty().SetColor(0.0, 0.0, 1.0)
        actor_hor.GetProperty().SetColor(0.0, 0.0, 1.0)
    elif ori == 1:
        actor_ver.GetProperty().SetColor(0.0, 0.0, 0.99)
        actor_hor.GetProperty().SetColor(0.0, 0.0, 0.99)
    else:
        actor_ver.GetProperty().SetColor(0.0, 0.0, 0.98)
        actor_hor.GetProperty().SetColor(0.0, 0.0, 0.98)

    return actor_ver, actor_hor


class InteractStyle(vtk.vtkInteractorStyleImage):
    def __init__(self, line_ver, line_hor, iren, image_actor, dims, ori):
        self.line_ver = line_ver
        self.line_hor = line_hor
        self.interactor = iren
        self.origin = image_actor.GetInput().GetOrigin()
        self.dims = dims
        self.ori = ori
        self.spacing = image_actor.GetInput().GetSpacing()
        self.AddObserver(vtk.vtkCommand.LeftButtonPressEvent, self.OnLeftButtonDown)

    def SetLine_new(self, x, y, line_ver, line_hor, ori, dims, spacing, origin):
        if ori == 0:
            line_ver.SetPoint2([x + origin[0], dims[1] * spacing[1] + origin[1], 0.1])
            line_ver.SetPoint1([x + origin[0], origin[1], 0.1])
            """横线"""
            line_hor.SetPoint1([origin[0], y + origin[1], 0.1])
            line_hor.SetPoint2([dims[0] * spacing[0] + origin[0], y + origin[1], 0.1])
        elif ori == 1:
            line_ver.SetPoint2([x + origin[0], dims[2] * spacing[1] + origin[1], 0.1])
            line_ver.SetPoint1([x + origin[0], origin[1], 0.1])
            line_hor.SetPoint1([origin[0], y + origin[1], 0.1])
            line_hor.SetPoint2([dims[1] * spacing[0] + origin[0], y + origin[1], 0.1])
        else:
            line_ver.SetPoint2([x + origin[0], dims[2] * spacing[1] + origin[1], 0.1])
            line_ver.SetPoint1([x + origin[0], origin[1], 0.1])
            line_hor.SetPoint1([origin[0], y + origin[1], 0.1])
            line_hor.SetPoint2([dims[0] * spacing[0] + origin[0], y + origin[1], 0.1])

        line_hor.Update()
        line_ver.Update()

    def OnLeftButtonDown(self, obj, event):
        # TODO：三框联动
        # TODO：判定是否越界
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.0001)
        p = self.interactor.GetEventPosition()
        picker.Pick(p[0], p[1], 0, self.interactor.GetRenderWindow().GetRenderers().GetFirstRenderer())
        pos = picker.GetPickPosition()
        x, y = round(pos[0] - self.origin[0]), round(
            pos[1] - self.origin[1])  # 将原点移到左下方   这里得到的x,y似乎已经乘过了spacing，后面再对x,y乘spacing会导致十字线的定位出错

        print(x, y)
        print(pos)
        self.SetLine_new(x, y, self.line_ver, self.line_hor, self.ori, self.dims, self.spacing, self.origin)
        renwin = self.interactor.GetRenderWindow()
        renwin.Render()


def add_cross_hair(image_actor, dims, ori):
    origin = image_actor.GetInput().GetOrigin()
    spacing = image_actor.GetInput().GetSpacing()

    line_ver = vtk.vtkLineSource()
    line_hor = vtk.vtkLineSource()

    if ori == 0:
        """竖线"""
        line_ver.SetPoint2([(dims[0] / 2) * spacing[0] + origin[0], dims[1] * spacing[1] + origin[1], 0.1])
        line_ver.SetPoint1([(dims[0] / 2) * spacing[0] + origin[0], origin[1], 0.1])
        """横线"""
        line_hor.SetPoint1([origin[0], (dims[1] / 2) * spacing[1] + origin[1], 0.1])
        line_hor.SetPoint2([dims[0] * spacing[0] + origin[0], (dims[1] / 2) * spacing[1] + origin[1], 0.1])
    elif ori == 1:
        line_ver.SetPoint2([(dims[1] / 2) * spacing[0] + origin[0], dims[2] * spacing[1] + origin[1], 0.1])
        line_ver.SetPoint1([(dims[1] / 2) * spacing[0] + origin[0], origin[1], 0.1])
        line_hor.SetPoint1([origin[0], (dims[2] / 2) * spacing[1] + origin[1], 0.1])
        line_hor.SetPoint2([dims[1] * spacing[0] + origin[0], (dims[2] / 2) * spacing[1] + origin[1], 0.1])
    else:
        line_ver.SetPoint2([(dims[0] / 2) * spacing[0] + origin[0], dims[2] * spacing[1] + origin[1], 0.1])
        line_ver.SetPoint1([(dims[0] / 2) * spacing[0] + origin[0], origin[1], 0.1])
        line_hor.SetPoint1([origin[0], (dims[2] / 2) * spacing[1] + origin[1], 0.1])
        line_hor.SetPoint2([dims[0] * spacing[0] + origin[0], (dims[2] / 2) * spacing[1] + origin[1], 0.1])

    line_ver.Update()
    line_hor.Update()

    return line_ver, line_hor


def get_ori(color):
    if color[-1] == 1.0:
        return 0
    elif color[-1] == 0.99:
        return 1
    else:
        return 2


def set_Line(x, y, line_vers, ori, dims, spacing, origin):
    line_ver = line_vers[ori][0]
    line_hor = line_vers[ori][1]

    if ori == 0:
        if y>spacing[1]*dims[1]:
            y = spacing[1]*dims[1]
        if y<0:
            y = 0
        if x>spacing[0]*dims[0]:
            x = spacing[0]*dims[0]
        if x<0:
            x = 0

        line_ver.SetPoint2([x + origin[0], dims[1] * spacing[1] + origin[1], 0.1])
        line_ver.SetPoint1([x + origin[0], origin[1], 0.1])
        """横线"""
        line_hor.SetPoint1([origin[0], y + origin[1], 0.1])
        line_hor.SetPoint2([dims[0] * spacing[0] + origin[0], y + origin[1], 0.1])
    elif ori == 1:
        if x > spacing[0] * dims[0]:
            x = spacing[0] * dims[0]
        if x < 0:
            x = 0
        if y>spacing[1]*dims[2]:
            y = spacing[1]*dims[2]
        if y<0:
            y = 0

        line_ver.SetPoint2([x + origin[0], dims[2] * spacing[1] + origin[1], 0.1])
        line_ver.SetPoint1([x + origin[0], origin[1], 0.1])
        line_hor.SetPoint1([origin[0], y + origin[1], 0.1])
        line_hor.SetPoint2([dims[1] * spacing[0] + origin[0], y + origin[1], 0.1])
    else:
        if x > spacing[0] * dims[0]:
            x = spacing[0] * dims[0]
        if x < 0:
            x = 0
        if y>spacing[1]*dims[2]:
            y = spacing[1]*dims[2]
        if y<0:
            y = 0

        line_ver.SetPoint2([x + origin[0], dims[2] * spacing[1] + origin[1], 0.1])
        line_ver.SetPoint1([x + origin[0], origin[1], 0.1])
        line_hor.SetPoint1([origin[0], y + origin[1], 0.1])
        line_hor.SetPoint2([dims[0] * spacing[0] + origin[0], y + origin[1], 0.1])

    line_hor.Update()
    line_ver.Update()


def ReadPolyData(path):
    polyData = vtk.vtkPolyData()

    if path.endswith('.ply'):
        reader = vtk.vtkPLYReader()
        reader.SetFileName(path)
        reader.Update()
        polyData = reader.GetOutput()
    elif path.endswith('.vtp'):
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(path)
        reader.Update()
        polyData = reader.GetOutput()
    elif path.endswith('.obj'):
        reader = vtk.vtkOBJReader()
        reader.SetFileName(path)
        reader.Update()
        polyData = reader.GetOutput()
    elif path.endswith('.stl'):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(path)
        reader.Update()
        polyData = reader.GetOutput()
    elif path.endswith('.vtk'):
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(path)
        reader.Update()
        polyData = reader.GetOutput()
    else:
        return False

    return polyData


def ReadImage(path):
    if path.endswith('jpeg') or path.endswith('jpg'):
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(path)
    elif path.endswith('png'):
        reader = vtk.vtkPNGReader()
        reader.SetFileName(path)
    elif path.endswith('bmp'):
        reader = vtk.vtkBMPReader()
        reader.SetFileName(path)
    elif path.endswith('tif'):
        reader = vtk.vtkTIFFReader()
        reader.SetFileName(path)
    elif path.endswith('mha'):
        reader = vtk.vtkMetaImageReader()
        reader.SetFileName(path)
    else:
        return False
    return reader


if __name__ == '__main__':
    # result = read_img('/home/icml-hqu/PycharmProjects/medical/dicom/series-00000/image-00000.dcm')
    # result = read_img('/data/datasets/ribfrac/ribfrac-train-images/train_image/RibFrac101-image.nii.gz')
    result = read_img('/media/icml/wbh/RawData/RawData/dataset/dataset0/labelsTr/label0003.nii.gz')
    print(result.GetOrigin())
    print(result.GetSpacing())
    print(result.GetDirection())
    img = sitk.GetArrayFromImage(result)
    # save_img('segment.nii.gz', img, result)

    # save_img('segment.dcm', img, result)
    print(img.shape)
    print(img.dtype)


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
