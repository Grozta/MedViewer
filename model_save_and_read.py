#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os

from vtkmodules.all import *
from util import is_contain_chinese


def save_actors(actors, polydatas, name,renderer):
    """
    保存actor以及相应的属性
    不要用XXXExporter!不要用XXXExporter!!不要用XXXExporter!!!
    用XXXExporter导出的结果背面是黑的
    至于为什么这样写，太过复杂，自己体会
    """

    basename = os.path.basename(name)
    file_name, file_type = os.path.splitext(basename)
    path = os.path.dirname(name)
    # actors = renderer.GetActors()
    # actors.InitTraversal()

    if '.stl' == file_type:
        os.makedirs(os.path.join(path, file_name), exist_ok=True)
        for i,actor in enumerate(actors):
            pd = vtkPolyData()
            pd.DeepCopy(actor.GetMapper().GetInput())
            writer = vtkSTLWriter()
            save_path = os.path.join(path, file_name, f'{file_name}-{i}{file_type}')
            if is_contain_chinese(save_path):
                return False
            # if os.path.isfile(save_path):
            #     os.remove(save_path)
            writer.SetFileName(save_path)
            writer.SetInputData(pd)
            writer.Write()
    elif '.ply' == file_type:
        os.makedirs(os.path.join(path, file_name), exist_ok=True)
        for i, ply in enumerate(polydatas):
            writer = vtkPLYWriter()
            save_path = os.path.join(path, file_name, f'{file_name}-{i}{file_type}')
            if is_contain_chinese(save_path):
                return False
            # if os.path.isfile(save_path):
            #     os.remove(save_path)
            writer.SetFileName(save_path)
            writer.SetInputData(ply)
            # writer.SetInputConnection(ply.GetOutputPort())
            writer.Write()
    else:
        if is_contain_chinese(name):
            return False
        mbd = vtkMultiBlockDataSet()
        mbd.SetNumberOfBlocks(len(actors))

        for i,actor in enumerate(actors):
            pd = vtkPolyData()
            pd.DeepCopy(actor.GetMapper().GetInput())
            mbd.SetBlock(i, pd)

            """保存一系列属性"""
            SaveCameraAsFieldData("Camera", renderer.GetActiveCamera(), pd)
            SavePropertyAsFieldData("Property", actor.GetProperty(), pd)
            SavePropertyAsFieldData("BackfaceProperty", actor.GetBackfaceProperty(), pd)
            SaveMapperAsFieldData("PolyDataMapper", actor.GetMapper(), pd)
            SaveActorAsFieldData("Actor", actor, pd)

        writer = vtkXMLMultiBlockDataWriter()

        writer.SetDataModeToAscii()
        writer.SetInputData(mbd)
        writer.SetFileName(name)  # TODO 不能用固定的名字
        writer.Write()
        os.remove(name)

    return True


def SAVE_SCALAR(arrayPrefix, instance, pd, name, T):
    T.SetNumberOfComponents(1)
    T.SetNumberOfTuples(1)
    try:
        T.SetValue(0, getattr(instance, 'Get' + name)())
    except:
        T.SetValue(0, int(getattr(instance, 'Get' + name)()))
    T.SetName(arrayPrefix + ":" + name)
    pd.GetFieldData().AddArray(T)


def SAVE_VECTOR(arrayPrefix, instance, pd, name, T, components, tuples):
    T.SetNumberOfComponents(components)
    T.SetNumberOfTuples(tuples)
    T.SetTuple(0, getattr(instance, 'Get' + name)())
    T.SetName(arrayPrefix + ":" + name)
    pd.GetFieldData().AddArray(T)


def SaveCameraAsFieldData(arrayPrefix, camera, pd):
    SAVE_VECTOR(arrayPrefix, camera, pd, 'ViewUp', vtkDoubleArray(), 3, 1)
    SAVE_VECTOR(arrayPrefix, camera, pd, 'Position', vtkDoubleArray(), 3, 1)
    SAVE_VECTOR(arrayPrefix, camera, pd, 'FocalPoint', vtkDoubleArray(), 3, 1)
    SAVE_VECTOR(arrayPrefix, camera, pd, 'ClippingRange', vtkDoubleArray(), 2, 1)
    SAVE_SCALAR(arrayPrefix, camera, pd, 'ViewAngle', vtkDoubleArray())


def SavePropertyAsFieldData(arrayPrefix, property, pd):
    if property:
        SAVE_SCALAR(arrayPrefix, property, pd, 'Ambient', vtkDoubleArray())
        SAVE_VECTOR(arrayPrefix, property, pd, 'AmbientColor', vtkDoubleArray(), 3, 1)
        SAVE_SCALAR(arrayPrefix, property, pd, 'Diffuse', vtkDoubleArray())
        SAVE_VECTOR(arrayPrefix, property, pd, 'DiffuseColor', vtkDoubleArray(), 3, 1)
        SAVE_SCALAR(arrayPrefix, property, pd, 'Specular', vtkDoubleArray())
        SAVE_VECTOR(arrayPrefix, property, pd, 'SpecularColor', vtkDoubleArray(), 3, 1)
        SAVE_SCALAR(arrayPrefix, property, pd, 'SpecularPower', vtkDoubleArray())
        SAVE_VECTOR(arrayPrefix, property, pd, 'EdgeColor', vtkDoubleArray(), 3, 1)
        SAVE_SCALAR(arrayPrefix, property, pd, 'EdgeVisibility', vtkIntArray())
        SAVE_VECTOR(arrayPrefix, property, pd, 'VertexColor', vtkDoubleArray(), 3, 1)
        SAVE_VECTOR(arrayPrefix, property, pd, 'Color', vtkDoubleArray(), 3, 1)
        SAVE_SCALAR(arrayPrefix, property, pd, 'Interpolation', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'Opacity', vtkDoubleArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'Representation', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'BackfaceCulling', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'FrontfaceCulling', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'PointSize', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'LineWidth', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'LineStipplePattern', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'LineStippleRepeatFactor',
                    vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'Lighting', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'RenderPointsAsSpheres', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, property, pd, 'Shading', vtkIntArray())

        # if property.GetMaterialName():
        #     SAVE_SCALAR(arrayPrefix, property, pd, MaterialName, vtkStringArray)


def SaveMapperAsFieldData(arrayPrefix, mapper, pd):
    if mapper.GetLookupTable():
        prefix = arrayPrefix + "LookupTable:"
        scalarsToColors = mapper.GetLookupTable()

        SAVE_SCALAR(prefix, scalarsToColors, pd, 'Alpha', vtkDoubleArray)
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'VectorMode', vtkIntArray)
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'VectorComponent', vtkIntArray)
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'VectorSize', vtkIntArray)
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'IndexedLookup', vtkIntArray)

        lut = mapper.GetLookupTable()
        SAVE_VECTOR(prefix, lut, pd, 'TableRange', vtkDoubleArray, 2, 1)
        SAVE_SCALAR(prefix, lut, pd, 'Scale', vtkIntArray)
        SAVE_VECTOR(prefix, lut, pd, 'HueRange', vtkDoubleArray, 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'SaturationRange', vtkDoubleArray, 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'ValueRange', vtkDoubleArray, 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'AlphaRange', vtkDoubleArray, 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'NanColor', vtkDoubleArray, 4, 1)
        SAVE_VECTOR(prefix, lut, pd, 'BelowRangeColor', vtkDoubleArray, 4, 1)
        SAVE_SCALAR(prefix, lut, pd, 'UseBelowRangeColor', vtkIntArray)
        SAVE_VECTOR(prefix, lut, pd, 'AboveRangeColor', vtkDoubleArray, 4, 1)
        SAVE_SCALAR(prefix, lut, pd, 'UseAboveRangeColor', vtkIntArray)
        SAVE_SCALAR(prefix, lut, pd, 'NumberOfTableValues', vtkIntArray)
        SAVE_SCALAR(prefix, lut, pd, 'Ramp', vtkIntArray)
        SAVE_SCALAR(prefix, lut, pd, 'NumberOfColors', vtkIntArray)

        Table = vtkUnsignedCharArray()
        # Table.SetNumberOfComponents(4)
        # Table.SetNumberOfTuples(lut.GetTable().GetNumberOfTuples())
        Table.DeepCopy(lut.GetTable())
        Table.SetName((arrayPrefix + ":LookupTable:" + "Table"))
        pd.GetFieldData().AddArray(Table)

        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ScalarVisibility', vtkIntArray)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'Static', vtkIntArray)
        SAVE_VECTOR(arrayPrefix, mapper, pd, 'ScalarRange', vtkDoubleArray, 2, 1)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'UseLookupTableScalarRange',
                    vtkIntArray)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ColorMode', vtkIntArray)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'InterpolateScalarsBeforeMapping',
                    vtkIntArray)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ScalarMode', vtkIntArray)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ResolveCoincidentTopology',
                    vtkIntArray)


def SaveActorAsFieldData(arrayPrefix, actor, pd):
    SAVE_SCALAR(arrayPrefix, actor, pd, 'Dragable', vtkIntArray())
    SAVE_SCALAR(arrayPrefix, actor, pd, 'Pickable', vtkIntArray())
    SAVE_SCALAR(arrayPrefix, actor, pd, 'Visibility', vtkIntArray())
    SAVE_VECTOR(arrayPrefix, actor, pd, 'Orientation', vtkDoubleArray(), 3, 1)
    SAVE_VECTOR(arrayPrefix, actor, pd, 'Origin', vtkDoubleArray(), 3, 1)
    SAVE_VECTOR(arrayPrefix, actor, pd, 'Scale', vtkDoubleArray(), 3, 1)
    SAVE_SCALAR(arrayPrefix, actor, pd, 'ForceOpaque', vtkIntArray())
    SAVE_SCALAR(arrayPrefix, actor, pd, 'ForceTranslucent', vtkIntArray())

    if actor.GetUserTransform():
        userTransform = actor.GetUserTransform()
        # userTransform.Print(std::cout)


def SaveMapperAsFieldData(arrayPrefix, mapper, pd):
    if mapper.GetLookupTable():
        prefix = arrayPrefix + "LookupTable:"
        scalarsToColors = mapper.GetLookupTable()

        SAVE_SCALAR(prefix, scalarsToColors, pd, 'Alpha', vtkDoubleArray())
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'VectorMode', vtkIntArray())
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'VectorComponent', vtkIntArray())
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'VectorSize', vtkIntArray())
        SAVE_SCALAR(prefix, scalarsToColors, pd, 'IndexedLookup', vtkIntArray())

        lut = mapper.GetLookupTable()
        SAVE_VECTOR(prefix, lut, pd, 'TableRange', vtkDoubleArray(), 2, 1)
        SAVE_SCALAR(prefix, lut, pd, 'Scale', vtkIntArray())
        SAVE_VECTOR(prefix, lut, pd, 'HueRange', vtkDoubleArray(), 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'SaturationRange', vtkDoubleArray(), 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'ValueRange', vtkDoubleArray(), 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'AlphaRange', vtkDoubleArray(), 2, 1)
        SAVE_VECTOR(prefix, lut, pd, 'NanColor', vtkDoubleArray(), 4, 1)
        SAVE_VECTOR(prefix, lut, pd, 'BelowRangeColor', vtkDoubleArray(), 4, 1)
        SAVE_SCALAR(prefix, lut, pd, 'UseBelowRangeColor', vtkIntArray())
        SAVE_VECTOR(prefix, lut, pd, 'AboveRangeColor', vtkDoubleArray(), 4, 1)
        SAVE_SCALAR(prefix, lut, pd, 'UseAboveRangeColor', vtkIntArray())
        SAVE_SCALAR(prefix, lut, pd, 'NumberOfTableValues', vtkIntArray())
        SAVE_SCALAR(prefix, lut, pd, 'Ramp', vtkIntArray())
        SAVE_SCALAR(prefix, lut, pd, 'NumberOfColors', vtkIntArray())

        Table = vtkUnsignedCharArray()

        Table.DeepCopy(lut.GetTable())
        Table.SetName(arrayPrefix + ":LookupTable:" + "Table")
        pd.GetFieldData().AddArray(Table)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ScalarVisibility', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'Static', vtkIntArray())
        SAVE_VECTOR(arrayPrefix, mapper, pd, 'ScalarRange', vtkDoubleArray(), 2, 1)
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'UseLookupTableScalarRange',
                    vtkIntArray())
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ColorMode', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'InterpolateScalarsBeforeMapping',
                    vtkIntArray())
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ScalarMode', vtkIntArray())
        SAVE_SCALAR(arrayPrefix, mapper, pd, 'ResolveCoincidentTopology',
                    vtkIntArray())


def read_model(filepath):
    """
    同上，等待大佬优化
    """
    # TODO 把读出的结果显示在软件里
    colors = vtkNamedColors()
    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ImportMultiBlockScene(renderer, filepath)
    renderer.SetBackground(colors.GetColor3d("Silver"))
    renWin.SetSize(600, 600)
    renWin.Render()
    iren.Start()


def ImportMultiBlockScene(renderer, filename):
    camera = renderer.GetActiveCamera()
    reader = vtkXMLMultiBlockDataReader()
    reader.SetFileName(filename)
    reader.Update()

    input = reader.GetOutput()
    iter = vtkDataObjectTreeIterator()
    iter.SetDataSet(input)
    iter.SkipEmptyNodesOn()
    iter.VisitOnlyLeavesOn()
    iter.InitTraversal()

    while not iter.IsDoneWithTraversal():
        dso = iter.GetCurrentDataObject()
        pd = vtkPolyData()
        pd.DeepCopy(dso)
        RestoreCameraFromFieldData("Camera", camera, pd)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(pd)

        actor = vtkActor()
        actor.SetMapper(mapper)
        RestorePropertyFromFieldData("Property", actor.GetProperty(), pd)
        backProperty = vtkProperty()
        actor.SetBackfaceProperty(backProperty)
        RestorePropertyFromFieldData("BackfaceProperty", actor.GetBackfaceProperty(), pd)
        RestoreActorFromFieldData("Actor", actor, pd)
        renderer.AddActor(actor)
        iter.GoToNextItem()


def RestoreCameraFromFieldData(arrayPrefix, camera, pd):
    fd = pd.GetFieldData()
    camera.SetFocalPoint(fd.GetArray(arrayPrefix + ":" + "FocalPoint").GetTuple(0))
    camera.SetPosition(fd.GetArray(arrayPrefix + ":" + "Position").GetTuple(0))
    camera.SetViewUp(fd.GetArray(arrayPrefix + ":" + "ViewUp").GetTuple(0))
    camera.SetClippingRange(fd.GetArray(arrayPrefix + ":" + "ClippingRange").GetTuple(0))
    camera.SetViewAngle(fd.GetArray(arrayPrefix + ":" + "ViewAngle").GetTuple1(0))


def RestorePropertyFromFieldData(arrayPrefix, property, pd):
    if property:
        fd = pd.GetFieldData()
        try:
            property.SetAmbient(fd.GetArray(arrayPrefix + ":" + "Ambient").GetTuple1(0))
        except:
            pass
        try:
            property.SetAmbientColor(fd.GetArray(arrayPrefix + ":" + "AmbientColor").GetTuple(0))
        except:
            pass
        property.SetDiffuse(fd.GetArray(arrayPrefix + ":" + "Diffuse").GetTuple1(0))
        property.SetDiffuseColor(fd.GetArray(arrayPrefix + ":" + "DiffuseColor").GetTuple(0))
        property.SetSpecular(fd.GetArray(arrayPrefix + ":" + "Specular").GetTuple1(0))
        property.SetSpecularColor(fd.GetArray(arrayPrefix + ":" + "SpecularColor").GetTuple(0))
        property.SetSpecularPower(fd.GetArray((arrayPrefix + ":" + "SpecularPower")).GetTuple1(0))
        property.SetEdgeColor(fd.GetArray((arrayPrefix + ":" + "EdgeColor")).GetTuple(0))
        property.SetEdgeVisibility(int(fd.GetArray(arrayPrefix + ":" + "EdgeVisibility").GetTuple1(0)))
        property.SetVertexColor(fd.GetArray((arrayPrefix + ":" + "VertexColor")).GetTuple(0))
        # property.SetVertexVisibility(fd.GetArray(arrayPrefix + ":" + "VertexVisibility").GetTuple1(0))
        property.SetVertexVisibility(1)
        property.SetInterpolation(int(fd.GetArray((arrayPrefix + ":" + "Interpolation")).GetTuple1(0)))
        property.SetOpacity(fd.GetArray((arrayPrefix + ":" + "Opacity")).GetTuple1(0))
        property.SetRepresentation(int(fd.GetArray((arrayPrefix + ":" + "Representation")).GetTuple1(0)))
        property.SetBackfaceCulling(int(fd.GetArray((arrayPrefix + ":" + "BackfaceCulling")).GetTuple1(0)))
        property.SetFrontfaceCulling(int(fd.GetArray((arrayPrefix + ":" + "FrontfaceCulling")).GetTuple1(0)))
        property.SetPointSize(fd.GetArray((arrayPrefix + ":" + "PointSize")).GetTuple1(0))
        property.SetLineWidth(fd.GetArray((arrayPrefix + ":" + "LineWidth")).GetTuple1(0))
        property.SetLineStipplePattern(int(fd.GetArray((arrayPrefix + ":" + "LineStipplePattern")).GetTuple1(0)))
        property.SetLineStippleRepeatFactor(
            int(fd.GetArray((arrayPrefix + ":" + "LineStippleRepeatFactor")).GetTuple1(0)))
        property.SetLighting(1.0 == fd.GetArray(arrayPrefix + ":" + "Lighting").GetTuple1(0))
        property.SetRenderPointsAsSpheres(1.0 == fd.GetArray(arrayPrefix + ":" + "RenderPointsAsSpheres").GetTuple1(0))
        # property.SetRenderLinesAsTubes(fun(fd.GetArray(arrayPrefix + ":" + "RenderLinesAsTubes").GetTuple1(0) == 1.0))
        property.SetShading(1.0 == fd.GetArray(arrayPrefix + ":" + "Shading").GetTuple1(0))


def RestoreActorFromFieldData(arrayPrefix, actor, pd):
    fd = pd.GetFieldData()

    actor.SetDragable(fd.GetArray((arrayPrefix + ":" + "Dragable")).GetTuple1(0) == 1.0)
    actor.SetPickable(fd.GetArray((arrayPrefix + ":" + "Pickable")).GetTuple1(0) == 1.0)
    actor.SetVisibility(int(fd.GetArray((arrayPrefix + ":" + "Visibility")).GetTuple1(0)))
    # actor.SetPosition(fd.GetArray((arrayPrefix + ":" + "Position")).GetTuple(0))
    actor.SetOrientation(fd.GetArray((arrayPrefix + ":" + "Orientation")).GetTuple(0))
    actor.SetOrigin(fd.GetArray((arrayPrefix + ":" + "Origin")).GetTuple(0))
    actor.SetScale(fd.GetArray((arrayPrefix + ":" + "Scale")).GetTuple(0))
    actor.SetForceOpaque(fd.GetArray((arrayPrefix + ":" + "ForceOpaque")).GetTuple1(0) == 1.0)
    actor.SetForceTranslucent(fd.GetArray((arrayPrefix + ":" + "ForceTranslucent")).GetTuple1(0) == 1.0)


if __name__ == '__main__':
    read_model('ddd3.vtk')
