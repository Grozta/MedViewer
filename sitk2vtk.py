#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import vtkmodules.all as vtk

# from vtk.util.vtkConstants import *
from vtkmodules.all import *


# filename = sys.argv[1]

def numpy2VTK_new(img, spacing=(1.0, 1.0, 1.0)):
    # evolved from code from Stou S.,
    # on http://www.siafoo.net/snippet/314
    importer = vtkImageImport()

    img_f = img.flatten().tolist()
    img_f = list(set(img_f))
    num_labels = len(img_f) - 1
    labels = []
    for i in range(num_labels):
        v = img_f[i + 1]
        img[img == v] = i + 1
        labels.append(i + 1)

    img_data = img.astype('uint8')
    img_string = img_data.tostring()  # type short
    dim = img.shape

    importer.CopyImportVoidPointer(img_string, len(img_string))
    importer.SetDataScalarType(VTK_UNSIGNED_CHAR)
    importer.SetNumberOfScalarComponents(1)

    extent = importer.GetDataExtent()
    importer.SetDataExtent(extent[0], extent[0] + dim[2] - 1,
                           extent[2], extent[2] + dim[1] - 1,
                           extent[4], extent[4] + dim[0] - 1)
    importer.SetWholeExtent(extent[0], extent[0] + dim[2] - 1,
                            extent[2], extent[2] + dim[1] - 1,
                            extent[4], extent[4] + dim[0] - 1)

    importer.SetDataSpacing(spacing[0], spacing[1], spacing[2])
    importer.SetDataOrigin(0, 0, 0)

    return importer, num_labels, labels


def make_colors(n,color):
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfColors(n)
    lut.SetTableRange(0, n - 1)
    lut.SetScaleToLinear()
    lut.Build()
    lut.SetTableValue(0, 0, 0, 0, 1)

    randomSeq = vtk.vtkMinimalStandardRandomSequence()
    randomSeq.SetSeed(4396)
    color = [1]+color+[1]
    lut.SetTableValue(*color)
    # lut.SetTableValue(2, 0, 1, 0, 1)
    # lut.SetTableValue(3, 1, 0, 0, 1)
    return lut

def get_colcor(name):
    if name == 'red':
        color = [1,0,0]
    elif name == 'yellow':
        color = [1,1,0]
    elif name =='blue':
        color = [0,0,1]
    else:
        color = [0,0.8686,0.3411]
    return color

def get_Isosurface(reader,num_labels,labels, spacing=(1.0, 1.0, 1.0)):
    # reader, num_labels, labels = numpy2VTK_new(img, spacing)
    colors = vtkNamedColors()
    actors = []
    color_ = ['red', 'lightgreen', 'yellow', 'blue']
    polydatas = []
    for label, c in zip(labels, color_):
        the = vtkImageThreshold()
        the.SetInputConnection(reader.GetOutputPort())
        the.ThresholdBetween(label,label)
        the.ReplaceInOn()
        the.ReplaceOutOn()
        the.SetInValue(1)
        the.SetOutValue(0)
        the.Update()

        extractor = vtkContourFilter()
        extractor.SetInputConnection(the.GetOutputPort())
        extractor.ComputeGradientsOff()
        extractor.ComputeNormalsOff()
        # extractor.ComputeScalarsOff()
        extractor.SetValue(0,1)
        extractor.Update()

        smooth = smooth_functions(extractor, 1)
        smooth.Update()



        stripper = vtkStripper()
        stripper.SetInputConnection(smooth.GetOutputPort())
        stripper.Update()

        tf = vtkTriangleFilter()
        tf.SetInputConnection(smooth.GetOutputPort())
        tf.Update()

        decimate = vtkDecimatePro()
        decimate.SetInputData(tf.GetOutput())
        decimate.SetTargetReduction(0.6)
        decimate.PreserveTopologyOn()
        decimate.Update()

        color = get_colcor(c)

        lut = make_colors(2,color)

        mapper = vtkPolyDataMapper()

        mapper.SetInputConnection(decimate.GetOutputPort())
        mapper.SetLookupTable(lut)
        mapper.SetScalarRange(0, lut.GetNumberOfColors())


        bp = vtkProperty()
        bp.SetColor(colors.GetColor3d(c))
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d(c))
        actor.SetBackfaceProperty(bp)
        actors.append(actor)
        polydatas.append(decimate)
    return actors,polydatas


def get_actors(img, tf=[], spacing=(1.0, 1.0, 1.0)):
    reader, num_labels, labels = numpy2VTK_new(img, spacing)
    colors = vtkNamedColors()
    actors = []
    color_ = ['red', 'lightgreen', 'yellow', 'blue']
    for label, c in zip(labels, color_):
        extractor = vtkDiscreteMarchingCubes()
        extractor.SetInputConnection(reader.GetOutputPort())
        extractor.SetValue(0, label)

        smooth = smooth_functions(extractor, 1)
        smooth.Update()

        stripper = vtkStripper()
        stripper.SetInputConnection(smooth.GetOutputPort())

        mapper = vtkPolyDataMapper()
        # mapper.SetInputData(smooth.GetOutput())
        mapper.SetInputConnection(stripper.GetOutputPort())
        # mapper.ScalarVisibilityOff()

        bp = vtkProperty()
        bp.SetColor(colors.GetColor3d(c))
        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d(c))
        actor.SetBackfaceProperty(bp)
        actors.append(actor)
    # appendpoly = vtkAppendPolyData()
    # for label, color in zip(labels, Colors):
    #     pointColors = vtkUnsignedCharArray()
    #     pointColors.SetNumberOfComponents(3)
    #
    #     extractor = vtkDiscreteMarchingCubes()
    #     extractor.SetInputConnection(reader.GetOutputPort())
    #     extractor.SetValue(0, label)
    #
    #
    #     smooth = smooth_functions(extractor, 1)
    #     output = smooth.GetOutput()
    #
    #     for i in range(output.GetNumberOfPoints()):
    #         pointColors.InsertNextTuple3(*color)
    #
    #     output.GetPointData().SetScalars(pointColors)
    #     appendpoly.AddInputData(output)
    #
    # mapper = vtkPolyDataMapper()
    # mapper.SetInputConnection(appendpoly.GetOutputPort())
    # # mapper.ScalarVisibilityOff()
    # color = vtkNamedColors()
    # actor = vtkActor()
    # actor.SetMapper(mapper)
    # actor.GetProperty().SetDiffuseColor(color.GetColor3d('red'))
    #
    # actors.append(actor)
    return actors


def smooth_functions(dmc, fid=1):
    if 1 == fid:
        smooth = vtk.vtkSmoothPolyDataFilter()
        smooth.ReleaseDataFlagOn()  # TODO
        smooth.SetInputConnection(dmc.GetOutputPort())
        smooth.SetNumberOfIterations(300)
        smooth.SetRelaxationFactor(0.03)
        smooth.SetFeatureAngle(160.0)
        smooth.SetFeatureEdgeSmoothing(False)
        smooth.SetBoundarySmoothing(False)
        # smooth.FeatureEdgeSmoothingOn();
        # smooth.BoundarySmoothingOn();
        smooth.Update()

    if fid == 2:
        smooth_iterations = 30
        passBand = 0.001
        featureAngle = 140.0

        smooth = vtk.vtkWindowedSincPolyDataFilter()
        smooth.SetInputConnection(dmc.GetOutputPort())
        smooth.SetNumberOfIterations(smooth_iterations)
        smooth.SetRelaxationFactor(0.1)
        smooth.FeatureEdgeSmoothingOn()
        # smooth.BoundarySmoothingOff()
        smooth.BoundarySmoothingOn()
        smooth.FeatureEdgeSmoothingOn()
        smooth.SetFeatureAngle(featureAngle)
        smooth.SetPassBand(passBand)
        smooth.NonManifoldSmoothingOn()
        smooth.NormalizeCoordinatesOn()
        smooth.Update()
    return smooth


def vtk_basic(actors):
    """
    Create a window, renderer, interactor, add the actors and start the thing

    Parameters
    ----------
    actors :  list of vtkActors

    Returns
    -------
    nothing
    """

    # create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(600, 600)
    # ren.SetBackground( 1, 1, 1)

    # create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    for a in actors:
        # assign actor to the renderer
        ren.AddActor(a)

    # render
    renWin.Render()

    # enable user interface interactor
    iren.Initialize()
    iren.Start()
