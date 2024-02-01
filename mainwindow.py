from ui_main_window import Ui_Form
from PyQt5.QtWidgets import QMenu, QAction, QToolButton, QApplication
from VTKWindow import VTKWindow
from MessageBox import HQUMessageBox

import torch, gc

gc.collect()
torch.cuda.empty_cache()

import multiprocessing
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import time
from functools import partial

import SimpleITK as sitk
import numpy as np

from PyQt5.QtCore import Qt, QCoreApplication, QSize, QObject, pyqtSignal, pyqtSlot, QThread, QRect, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QWidget, QHBoxLayout, QApplication, \
    QTableWidgetItem, QLabel, QDialog, QProgressBar, QHeaderView, QMessageBox
import cv2
from vtkmodules.all import *
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from Classification.src_rct.classify_injury import load_and_process_image
from ImgWidget1 import ImgWidget1
from LabelColor import LabelColor
from LabelEditorDialog_window import LabelEditorDialogWindow
from Operative.Module.play_img import playimg2
from Operative.Module.seg_test2 import operative_load_model, deal_single_image
from Rib_segment import seg_rib
from batch_seg import batch_segmentation
from classify_window import ClassifyWindow
from contrast_window import ContrastWindow
from evaluation import directory_dice
from model_save_and_read import save_actors
from pelvic_segment import pelvic_segment
from pelvic_segment_cs_net import pelvic_segment_cs_net
from sitk2vtk import get_Isosurface
from util import read_img, save_img, numpy2vtkImageImport, resliceByOrient, add_cross_hair, cross_hair_actors, get_ori, \
    set_Line, ReadPolyData, registration_by_itk_elastix, get_base_dir, ReadImage, sitk_image_to_itk_image, \
    is_contain_chinese

base_dir = get_base_dir()


class ThreadObject(QObject):
    _progressBar_signal = pyqtSignal()

    def __init__(self, func=None):
        super(ThreadObject, self).__init__()
        self.func = func

    @pyqtSlot()
    def run(self):
        if self.func:
            try:
                self.func()
            except Exception as e:
                print(e)
        print('end')
        self._progressBar_signal.emit()


class ProgressBar(QObject):
    def __init__(self, parent=None, func=None, title: str = '', context: str = ''):
        super(ProgressBar, self).__init__(parent)
        # self.setWindowFlags((self.windowFlags() |
        #                      Qt.WindowTitleHint |
        #                      Qt.WindowStaysOnTopHint |
        #                      Qt.CustomizeWindowHint)
        #                     & (~Qt.WindowCloseButtonHint)
        #                     & (~Qt.WindowContextHelpButtonHint))
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        # #self.setWindowTitle('Processing')
        # self.setWindowIcon(QIcon(os.path.join(base_dir, 'resources', 'HQU_logo1.png')))
        # self.setFixedSize(500, 32)
        # self.progressBar = QProgressBar(self)  # 创建
        # self.progressBar.setMinimum(0)  # 设置进度条最小值
        # self.progressBar.setMaximum(100)  # 设置进度条最大值
        # self.progressBar.setTextVisible(False)
        # self.progressBar.setValue(0)  # 进度条初始值为0
        # self.progressBar.setGeometry(QRect(1, 3, 499, 28))  # 设置进度条在 QDialog 中的位置 [左，上，右，下]
        self.thread = QThread(self)
        self.thread_object = ThreadObject(func=func)
        self.thread_object.moveToThread(self.thread)
        self.thread_object._progressBar_signal.connect(self.end)
        self.thread.started.connect(self.thread_object.run)
        self.thread.finished.connect(self.thread_object.deleteLater)
        self.messageBox = HQUMessageBox.status(parent, title, context)
        self.thread.started.connect(lambda: self.messageBox.exec_())
        self.thread.start()

    @pyqtSlot()
    def end(self):
        self.messageBox.close()
        # 线程退出
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        if self.thread is not None:
            del self.thread
        self.close()


class WorkThread(QThread):
    """

    """
    _progressBar_signal = pyqtSignal()

    def __init__(self, func=None):
        super(WorkThread, self).__init__()
        self.func = func

    @pyqtSlot()
    def run(self):
        if self.func:
            try:
                self.func()
            except Exception as e:
                print(e)
        print('end')
        self._progressBar_signal.emit()


class ProgressBarWithText(QDialog):
    """
    带百分比的进度条
    """

    def __init__(self, parent=None, func=None):
        super(ProgressBarWithText, self).__init__(parent)
        self.setWindowFlags((self.windowFlags() |
                             Qt.WindowTitleHint |
                             Qt.WindowStaysOnTopHint |
                             Qt.CustomizeWindowHint)
                            & (~Qt.WindowCloseButtonHint)
                            & (~Qt.WindowContextHelpButtonHint))
        self.setWindowTitle('Processing')
        self.setWindowIcon(QIcon(os.path.join(base_dir, 'resources', 'HQU_logo1.png')))
        self.setFixedSize(500, 32)
        self.progressBar = QProgressBar(self)  # 创建
        self.progressBar.setMinimum(0)  # 设置进度条最小值
        self.progressBar.setMaximum(100)  # 设置进度条最大值
        self.progressBar.setValue(0)  # 进度条初始值为0
        self.progressBar.setGeometry(QRect(1, 3, 499, 28))  # 设置进度条在 QDialog 中的位置 [左，上，右，下]

        self.thread = QThread()
        self.thread_object = ThreadObject(func=partial(func, self.update_value))
        self.thread_object.moveToThread(self.thread)
        self.thread_object._progressBar_signal.connect(self.end)
        self.thread.started.connect(self.thread_object.run)
        self.thread.finished.connect(self.thread_object.deleteLater)
        self.thread.start()

    def update_value(self, value):
        self.progressBar.setValue(value)

    @pyqtSlot()
    def end(self):
        # 线程退出
        self.progressBar.setValue(100)
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        if self.thread is not None:
            del self.thread
        if self.thread_object is not None:
            del self.thread_object
        self.close()


class MainWindow(QWidget, Ui_Form):
    class VTKLayout():
        DeaultLayout = 0
        """1大3小"""
        No3DLayout = 1
        """1大2小，没有3D"""
        PainLayout = 2
        """4小"""
        SingelLayout = 3
        """只显示一张图"""

    Margins = 0
    """四周边距"""
    _pressed = False  # 拉升参数
    Direction = None
    mPos = None
    # 枚举左上右下以及四个定点
    Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)
    # 顶部可移动窗口移动鼠标位置
    headmPos = None

    # 图
    transverse = None
    """# 左上 横断面"""
    sagittal = None
    """#右上 矢状面"""
    coronal = None
    """# 右下 冠状面"""
    restruct_3d = None
    """# 左下 3维重建"""

    _layoutForVtkInCurentWindow = None
    """ 当前窗口中vtk的布局风格"""

    _vtkListInCurentWindow = None
    """ 当前窗口中vtk的窗口widget列表"""

    def __init__(self, parent=None):
        self.initUiForWindow(parent)
        self.registration_init()
        self.var_init()
        self.vtk_init()
        self.render3d = [None, None, None, None, None]
        self.set_style = False  # 初始化style

    def var_init(self):
        """
        清空变量
        """
        self.main_image = None  # 主图像
        self.label_main = None  # 标签，为None时不能建模
        self.image = None  # 主图像numpy
        self.label = None  # 标签numpy
        self.label_origin = None  # 标签numpy（原始的）
        self.dims = None  # (x,y,z),(S,C,A)

        self.minimum = 0  # 主图像最小值
        self.maximum = 0  # 主图像最大值
        self.level = 0  # 主图像窗位
        self.window = 0  # 主图像窗宽
        self.filename = ''

        self.lines = [[0, 0], [0, 0], [0, 0]]  # 三个框的十字线
        self.Origins = [0] * 3  # 三个框最初的切片的Origin
        self.textActors = [None] * 3

        self.img_center = [0] * 3  # 切片中心
        self.image_actors = [None] * 3
        self.num_labels = None  # 标签个数
        self.num2labels = None  # 每个标签对应的数值

        self.reader1 = None  # 主图片转成vtkImageImporter
        self.reader2 = None  # 标签转成vtkImageImporter

        self.image_color_map = None  # 主图片颜色映射
        self.label_color_map = None  # 标签颜色映射

        self.ren_top_left = None
        self.ren_top_right = None
        self.ren_bot_left = None
        self.ren_bot_right = None
        self.model_ren = None
        self.num_models = 0
        self.ren_init()
        self.clicked = False  # 有没有点过

        self.image_path = ''  # 记录当前打开的文件的路径
        # self.rib_save_list = 'predict_label/rib'  # 肋骨预测结果保存目录

        self.polydatas = []  # 用于保存ply文件

        self.Assembly = []
        try:
            self.tableWidget_3d.clearContents()
            self.tableWidget_3d.setDisabled(True)
            self.tableWidget_3d.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

            self.tableWidget_3d.setColumnWidth(0, 224)
            self.tableWidget_3d.setColumnWidth(1, 40)
            self.tableWidget_3d.setColumnWidth(2, 40)
            self.tableWidget_3d.setColumnWidth(3, 40)
            self.tableWidget_3d.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
            self.num_models = 0
        except:
            pass

        self.tableWidget_seg.setRowCount(0)
        self.tableWidget_seg.clearContents()
        self.tableWidget_seg.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.tableWidget_seg.setColumnWidth(0, 264)
        self.tableWidget_seg.setColumnWidth(1, 40)
        self.tableWidget_seg.setColumnWidth(2, 40)
        self.tableWidget_seg.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.operative_model = None  # 手术器械分割
        self.main_image_shape = None  # 图像的shape

        self.contrast_window = None
        self.label_editor_dialog_window = None
        self.video_window = None
        self.classifyWindow = None

        self.left_button_press_flag = False  # 是否按下左键

    def vtk_init(self):
        """
        transverse 是横断面
        sagittal 是矢状面
        coronal 冠状面
        restruct_3d 3维重建
        """
        item_list = list(range(self.gridLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.gridLayout.itemAt(i)
            self.gridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        displayVtkList = []
        """左"""
        self.transverse = QVTKRenderWindowInteractor(self.mian)
        self.transverse.GetRenderWindow().GetInteractor().Start()
        self.transverseWidget = VTKWindow(vtkInteractWindow=self.transverse, name="transverse", parent=self.mian)
        self.transverseWidget.getScrollBar().valueChanged.connect(self.change_axial)
        self.transverseWidget.toolButton_vtkTrans.clicked.connect(self.vtkLayoutManager)
        displayVtkList.append(self.transverseWidget)
        """右上"""
        self.sagittal = QVTKRenderWindowInteractor(self.mian)
        self.sagittal.GetRenderWindow().GetInteractor().Start()
        self.sagittalWidget = VTKWindow(vtkInteractWindow=self.sagittal, name="sagittal", parent=self.mian)
        self.sagittalWidget.getScrollBar().valueChanged.connect(self.change_sagi)
        self.sagittalWidget.toolButton_vtkTrans.clicked.connect(self.vtkLayoutManager)
        displayVtkList.append(self.sagittalWidget)
        """右中"""
        self.coronal = QVTKRenderWindowInteractor(self.mian)
        self.coronal.GetRenderWindow().GetInteractor().Start()
        self.coronalWidget = VTKWindow(vtkInteractWindow=self.coronal, name="coronal", parent=self.mian)
        self.coronalWidget.getScrollBar().valueChanged.connect(self.change_corn)
        self.coronalWidget.toolButton_vtkTrans.clicked.connect(self.vtkLayoutManager)
        displayVtkList.append(self.coronalWidget)
        """右下"""
        self.restruct_3d = QVTKRenderWindowInteractor(self.mian)
        self.restruct_3d.GetRenderWindow().GetInteractor().Start()
        self.restruct_3dWidget = VTKWindow(vtkInteractWindow=self.restruct_3d, name="restruct_3d", parent=self.mian)
        self.restruct_3dWidget.getScrollBar().setVisible(False)
        self.restruct_3dWidget.sliderWindow.setVisible(True)
        self.restruct_3dWidget.horizontalSlider.setRange(0, 10)
        self.restruct_3dWidget.horizontalSlider.sliderMoved.connect(self.horizontalSlider_change)
        self.restruct_3dWidget.toolButton_vtkTrans.clicked.connect(self.vtkLayoutManager)

        self.setVTKLayout(MainWindow.VTKLayout.No3DLayout, displayVtkList)

    def setVTKLayout(self, layout, vtkList):
        MainWindow._layoutForVtkInCurentWindow = layout
        MainWindow._vtkListInCurentWindow = vtkList
        item_list = list(range(self.gridLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.gridLayout.itemAt(i)
            self.gridLayout.removeItem(item)

        if layout == MainWindow.VTKLayout.DeaultLayout:
            if len(vtkList) == 4:
                self.gridLayout.addWidget(vtkList[0], 0, 0, 3, 4)
                self.gridLayout.addWidget(vtkList[1], 0, 4, 1, 2)
                self.gridLayout.addWidget(vtkList[2], 1, 4, 1, 2)
                self.gridLayout.addWidget(vtkList[3], 2, 4, 1, 2)
                self.restruct_3dWidget.setVisible(True)

        elif layout == MainWindow.VTKLayout.No3DLayout:
            if len(vtkList) == 3:
                self.gridLayout.addWidget(vtkList[0], 0, 0, 2, 4)
                self.gridLayout.addWidget(vtkList[1], 0, 4, 1, 2)
                self.gridLayout.addWidget(vtkList[2], 1, 4, 1, 2)
                self.restruct_3dWidget.setVisible(False)
        elif layout == MainWindow.VTKLayout.PainLayout:
            if len(vtkList) == 4:
                self.gridLayout.addWidget(vtkList[0], 0, 0, 1, 1)
                self.gridLayout.addWidget(vtkList[1], 1, 0, 1, 1)
                self.gridLayout.addWidget(vtkList[2], 0, 1, 1, 1)
                self.gridLayout.addWidget(vtkList[3], 1, 1, 1, 1)
                self.restruct_3dWidget.setVisible(True)
        elif layout == MainWindow.VTKLayout.SingelLayout:
            if len(vtkList) == 1:
                self.gridLayout.addWidget(vtkList[0], 0, 0, 1, 1)
        else:
            print(self.tr("布局无效"))

    def registration_init(self):
        """
        配准变量清空
        """
        self.mode = 0  # 0表示正常，1表示对比
        self.floating_image_path = ''  # 浮动图片路径
        self.fixed_image_path = ''  # 参考图路径
        self.registration_image_path = ''  # 配准后的图的路径
        self.reader_fixed = None  # 参考图转vtkImageImporter

    def ren_init(self):
        """
        初始化三维重建
        """

        self.render_tobe = vtkRenderer()
        self.ren_top_left = vtkRenderer()
        self.ren_top_left.SetViewport(0, 0.5, 0.5, 1)
        self.ren_top_left.SetBackground(0.1, 0.2, 0.4)

        self.ren_top_right = vtkRenderer()
        self.ren_top_right.SetViewport(0.5, 0.5, 1, 1)
        self.ren_top_right.SetBackground(0.1, 0.2, 0.3)

        self.ren_bot_left = vtkRenderer()
        self.ren_bot_left.SetViewport(0, 0, 0.5, 0.5)
        self.ren_bot_left.SetBackground(0.1, 0.3, 0.4)

        self.ren_bot_right = vtkRenderer()
        self.ren_bot_right.SetViewport(0.5, 0, 1, 0.5)
        self.ren_bot_right.SetBackground(0.2, 0.2, 0.3)

        self.render3d = [None, None, None, None, None]

        for index in range(self.num_models):
            self.tableWidget_3d.removeRow(index)
        self.num_models = 0

        self.Assembly = []
        # TODO 移除所有的行

    def initUiForWindow(self, parent):
        """UI初始化，包括页面创建，按钮绑定"""
        super(QWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.setupUi(self)
        # 鼠标跟踪
        # self.normalCursor = QCursor(QPixmap("resources/icon_select.png"))
        self.normalCursor = Qt.ArrowCursor
        self.setCursor(self.normalCursor)
        # 设置窗口背景透明 # 这里会导致vtk无法绘制，具体原因还没有找到
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        # 绑定titel栏中按钮信号
        # 关闭按钮
        self.toolButton_close.clicked.connect(self.exitApp)
        # 最小化按钮
        self.toolButton_min.clicked.connect(self.showMinimized)
        # 最大化/还原按钮
        self.toolButton_max.clicked.connect(self.windowSizeChanged)
        # 安装事件过滤器
        # self.installEventFilter(self)
        self.initTitel()
        self.initTool()
        self.initWorkSpace()
        self.initMaskWidget()
        self.stackedWidget.setCurrentWidget(self.page_start)
        self.toolButton_ResetImage.setVisible(False)
        self.toolButton_ImportImage.setVisible(False)
        self.toolButton_ExportImage.setVisible(False)

    def initWorkSpace(self):
        self.tabWidget_edit.setCurrentIndex(0)
        self.tableWidget_3d.cellClicked.connect(self.onClicked)
        self.tableWidget_seg.cellClicked.connect(self.seg_table_clicked)

    def initTitel(self):
        """顶部的标题栏初始化"""
        # 添加新的按钮，绑定信号 这是【大的导入按钮】
        self.toolButton_import.clicked.connect(self.slotLoadImage)
        # 给打开文件加载菜单
        self.open_menu = QMenu(self)
        self.open_menu.setTearOffEnabled(False)
        self.open_menu.setLayoutDirection(Qt.LayoutDirection.LayoutDirectionAuto)

        self.loadImageFile_action = QAction(QIcon("resources/blueDot.png"), self.tr("导入图像文件"))  # 加载图像action
        self.loadImageFile_action.triggered.connect(self.add_main_file)
        self.open_menu.addAction(self.loadImageFile_action)

        self.loadSegmentFile_action = QAction(QIcon("resources/redDot.png"), self.tr("导入分割文件"))
        self.loadSegmentFile_action.triggered.connect(self.add_segment_file)
        self.open_menu.addAction(self.loadSegmentFile_action)

        self.loadMesh_action = QAction(QIcon("resources/blueDot.png"), self.tr("导入Mesh文件"))
        self.loadMesh_action.triggered.connect(self.Choose_Directory)
        self.open_menu.addAction(self.loadMesh_action)

        self.toolButton_ImportImage.clicked.connect(
            lambda: self.open_menu.popup(
                self.toolButton_ImportImage.mapToGlobal(self.toolButton_ExportImage.rect().bottomLeft())))

        # 给保存按钮增加菜单
        self.save_menu = QMenu(self)
        self.save_menu.setTearOffEnabled(False)
        self.save_menu.setLayoutDirection(Qt.LayoutDirection.LayoutDirectionAuto)
        self.saveImageFile_action = QAction(QIcon("resources/blueDot.png"), self.tr("导出图像文件"))  # 保存图像action
        self.saveImageFile_action.triggered.connect(self.save_main_file)
        self.save_menu.addAction(self.saveImageFile_action)

        self.saveSegmentFile_action = QAction(QIcon("resources/redDot.png"), self.tr("导出分割文件"))
        self.saveSegmentFile_action.triggered.connect(self.save_segment_file)
        self.save_menu.addAction(self.saveSegmentFile_action)

        self.saveMesh_action = QAction(QIcon("resources/blueDot.png"), self.tr("导出Mesh文件"))
        self.saveMesh_action.triggered.connect(self.save_model_file)
        self.save_menu.addAction(self.saveMesh_action)

        self.toolButton_ExportImage.clicked.connect(
            lambda: self.save_menu.popup(
                self.toolButton_ExportImage.mapToGlobal(self.toolButton_ExportImage.rect().bottomLeft())))

        # 重置按钮
        self.toolButton_ResetImage.clicked.connect(self.resetApp)

    def initTool(self):
        """初始化工具栏"""

        # 设置对齐方式
        # self.setAligmentForToolContent(qtCore.Qt.AlignLeft)
        # 给每个大功能 ，装按钮
        self.tabWidget.setCurrentWidget(self.tab_segment)
        # 目前是左对齐）
        self.tab_segment.layout().setAlignment(Qt.AlignLeft)
        self.tab_registration.layout().setAlignment(Qt.AlignLeft)
        self.tab_keyPointCheck.layout().setAlignment(Qt.AlignLeft)
        self.tab_diagnoise.layout().setAlignment(Qt.AlignLeft)
        # ------------------分割---------------------------
        # Rib分割
        self.segment_Rib = QToolButton(self.tab_segment)
        self.segment_Rib.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.segment_Rib.setToolTip(self.tr('肋骨分割'))
        self.segment_Rib.setText(self.tr('肋骨分割'))
        self.segment_Rib.setIcon(QIcon('icon/bank.ico'))
        self.segment_Rib.setAutoRaise(True)
        self.segment_Rib.clicked.connect(self.rib_seg_pipeline)
        self.tab_segment.layout().addWidget(self.segment_Rib)
        # Rib批量分割
        self.segment_Rib_Batch = QToolButton(self.tab_segment)
        self.segment_Rib_Batch.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.segment_Rib_Batch.setToolTip(self.tr('肋骨分割批量分割'))
        self.segment_Rib_Batch.setText(self.tr('肋骨批量分割'))
        self.segment_Rib_Batch.setIcon(QIcon('icon/bank.ico'))
        self.segment_Rib_Batch.setAutoRaise(True)
        self.segment_Rib_Batch.clicked.connect(self.rib_batch_segmentation)
        self.tab_segment.layout().addWidget(self.segment_Rib_Batch)
        # Pelvic I分割
        self.segment_Pelivc_I = QToolButton(self.tab_segment)
        self.segment_Pelivc_I.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.segment_Pelivc_I.setToolTip(self.tr('盆骨分割 I'))
        self.segment_Pelivc_I.setText(self.tr('盆骨分割 I'))
        self.segment_Pelivc_I.setIcon(QIcon('icon/bank.ico'))
        self.segment_Pelivc_I.setAutoRaise(True)
        self.segment_Pelivc_I.clicked.connect(self.pelvic_seg_pipeline)
        self.tab_segment.layout().addWidget(self.segment_Pelivc_I)
        # Pelvic II分割
        self.segment_Pelivc_II = QToolButton(self.tab_segment)
        self.segment_Pelivc_II.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.segment_Pelivc_II.setToolTip(self.tr('盆骨分割 II'))
        self.segment_Pelivc_II.setText(self.tr('盆骨分割 II'))
        self.segment_Pelivc_II.setIcon(QIcon('icon/bank.ico'))
        self.segment_Pelivc_II.setAutoRaise(True)
        self.segment_Pelivc_II.clicked.connect(self.pelvic_cs_net_seg_pipeline)
        self.tab_segment.layout().addWidget(self.segment_Pelivc_II)
        # Pelvic批量分割
        self.segment_Pelivc_Batch = QToolButton(self.tab_segment)
        self.segment_Pelivc_Batch.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.segment_Pelivc_Batch.setToolTip(self.tr('盆骨批量分割'))
        self.segment_Pelivc_Batch.setText(self.tr('盆骨批量分割'))
        self.segment_Pelivc_Batch.setIcon(QIcon('icon/bank.ico'))
        self.segment_Pelivc_Batch.setAutoRaise(True)
        self.segment_Pelivc_Batch.clicked.connect(self.my_batch_segmentation)
        self.tab_segment.layout().addWidget(self.segment_Pelivc_Batch)
        # 视频分割
        self.segment_Video = QToolButton(self.tab_segment)
        self.segment_Video.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.segment_Video.setToolTip(self.tr('器械分割'))
        self.segment_Video.setText(self.tr('器械分割'))
        self.segment_Video.setIcon(QIcon('icon/bank.ico'))
        self.segment_Video.setAutoRaise(True)
        self.segment_Video.clicked.connect(self.load_video)
        self.tab_segment.layout().addWidget(self.segment_Video)
        # 文件夹Dice
        self.segment_directory_dice = QToolButton(self.tab_segment)
        self.segment_directory_dice.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.segment_directory_dice.setToolTip(self.tr('文件夹Dice'))
        self.segment_directory_dice.setText(self.tr('文件夹Dice'))
        self.segment_directory_dice.setIcon(QIcon('icon/bank.ico'))
        self.segment_directory_dice.setAutoRaise(True)
        self.segment_directory_dice.clicked.connect(self.directory_dice)
        self.tab_segment.layout().addWidget(self.segment_directory_dice)
        # ------------------配准---------------------------
        # 刚性配准
        self.reg_Rigid = QToolButton(self.tab_segment)
        self.reg_Rigid.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.reg_Rigid.setToolTip(self.tr('刚性配准'))
        self.reg_Rigid.setText(self.tr('刚性配准'))
        self.reg_Rigid.setIcon(QIcon('icon/bank.ico'))
        self.reg_Rigid.setAutoRaise(True)
        self.reg_Rigid.clicked.connect(self.registration_rigid)
        self.tab_registration.layout().addWidget(self.reg_Rigid)
        # 仿射配准
        self.reg_Affine = QToolButton(self.tab_segment)
        self.reg_Affine.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.reg_Affine.setToolTip(self.tr('仿射配准'))
        self.reg_Affine.setText(self.tr('仿射配准'))
        self.reg_Affine.setIcon(QIcon('icon/bank.ico'))
        self.reg_Affine.setAutoRaise(True)
        self.reg_Affine.clicked.connect(self.registration_affine)
        self.tab_registration.layout().addWidget(self.reg_Affine)
        # 浮动图像
        self.reg_Image_float = QToolButton(self.tab_segment)
        self.reg_Image_float.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.reg_Image_float.setToolTip(self.tr('浮动图像'))
        self.reg_Image_float.setText(self.tr('浮动图像'))
        self.reg_Image_float.setIcon(QIcon('icon/bank.ico'))
        self.reg_Image_float.setAutoRaise(True)
        self.reg_Image_float.clicked.connect(self.show_floating_image)
        self.tab_registration.layout().addWidget(self.reg_Image_float)
        # 查看固定图像
        self.reg_Image_Fixed = QToolButton(self.tab_segment)
        self.reg_Image_Fixed.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.reg_Image_Fixed.setToolTip(self.tr('查看固定图像'))
        self.reg_Image_Fixed.setText(self.tr('固定图像'))
        self.reg_Image_Fixed.setIcon(QIcon('icon/bank.ico'))
        self.reg_Image_Fixed.setAutoRaise(True)
        self.reg_Image_Fixed.clicked.connect(self.show_fixed_image)
        self.tab_registration.layout().addWidget(self.reg_Image_Fixed)
        # 图像对比
        self.reg_Image_Registered = QToolButton(self.tab_segment)
        self.reg_Image_Registered.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.reg_Image_Registered.setToolTip(self.tr('查看配准图像'))
        self.reg_Image_Registered.setText(self.tr('查看配准图像'))
        self.reg_Image_Registered.setIcon(QIcon('icon/bank.ico'))
        self.reg_Image_Registered.setAutoRaise(True)
        self.reg_Image_Registered.clicked.connect(self.show_registration_image)
        self.tab_registration.layout().addWidget(self.reg_Image_Registered)
        # 查看配准图像
        self.reg_Image_Compared = QToolButton(self.tab_segment)
        self.reg_Image_Compared.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.reg_Image_Compared.setToolTip(self.tr('查看对比图像'))
        self.reg_Image_Compared.setText(self.tr('查看对比图像'))
        self.reg_Image_Compared.setIcon(QIcon('icon/bank.ico'))
        self.reg_Image_Compared.setAutoRaise(True)
        self.reg_Image_Compared.clicked.connect(self.show_compare_image)
        self.tab_registration.layout().addWidget(self.reg_Image_Compared)
        # ------------------关键点检测---------------------------
        # 关键点检测
        self.key_landMark = QToolButton(self.tab_segment)
        self.key_landMark.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.key_landMark.setToolTip(self.tr('关键点检测'))
        self.key_landMark.setText(self.tr('关键点检测'))
        self.key_landMark.setIcon(QIcon('icon/bank.ico'))
        self.key_landMark.setAutoRaise(True)
        self.tab_keyPointCheck.layout().addWidget(self.key_landMark)
        # ------------------诊断---------------------------
        # 诊断
        self.diag_diagnoseis = QToolButton(self.tab_segment)
        self.diag_diagnoseis.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.diag_diagnoseis.setToolTip(self.tr('诊断'))
        self.diag_diagnoseis.setText(self.tr('诊断'))
        self.diag_diagnoseis.setIcon(QIcon('icon/bank.ico'))
        self.diag_diagnoseis.setAutoRaise(True)
        self.diag_diagnoseis.clicked.connect(self.classify)
        self.tab_diagnoise.layout().addWidget(self.diag_diagnoseis)

        self.initGRightTitel()

    def initGRightTitel(self):
        """title上的全局调整栏，和按钮在同一行，但是是右对齐"""
        self.gToolRightWidget = QWidget(self.tool)
        self.gToolRightWidget.setObjectName("gToolRightWidget")
        self.horizontalLayout_GToolR = QHBoxLayout(self.gToolRightWidget)
        self.horizontalLayout_GToolR.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_GToolR.setSpacing(3)
        self.horizontalLayout_GToolR.setObjectName("horizontalLayout_GToolR")
        self.horizontalLayout_GToolR.setAlignment(Qt.AlignRight)
        icon = QIcon()
        self.toolButton_vtkLayout = QToolButton(self.gToolRightWidget)
        icon.addPixmap(QPixmap("resources/vtkLayout.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_vtkLayout.setIcon(icon)
        self.toolButton_vtkLayout.setObjectName("toolButton_vtkLayout")
        self.toolButton_vtkLayout.setToolTip(self.tr("设置图像显示布局"))
        self.horizontalLayout_GToolR.addWidget(self.toolButton_vtkLayout)

        icon1 = QIcon()
        icon1.addPixmap(QPixmap("resources/windowWL.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_windowWL = QToolButton(self.gToolRightWidget)
        self.toolButton_windowWL.setIcon(icon1)
        self.toolButton_windowWL.setObjectName("toolButton_windowWL")
        self.toolButton_windowWL.setToolTip(self.tr("设置图像显示窗宽窗位"))
        self.toolButton_windowWL.clicked.connect(self.set_contrast)
        self.horizontalLayout_GToolR.addWidget(self.toolButton_windowWL)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("resources/modeColorMap.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_modeColorMap = QToolButton(self.gToolRightWidget)
        self.toolButton_modeColorMap.setIcon(icon2)
        self.toolButton_modeColorMap.setObjectName("toolButton_modeColorMap")
        self.toolButton_modeColorMap.setToolTip(self.tr("设置图像模型颜色"))
        self.toolButton_modeColorMap.clicked.connect(self.set_color_map)
        self.horizontalLayout_GToolR.addWidget(self.toolButton_modeColorMap)
        self.gToolRightWidget.setMaximumSize(90, 26)

        # 初试化vtk布局的菜单
        self.vtkLayoutMenu = QMenu(self.toolButton_vtkLayout)
        self.vtkLayoutMenu.setTearOffEnabled(False)
        self.vtkLayoutMenu.setLayoutDirection(Qt.LayoutDirection.LayoutDirectionAuto)
        self.vtkLayout1_action = QAction(QIcon("resources/vtk_layout1.png"), self.tr("布局一"))
        self.vtkLayout1_action.setObjectName('vtkLayout1_action')
        self.vtkLayout1_action.setProperty("layout", MainWindow.VTKLayout.DeaultLayout)
        self.vtkLayout1_action.triggered.connect(self.vtkLayoutManager)
        self.vtkLayoutMenu.addAction(self.vtkLayout1_action)

        self.vtkLayout2_action = QAction(QIcon("resources/vtk_layout2.png"), self.tr("布局二"))
        self.vtkLayout2_action.setObjectName('vtkLayout2_action')
        self.vtkLayout2_action.setProperty("layout", MainWindow.VTKLayout.PainLayout)
        self.vtkLayout2_action.triggered.connect(self.vtkLayoutManager)
        self.vtkLayoutMenu.addAction(self.vtkLayout2_action)

        self.vtkLayout3_action = QAction(QIcon("resources/vtk_layout3.png"), self.tr("布局三"))
        self.vtkLayout3_action.setObjectName('vtkLayout3_action')
        self.vtkLayout3_action.setProperty("layout", MainWindow.VTKLayout.No3DLayout)
        self.vtkLayout3_action.triggered.connect(self.vtkLayoutManager)
        self.vtkLayoutMenu.addAction(self.vtkLayout3_action)

        self.toolButton_vtkLayout.clicked.connect(
            lambda: self.vtkLayoutMenu.popup(
                self.toolButton_vtkLayout.mapToGlobal(self.toolButton_vtkLayout.rect().bottomLeft())))

    def vtkLayoutManager(self):
        # 这里是全局的视图布局控制
        senderLayout = self.sender().property("layout")
        widgetList = []
        if senderLayout == MainWindow.VTKLayout.DeaultLayout:
            widgetList.append(self.transverseWidget)
            widgetList.append(self.sagittalWidget)
            widgetList.append(self.coronalWidget)
            widgetList.append(self.restruct_3dWidget)
            self.restruct_3dWidget.setVisible(True)
            self.setVTKLayout(MainWindow.VTKLayout.DeaultLayout, widgetList)
            for widget in widgetList:
                widget.toolButton_vtkTrans.setVisible(True)

        if senderLayout == MainWindow.VTKLayout.PainLayout:
            widgetList.append(self.transverseWidget)
            widgetList.append(self.sagittalWidget)
            widgetList.append(self.coronalWidget)
            widgetList.append(self.restruct_3dWidget)
            self.restruct_3dWidget.setVisible(True)
            self.setVTKLayout(MainWindow.VTKLayout.PainLayout, widgetList)
            for widget in widgetList:
                widget.toolButton_vtkTrans.setVisible(False)

        if senderLayout == MainWindow.VTKLayout.No3DLayout:
            widgetList.append(self.transverseWidget)
            widgetList.append(self.sagittalWidget)
            widgetList.append(self.coronalWidget)
            self.restruct_3dWidget.setVisible(False)
            self.setVTKLayout(MainWindow.VTKLayout.No3DLayout, widgetList)
            for widget in widgetList:
                widget.toolButton_vtkTrans.setVisible(True)
        # 这里是vtk窗口内的控制
        pos = 0
        if self.sender() == self.transverseWidget.toolButton_vtkTrans:
            pos = MainWindow._vtkListInCurentWindow.index(self.transverseWidget)
        if self.sender() == self.sagittalWidget.toolButton_vtkTrans:
            pos = MainWindow._vtkListInCurentWindow.index(self.sagittalWidget)
        if self.sender() == self.coronalWidget.toolButton_vtkTrans:
            pos = MainWindow._vtkListInCurentWindow.index(self.coronalWidget)
        if self.sender() == self.restruct_3dWidget.toolButton_vtkTrans:
            pos = MainWindow._vtkListInCurentWindow.index(self.restruct_3dWidget)
        if self.sender().inherits('QToolButton'):
            MainWindow._vtkListInCurentWindow[0], MainWindow._vtkListInCurentWindow[pos] = \
                MainWindow._vtkListInCurentWindow[pos], MainWindow._vtkListInCurentWindow[0]
            self.setVTKLayout(MainWindow._layoutForVtkInCurentWindow, MainWindow._vtkListInCurentWindow)

    def resetApp(self):
        self.stackedWidget.setCurrentWidget(self.page_start)
        self.toolButton_ResetImage.setVisible(False)
        self.toolButton_ImportImage.setVisible(False)
        self.toolButton_ExportImage.setVisible(False)

    def slotLoadImage(self):
        if self.add_main_file():
            self.stackedWidget.setCurrentWidget(self.page_home)
            self.toolButton_ResetImage.setVisible(True)
            self.toolButton_ImportImage.setVisible(True)
            self.toolButton_ExportImage.setVisible(True)

    # 设置对齐方式
    def setAligmentForToolContent(self, layoutDirection):
        self.tab_segment.setLayoutDirection(layoutDirection)
        self.tab_registration.setLayoutDirection(layoutDirection)
        self.tab_diagnoise.setLayoutDirection(layoutDirection)

    def exitApp(self):
        reply2 = HQUMessageBox.question(self, self.tr("关闭程序"), self.tr("您确定关闭当前正在运行的程序吗？"))
        if reply2 == HQUMessageBox.YES:
            self.close()
            print("关闭成功")
        else:
            print("关闭取消")

    def windowSizeChanged(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(MainWindow, self).move(pos)

    def resizeEvent(self, event) -> None:
        # 设置gToolWidget位置
        gToolWidgetX = self.width() - self.gToolRightWidget.width() - 20
        self.gToolRightWidget.setGeometry(gToolWidgetX, 0, self.gToolRightWidget.width(),
                                          self.gToolRightWidget.height())

    def enterEvent(self, event):
        super(MainWindow, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(MainWindow, self).mouseDoubleClickEvent(event)
        if event.button() == Qt.LeftButton and event.pos().x() > self.Margins and self.titel.geometry().contains(
                self.titel.mapFrom(self.titel, event.pos())):
            self.windowSizeChanged()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton and event.pos().x() > self.Margins and self.titel.geometry().contains(
                self.titel.mapFrom(self.titel, event.pos())):
            self.headmPos = event.pos()
        if event.button() == Qt.LeftButton and self.Direction:
            self._mpos = event.pos()
            self._pressed = True
        event.ignore()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        self.headmPos = None
        self._pressed = False
        event.accept()

    def mouseMoveEvent(self, event):
        self.Direction = None

        if event.buttons() == Qt.LeftButton and self.headmPos:
            self.move(self.mapToGlobal(event.pos() - self.headmPos))

    def add_main_file(self):
        """
        添加主图像事件
        """
        # TODO 解决读取慢的问题

        main_file = QFileDialog.getOpenFileName(self, 'Load Image File', '',
                                                'All Files (*.*);;'
                                                'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz);;'
                                                'NRRD (*.nrrd *.nhdr);;'
                                                'DICOM (*.dcm);;'
                                                'Gipl (*.gipl *.gipl.gz);;'
                                                'Meta (*.mhd *.mha);;'
                                                'MRC (*.mrc *.rec);;'
                                                'MINC (*.mnc)'
                                                'vtk (*.vtk)'
                                                )[0]
        print(main_file)
        if not main_file:
            return False

        self.registration_init()
        status = HQUMessageBox.status(self, self.tr('文件导入'), self.tr('图像文件正在解析中，请稍后'))
        QApplication.processEvents()
        self.read_image_by_path(main_file)
        if MainWindow._layoutForVtkInCurentWindow != MainWindow.VTKLayout.No3DLayout:
            displayVtkList = []
            displayVtkList.append(self.transverseWidget)
            displayVtkList.append(self.sagittalWidget)
            displayVtkList.append(self.coronalWidget)
            self.setVTKLayout(MainWindow.VTKLayout.No3DLayout, displayVtkList)

        print('end add main file')
        status.close()
        return True

    def read_image_by_path(self, main_file):
        """
        读取图片
        :param main_file: 图片路径
        :return: 0正常，<0读取失败
        """
        if '' != main_file:
            # if ReadImage(main_file) != False:
            self.var_init()
            self.clear_3d()

            self.image_path = main_file
            self.filename = os.path.basename(main_file)
            # self.clean_layout()
            reader2d = ReadImage(main_file)
            if reader2d:
                self.vtk_pipeline_image2d(self.transverse, reader2d)
            else:
                temp_main_image = read_img(main_file)  # (x,y,z),(S,C,A)
                if temp_main_image is None:
                    msg_box = HQUMessageBox.warning(self, 'Warning', 'Failed to load image')
                    return -1
                self.main_image = temp_main_image
                temp = sitk.GetArrayFromImage(self.main_image)  # (z,y,x),(A,C,S)
                self.main_image_shape = temp.shape
                # 获取各方向切片的个数 初始化滚轴
                self.dims = temp.shape[::-1]  # (x,y,z),(S,C,A)
                # A
                # self.transverseWidget.getScrollBar().valueChanged.disconnect(self.change_axial)
                self.transverseWidget.getScrollBar().blockSignals(True)
                self.transverseWidget.getScrollBar().setMinimum(1)
                self.transverseWidget.getScrollBar().setMaximum(self.dims[2])
                self.transverseWidget.getScrollBar().setValue(self.dims[2] // 2)
                # self.transverseWidget.getScrollBar().valueChanged.connect(self.change_axial)
                self.transverseWidget.getScrollBar().blockSignals(False)
                # self.label_slice.setText(
                #     '{} of {}'.format(self.transverseWidget.getScrollBar().value(), self.transverseWidget.getScrollBar().maximum()))
                # S
                # self.sagittalWidget.getScrollBar().valueChanged.disconnect(self.change_sagi)

                self.sagittalWidget.getScrollBar().blockSignals(True)
                self.sagittalWidget.getScrollBar().setMinimum(1)
                self.sagittalWidget.getScrollBar().setMaximum(self.dims[0])
                self.sagittalWidget.getScrollBar().setValue(self.dims[0] // 2)
                self.sagittalWidget.getScrollBar().blockSignals(False)
                # self.sagittalWidget.getScrollBar().valueChanged.connect(self.change_sagi)
                # self.label_slice_2.setText(
                #     '{} of {}'.format(self.sagittalWidget.getScrollBar().value(), self.sagittalWidget.getScrollBar().maximum()))
                # C
                # self.coronalWidget.getScrollBar().valueChanged.disconnect(self.change_corn)
                self.coronalWidget.getScrollBar()
                self.coronalWidget.getScrollBar().blockSignals(True)
                self.coronalWidget.getScrollBar().setMinimum(1)
                self.coronalWidget.getScrollBar().setMaximum(self.dims[1])
                self.coronalWidget.getScrollBar().setValue(self.dims[1] // 2)
                self.coronalWidget.getScrollBar().blockSignals(False)
                # self.coronalWidget.getScrollBar().valueChanged.connect(self.change_corn)
                # self.label_slice_3.setText(
                #     '{} of {}'.format(self.coronalWidget.getScrollBar().value(), self.coronalWidget.getScrollBar().maximum()))

                spacing = self.main_image.GetSpacing()
                origin = self.main_image.GetOrigin()
                self.img_center = [origin[i] + spacing[i] * (self.dims[i] // 2 - 1) for i in range(3)]

                self.minimum = temp.min()
                self.maximum = temp.max()
                self.level = (self.minimum + self.maximum) // 2
                self.window = self.maximum - self.minimum
                self.image = temp
                # self.image = normalize(temp)

                self.vtk_pipeline_image(self.transverse, 0)
                self.vtk_pipeline_image(self.sagittal, 1)
                self.vtk_pipeline_image(self.coronal, 2)

                spacing = self.main_image.GetSpacing()
                self.lineEdit_4.setText("%.6f" % spacing[0])
                self.lineEdit_3.setText("%.6f" % spacing[1])
                self.lineEdit_2.setText("%.6f" % spacing[2])

                return 0
            # self.lb3.set_sibling_nodes(sibling)
        return -2

    def registration_helper(self, floating_image_path, fixed_image_path, parameter_map, output_path):
        """
        配准辅助函数

        :param floating_image_path: 浮动图路径
        :param fixed_image_path: 参考图路径
        :param parameter_map: 配准参数(rigid,affine)
        :param output_path: 输出路径
        """
        fixed_image = read_img(fixed_image_path)
        if fixed_image is None:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Failed to load image')
            return
        # self.main_image, self.final_transform = registration(self.main_image, fixed_image)
        # save_img(output_path, self.main_image)
        _, self.final_transform = registration_by_itk_elastix(sitk_image_to_itk_image(self.main_image),
                                                              sitk_image_to_itk_image(fixed_image),
                                                              parameter_map,
                                                              output_path)

        self.registration_init()
        self.floating_image_path = floating_image_path
        self.fixed_image_path = fixed_image_path
        self.registration_image_path = output_path
        self.reader_fixed = self.numpyTovtkimage(sitk.GetArrayFromImage(fixed_image))

        # self.show_registration_image()

    def registration_rigid(self):
        """
        刚性配准
        """
        # FIXME 摆烂写法，待优化
        fixed_image_path = QFileDialog.getOpenFileName(self, 'Open Reference File', '~',
                                                       'All Files (*.*);;'
                                                       'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz);;'
                                                       'NRRD (*.nrrd *.nhdr);;'
                                                       'DICOM (*.dcm);;'
                                                       'Gipl (*.gipl *.gipl.gz);;'
                                                       'Meta (*.mhd *.mha);;'
                                                       'MRC (*.mrc *.rec);;'
                                                       'MINC (*.mnc)'
                                                       'vtk (*.vtk)'
                                                       )[0]
        if '' != fixed_image_path:
            floating_image_path = self.image_path
            output_path = 'test.nii.gz'
            msg = HQUMessageBox.status(self, self.tr('提示'), self.tr('刚性配准中，请稍等...'),
                                       InThreadfunction=partial(self.registration_helper, floating_image_path,
                                                                        fixed_image_path, 'rigid', output_path))
            msg.exec_()
            self.show_registration_image()
        print('end registration_rigid')

    def registration_affine(self):
        """
        仿射变换配准
        """
        # FIXME 摆烂写法，待优化
        fixed_image_path = QFileDialog.getOpenFileName(self, 'Open Reference File', '~',
                                                       'All Files (*.*);;'
                                                       'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz);;'
                                                       'NRRD (*.nrrd *.nhdr);;'
                                                       'DICOM (*.dcm);;'
                                                       'Gipl (*.gipl *.gipl.gz);;'
                                                       'Meta (*.mhd *.mha);;'
                                                       'MRC (*.mrc *.rec);;'
                                                       'MINC (*.mnc)'
                                                       'vtk (*.vtk)'
                                                       )[0]
        if '' != fixed_image_path:
            floating_image_path = self.image_path
            output_path = 'test.nii.gz'
            msg = HQUMessageBox.status(self, self.tr('提示'), self.tr('反射配准中，请稍等...'),
                                       InThreadfunction=partial(self.registration_helper, floating_image_path,
                                                                fixed_image_path, 'affine', output_path))
            msg.exec_()
            self.show_registration_image()
            print('end registration_affine')

    def numpyTovtkimage(self, source_numpy, is_label=False):
        """
        numpy转vtkImageImport

        :param source_numpy: 图像(numpy)
        :param is_label: 是否为标签
        :return: vtkImageImport
        """
        num_labels = 0
        labels = []
        if is_label:
            img_f = np.unique(source_numpy)
            num_labels = len(img_f) - 1
            for i in range(num_labels):
                v = img_f[i + 1]
                source_numpy[source_numpy == v] = i + 1
                labels.append(i + 1)
        if is_label:
            spacing = self.label_main.GetSpacing()
            origin = self.label_main.GetOrigin()
            direction = self.label_main.GetDirection()
        else:
            spacing = self.main_image.GetSpacing()
            origin = self.main_image.GetOrigin()
            direction = self.main_image.GetDirection()
        importer = numpy2vtkImageImport(source_numpy, spacing, origin, direction, is_label)

        if is_label:
            return importer, num_labels, labels

        return importer

    # def vtk_pipeline(self, actors):
    #     """vtk成像的pipeline"""
    #     self.lb4.GetRenderWindow().AddRenderer(self.ren)
    #     self.iren = self.lb4.GetRenderWindow().GetInteractor()
    #     # TODO 修改大小
    #     # self.lb4.SetSize(500, 500)
    #     for a in actors:
    #         self.ren.AddActor(a)
    #     self.lb4.GetRenderWindow().Render()
    #     # self.iren.Start()
    #     print('end vtk pipeline finish')

    def vtk_pipeline_label(self, vtk_widget, ori):
        """先获取当前的render，在将maskactor加入其中"""
        # TODO 先加mask再加图像
        renwin = vtk_widget.GetRenderWindow()
        render = renwin.GetRenderers().GetFirstRenderer()
        renwin.RemoveRenderer(render)
        ren = vtkRenderer()

        imageactor = self.get_result(ori)
        maskactor = self.get_result(ori, False)
        line_ver, line_hor = cross_hair_actors(self.lines[ori][0], self.lines[ori][1], ori)
        ren.AddActor(maskactor)
        ren.AddActor(imageactor)
        ren.AddActor2D(self.textActors[ori])
        ren.AddActor(line_ver)
        ren.AddActor(line_hor)
        ren.SetBackground(0, 0, 0)
        renwin.AddRenderer(ren)
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.3)
        vtk_widget.GetRenderWindow().Render()

    def vtk_pipeline_image2d(self, vtk_widget, reader):
        actor = vtkImageActor()
        actor.GetMapper().SetInputConnection(reader.GetOutputPort())
        ren = vtkRenderer()
        ren.AddActor(actor)
        vtk_widget.GetRenderWindow().AddRenderer(ren)
        iren = vtk_widget.GetRenderWindow().GetInteractor()
        style = vtkInteractorStyleImage()
        iren.SetInteractorStyle(style)
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.3)
        iren.Initialize()

    def vtk_pipeline_image(self, vtk_widget, ori):
        renwin = vtk_widget.GetRenderWindow()
        renders = renwin.GetRenderers()
        renders.InitTraversal()
        for i in range(renders.GetNumberOfItems()):
            render = renders.GetNextItem()
            renwin.RemoveRenderer(render)

        ren = vtkRenderer()
        vtk_widget.GetRenderWindow().AddRenderer(ren)
        iren = vtk_widget.GetRenderWindow().GetInteractor()
        vtk_widget.SetSize(300, 300)

        imgactor = self.get_result(ori)
        self.image_actors[ori] = imgactor
        self.Origins[ori] = imgactor.GetInput().GetOrigin()
        textActor = vtkTextActor()
        if 0 == ori:
            textActor.SetInput('{} of {}'.format(self.transverseWidget.getScrollBar().value(),
                                                 self.transverseWidget.getScrollBar().maximum()))
            scrollbar = self.transverseWidget.getScrollBar()
        elif 1 == ori:
            textActor.SetInput('{} of {}'.format(self.sagittalWidget.getScrollBar().value(),
                                                 self.sagittalWidget.getScrollBar().maximum()))
            scrollbar = self.sagittalWidget.getScrollBar()
        elif 2 == ori:
            textActor.SetInput('{} of {}'.format(self.coronalWidget.getScrollBar().value(),
                                                 self.coronalWidget.getScrollBar().maximum()))
            scrollbar = self.coronalWidget.getScrollBar()
        textActor.SetPosition(290, 0)
        # # textActor.SetPosition(200, 0)
        textActor.GetTextProperty().SetFontSize(15)
        textActor.GetTextProperty().SetJustificationToRight()
        textActor.GetTextProperty().SetColor(vtkNamedColors().GetColor3d("lightgreen"))
        self.textActors[ori] = textActor
        ren.AddActor2D(textActor)

        ren.AddActor(imgactor)

        self.lines[ori][0], self.lines[ori][1] = add_cross_hair(imgactor, self.dims, ori)
        line_ver, line_hor = cross_hair_actors(self.lines[ori][0], self.lines[ori][1], ori)

        ren.AddActor(line_ver)
        ren.AddActor(line_hor)

        temp = vtkInteractorStyleImage()
        # temp.RemoveAllObservers()
        iren.SetInteractorStyle(temp)
        # 取消其他事件 TODO 取消指定事件
        iren.RemoveAllObservers()
        # iren.RemoveObservers(vtkCommand.KeyPressEvent)
        # iren.RemoveObservers(vtkCommand.EndPickEvent)
        # iren.RemoveObservers(vtkCommand.EndWindowLevelEvent)
        # iren.RemoveObservers(vtkCommand.InteractionEvent)
        # iren.RemoveObservers(vtkCommand.PickEvent)
        # iren.RemoveObservers(vtkCommand.ResetWindowLevelEvent)
        # iren.RemoveObservers(vtkCommand.StartPickEvent)
        # iren.RemoveObservers(vtkCommand.StartWindowLevelEvent)
        # iren.RemoveObservers(vtkCommand.WindowLevelEvent)
        iren.AddObserver(vtkCommand.LeftButtonPressEvent, self.left_button_press_callback)
        iren.AddObserver(vtkCommand.MouseMoveEvent, self.left_button_press_callback)
        iren.AddObserver(vtkCommand.LeftButtonReleaseEvent, self.left_button_press_callback)
        # 监听鼠标滚轮事件
        iren.AddObserver(vtkCommand.MouseWheelForwardEvent,
                         partial(self.change_scrollbar_value_down, scrollbar=scrollbar))
        iren.AddObserver(vtkCommand.MouseWheelBackwardEvent,
                         partial(self.change_scrollbar_value_up, scrollbar=scrollbar))

        ren.SetBackground(0, 0, 0)
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.3)
        iren.Initialize()

    def get_result(self, ori, is_image=True):
        if is_image:
            if self.reader1 is None:
                self.reader1 = self.numpyTovtkimage(self.image)
            slice = self.get_slice(self.reader1, ori, True, self.img_center)
        else:
            if self.reader2 is None:
                self.reader2, self.num_labels, self.num2labels = self.numpyTovtkimage(self.label, True)
            slice = self.get_slice(self.reader2, ori, False, self.img_center)
        if self.Origins[ori] != 0:
            slice.GetOutput().SetOrigin(self.Origins[ori])
            slice.Update()
        actor = vtkImageActor()
        actor.SetInputData(slice.GetOutput())
        return actor

    def get_lookuptable(self, is_image_slice=True):
        # TODO 或许应该更灵活
        if is_image_slice:
            lookuptable = vtkLookupTable()
            win_min = (2 * self.level - self.window) / 2.0 + 0.5
            win_max = (2 * self.level + self.window) / 2.0 + 0.5
            lookuptable.SetRange(win_min, win_max)  # Gets the range of scalars which will be mapped
            lookuptable.SetValueRange(0.0, 1.0)
            lookuptable.SetSaturationRange(0.0, 0.0)
            lookuptable.SetRampToLinear()
            lookuptable.Build()
            self.image_color_map = lookuptable
        else:
            lookuptable = vtkLookupTable()
            ids = LabelColor.label2r.keys()
            lookuptable.SetNumberOfTableValues(max(ids) + 1)
            lookuptable.SetRange(0.0, 1.0 * max(ids))
            lookuptable.SetTableValue(0, 0.0, 0.0, 0.0, 0.0)
            for k in ids:
                lookuptable.SetTableValue(k,
                                          LabelColor.label2r[k] / 255.0,
                                          LabelColor.label2g[k] / 255.0,
                                          LabelColor.label2b[k] / 255.0,
                                          0.4)
            lookuptable.Build()
            self.label_color_map = lookuptable
        return lookuptable

    def get_slice(self, reader, ori, is_image_slice=True, cur_center=None):
        """
        获取切片

        :param reader: vtk数据
        :param ori: 方向0:A(横断面z),1:S(矢状面x),2:C(冠状面y)
        :param is_image_slice: 图片True/标签False
        :param cur_center: 切片中心
        :return: 切片
        """

        if reader == None:
            print('vtk数据:reader为空')
            return
        flip = vtkImageFlip()
        flip.SetInputConnection(reader.GetOutputPort())
        flip.SetFilteredAxes(2)
        flip.Update()

        extent = flip.GetOutput().GetExtent()
        spacing = flip.GetOutput().GetSpacing()
        origin = flip.GetOutput().GetOrigin()

        if cur_center is None:
            center = [origin[i] + spacing[i] * 0.5 * (extent[2 * i] + extent[2 * i + 1]) for i in range(3)]
            # center = [0] * 3
            # center[0] = origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1])  # 矢状面（sagittal plane）S x
            # center[1] = origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3])  # 冠状面（coronal plane）C y
            # center[2] = origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])  # 横断面（transverse plane）A z
        else:
            center = cur_center

        # print('center',center)
        if 0 == ori:
            # 横断面（transverse plane）A z
            f1 = vtkImageFlip()
            f1.SetFilteredAxes(1)
            f1.SetInputConnection(flip.GetOutputPort())
            f1.Update()
            flip = f1

        reslice = resliceByOrient(flip, center, ori)
        lookuptable = self.image_color_map if is_image_slice else self.label_color_map
        if lookuptable is None:
            lookuptable = self.get_lookuptable(is_image_slice)
        colorMap = vtkImageMapToColors()
        colorMap.SetLookupTable(lookuptable)
        colorMap.SetInputConnection(reslice.GetOutputPort())
        colorMap.Update()
        return colorMap

    def get_Isosurface_helper(self):
        self.Isosurfaces, self.polydatas = get_Isosurface(self.reader2, self.num_labels, self.num2labels,
                                                          spacing=[1.0, 1.0, 1.0])

    def vtk_pipeline_modeling(self):
        # Isosurfaces, self.polydatas = get_Isosurface(self.reader2, self.num_labels, self.num2labels,
        #                                              spacing=[1.0, 1.0, 1.0])
        self.get_Isosurface_helper()
        # progress_bar_dialog = ProgressBar(parent=self, func=self.get_Isosurface_helper)
        # progress_bar_dialog.exec()

        renwin = self.restruct_3d.GetRenderWindow()
        renders = renwin.GetRenderers()
        renders.InitTraversal()
        for i in range(renders.GetNumberOfItems()):
            render = renders.GetNextItem()
            renwin.RemoveRenderer(render)

        self.ren_init()
        self.clicked = False
        renwin.AddRenderer(self.render_tobe)

        asem = vtkAssembly()
        # self.tableWidget_3d.setEnabled(True)
        for a in self.Isosurfaces:
            asem.AddPart(a)
            self.AddLine(a, self.filename, i)
        asem.SetPosition(0.0, 0.0, 0.0)
        x1, x2, y1, y2, z1, z2 = asem.GetBounds()
        scale_actor = max(100 / (x2 - x1), 100 / (y2 - y1), 100 / (z2 - z1))
        asem.SetScale(scale_actor, scale_actor, scale_actor)
        self.render_tobe.AddActor(asem)
        self.render_tobe.ResetCamera()
        self.Assembly.append(asem)
        renwin.Render()
        # iren.Start()
        print('end vtk pipeline finish')

    def AddLine(self, actor, name, part):
        self.tableWidget_3d.setEnabled(True)
        actor_color = tuple([int(i * 255) for i in actor.GetProperty().GetColor()])
        self.tableWidget_3d.setRowCount(self.num_models + 1)
        color_label = QLabel()
        color_label.setMinimumSize(15, 10)
        color_label.setStyleSheet("QLabel{background:rgb" + str(actor_color) + ";}")
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(color_label)
        h.setContentsMargins(0, 0, 0, 0)
        w = QWidget()
        w.setContentsMargins(0, 0, 0, 0)
        w.setLayout(h)
        first_table_widget = QTableWidgetItem(str(0))
        first_table_widget.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tableWidget_3d.setItem(self.num_models, 0, QTableWidgetItem(str(name) + ' ' + str(part)))
        self.tableWidget_3d.setCellWidget(self.num_models, 1,
                                          ImgWidget1(index=name, color=actor.GetProperty().GetColor()))
        self.tableWidget_3d.setCellWidget(self.num_models, 2, w)
        label = QLabel()
        # label.setStyleSheet("QLabel{background:rgb" + str(actor_color) + ";}")
        pic = QPixmap('resources/remove.png')
        # pic.scaled(5, 5)
        label.setAlignment(Qt.AlignCenter)
        label.setScaledContents(True)
        label.setPixmap(pic)
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(label)
        h.setContentsMargins(0, 0, 0, 0)
        w = QWidget()
        w.setContentsMargins(0, 0, 0, 0)
        w.setLayout(h)
        self.tableWidget_3d.setCellWidget(self.num_models, 3, w)
        self.num_models += 1

    def modeling(self):
        """
        三维重建
        """
        if not self.set_style:
            try:
                iren = self.restruct_3d.GetRenderWindow().GetInteractor()
                iren.SetInteractorStyle(vtkInteractorStyleJoystickActor())
            except:
                pass

        if self.label_origin is not None:
            self.clear_3d()
            begin = time.perf_counter()
            self.vtk_pipeline_modeling()
            cost_time = time.perf_counter() - begin
            print(cost_time)
            if not self.tableWidget_3d.isEnabled():
                self.tableWidget_3d.setEnabled(True)
            # msg_box = QMessageBox(QMessageBox.Information, 'Information', 'end of mesh')
            # msg_box.exec()
        else:
            print("no label")

    def save_model_file(self):
        """
        保存三维重建文件
        """
        polys = []
        actors = []
        for assembly in self.Assembly:
            parts = assembly.GetParts()
            parts.InitTraversal()
            for i in range(parts.GetNumberOfItems()):
                part = parts.GetNextProp3D()
                actors.append(part)
                polys.append(part.GetMapper().GetInput())
        if len(actors) == 0:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Please visualize annotation or load mesh first')
            return
        type_filter = {
            'VTP Files (*.vtp)': '.vtp',
            'STL Files (*.stl)': '.stl',
            'PLY Files (*.ply)': '.ply'
        }
        name, ext = QFileDialog.getSaveFileName(None, "Save Mesh",
                                                "",
                                                ';;'.join(type_filter.keys()))
        if '' == name:
            print('end save model file')
            return
        if '' == os.path.splitext(name)[-1]:
            name += type_filter[ext]
        res = save_actors(actors, polys, name, self.render_tobe)
        if res:
            msg_box = HQUMessageBox.information(self, 'Information', 'Successfully saved mesh')
            return
        else:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'The path cannot contain Chinese')
            return

    def seg_table_add_row(self, filename, remove_all=True):
        """
        标签表格中添加一行

        :param filename: 标签文件名
        """
        if remove_all:
            self.tableWidget_seg.setRowCount(0)
            self.tableWidget_seg.clearContents()

        row = self.tableWidget_seg.rowCount()
        self.tableWidget_seg.setRowCount(row + 1)
        self.tableWidget_seg.setItem(row, 0, QTableWidgetItem(os.path.basename(filename)))
        self.tableWidget_seg.setCellWidget(row, 1,
                                           ImgWidget1(index=None, color=None))

        label = QLabel()
        pic = QPixmap('resources/remove.png')
        pic.scaled(12, 12)
        label.setAlignment(Qt.AlignCenter)
        # label.setScaledContents(True)
        label.setPixmap(pic)
        self.tableWidget_seg.setCellWidget(row, 2, label)

    def add_segment_file(self):
        """
        添加分割文件事件
        """
        if self.main_image is None:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Please load image file first')
            return
        label_file = QFileDialog.getOpenFileName(self, 'Load Segmentation File', '~',
                                                 'All Files (*.*);;'
                                                 'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz);;'
                                                 'NRRD (*.nrrd *.nhdr);;'
                                                 'DICOM (*.dcm);;'
                                                 'Gipl (*.gipl *.gipl.gz);;'
                                                 'Meta (*.mhd *.mha);;'
                                                 'MRC (*.mrc *.rec);;'
                                                 'MINC (*.mnc)'
                                                 'vtk (*.vtk)'
                                                 )[0]
        status = HQUMessageBox.status(self, self.tr('导入分割文件'), self.tr('正在导入分割文件中，请稍后...'))
        QApplication.processEvents()
        if '' != label_file:
            print(label_file)
            self.label_main = read_img(label_file)
            QApplication.processEvents()
            self.label_origin = sitk.GetArrayFromImage(self.label_main)
            if self.label_origin.shape == self.main_image_shape:
                self.label = self.label_origin

                self.vtk_pipeline_label(self.transverse, 0)
                QApplication.processEvents()
                self.vtk_pipeline_label(self.sagittal, 1)
                QApplication.processEvents()
                self.vtk_pipeline_label(self.coronal, 2)
                QApplication.processEvents()

                self.seg_table_add_row(os.path.basename(label_file))
                QApplication.processEvents()

                print('end add segment file,and start 3d restruct ...')
                QApplication.processEvents()
                self.modeling()
                QApplication.processEvents()
                self.onClicked(0, 0)
                if MainWindow._layoutForVtkInCurentWindow != MainWindow.VTKLayout.DeaultLayout:
                    displayVtkList = []
                    displayVtkList.append(self.transverseWidget)
                    displayVtkList.append(self.sagittalWidget)
                    displayVtkList.append(self.coronalWidget)
                    displayVtkList.append(self.restruct_3dWidget)
                    self.setVTKLayout(MainWindow.VTKLayout.DeaultLayout, displayVtkList)
                print('end 3d restruct ...')

            else:
                HQUMessageBox.warning(self, 'Mismatched dimension',
                                      'Segmentation file must have the same dimension as image file')
        status.close()

    def save_main_file(self):
        """
        保存主图片事件
        """
        if self.main_image is None:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Please load image file first')
            return
        type_filter = {
            'All Files (*.*)': '.nii.gz',
            'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz)': '.nii.gz',
            'NRRD (*.nrrd *.nhdr)': '.nrrd',
            'Gipl (*.gipl *.gipl.gz)': '.gipl',
            'Meta (*.mhd *.mha)': '.mhd',
            'MRC (*.mrc *.rec)': '.mrc',
            'MINC (*.mnc)': '.mnc',
            'vtk (*.vtk)': '.vtk'
        }

        path, ext = QFileDialog.getSaveFileName(self, 'Save Image File', '~',
                                                ';;'.join(type_filter.keys())
                                                )
        if path == '':
            print('path empty')
            return
        if os.path.splitext(path)[-1] == '':
            path += type_filter[ext]
        print(path)
        if path.endswith('.dcm'):
            msg_box = HQUMessageBox.warning(self, 'Warning', 'DICOM is not supported')
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        save_img(path, self.main_image, self.main_image)
        # save_img(path, self.image, self.main_image)
        msg_box = HQUMessageBox.information(self, 'Information', 'Successfully saved image file')
        print('end save_main_file')

    def save_segment_file(self):
        """
        保存分割图片事件
        """
        if self.label_main is None:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Please load segmentation file first')
            return
        type_filter = {
            'All Files (*.*)': '.nii.gz',
            'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz)': '.nii.gz',
            'NRRD (*.nrrd *.nhdr)': '.nrrd',
            'Gipl (*.gipl *.gipl.gz)': '.gipl',
            'Meta (*.mhd *.mha)': '.mhd',
            'MRC (*.mrc *.rec)': '.mrc',
            'MINC (*.mnc)': '.mnc',
            'vtk (*.vtk)': '.vtk'
        }

        path, ext = QFileDialog.getSaveFileName(self, 'Save Segmentation File', '~',
                                                ';;'.join(type_filter.keys())
                                                )
        if path == '':
            print('path empty')
            return
        if os.path.splitext(path)[-1] == '':
            path += type_filter[ext]
        print(path)
        if path.endswith('.dcm'):
            msg_box = HQUMessageBox.warning(self, 'Warning', 'DICOM is not supported')
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        save_img(path, self.label_main, self.label_main)
        # save_img(path, self.label, self.label_main)
        msg_box = HQUMessageBox.information(self, 'Information', 'Successfully saved segmentation file')
        # print('end save_segment_file')

    def center(self):
        """
        界面居中显示
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def left_button_press_callback(self, caller, ev):
        if ev == 'LeftButtonPressEvent':
            self.left_button_press_flag = True
            self.change_cross_hair_and_view(caller, ev)
        elif ev == 'LeftButtonReleaseEvent':
            self.left_button_press_flag = False
        elif ev == 'MouseMoveEvent' and self.left_button_press_flag is True:
            self.change_cross_hair_and_view(caller, ev)

    def change_cross_hair_and_view(self, caller, ev):
        renwin = caller.GetRenderWindow()
        actors = renwin.GetRenderers().GetFirstRenderer().GetActors()
        actors.InitTraversal()
        lines = []
        for i in range(actors.GetNumberOfItems()):
            actor = actors.GetNextItem()
            if actor.GetMapper().GetInput().GetClassName() == 'vtkPolyData':
                ori = get_ori(actor.GetProperty().GetColor())
                lines.append(actor.GetMapper().GetInput())

        origin = self.image_actors[ori].GetInput().GetOrigin()
        spacing = self.image_actors[ori].GetInput().GetSpacing()
        dims = self.dims

        picker = vtkCellPicker()
        picker.SetTolerance(0.0001)
        p = caller.GetEventPosition()
        picker.Pick(p[0], p[1], 0, caller.GetRenderWindow().GetRenderers().GetFirstRenderer())
        pos = picker.GetPickPosition()
        x, y = pos[0] - origin[0], pos[1] - origin[1]
        set_Line(x, y, self.lines, ori, dims, spacing, origin)
        renwin.Render()
        self.reset_view(x, y, ori, dims, spacing)

    def change_scrollbar_value_up(self, caller, ev, scrollbar):
        """
        scrollbar值增加
        """
        if scrollbar.value() < scrollbar.maximum():
            scrollbar.setValue(scrollbar.value() + 1)

    def change_scrollbar_value_down(self, caller, ev, scrollbar):
        """
        scrollbar值减少
        """
        if scrollbar.value() > scrollbar.minimum():
            scrollbar.setValue(scrollbar.value() - 1)

    def reset_view(self, x, y, ori, dims, spacing):
        origin = self.main_image.GetOrigin()
        if 0 == ori:
            new_center = self.img_center
            y = spacing[1] * dims[1] - y
            new_center[1] = y + origin[1]
            new_center[0] = x + origin[0]
            self.img_center = new_center

            self.sagittalWidget.getScrollBar().setValue(x / spacing[0])  # S(x)
            self.scroll_bar_value_change(1)
            self.coronalWidget.getScrollBar().setValue(y / spacing[1])  # C(y)
            self.scroll_bar_value_change(2)

            renwin1 = self.sagittal.GetRenderWindow()
            self.slice_change_helper(renwin1, 1)
            renwin2 = self.coronal.GetRenderWindow()
            self.slice_change_helper(renwin2, 2)
        elif 1 == ori:
            new_center = self.img_center
            new_center[2] = dims[2] * spacing[1] - y + origin[2]
            new_center[1] = x + origin[1]
            self.img_center = new_center

            self.coronalWidget.getScrollBar().setValue(x / spacing[0])  # C(y)
            self.scroll_bar_value_change(2)
            self.transverseWidget.getScrollBar().setValue((dims[2] * spacing[1] - y) / spacing[1])  # A(z)
            self.scroll_bar_value_change(0)

            renwin0 = self.transverse.GetRenderWindow()
            self.slice_change_helper(renwin0, 0)
            renwin2 = self.coronal.GetRenderWindow()
            self.slice_change_helper(renwin2, 2)
        else:
            new_center = self.img_center
            new_center[2] = dims[2] * spacing[1] - y + origin[2]
            new_center[0] = x + origin[0]
            self.img_center = new_center

            self.sagittalWidget.getScrollBar().setValue(x / spacing[0])  # S(x)
            self.scroll_bar_value_change(1)
            self.transverseWidget.getScrollBar().setValue((dims[2] * spacing[1] - y) / spacing[1])  # A(z)
            self.scroll_bar_value_change(0)

            renwin0 = self.transverse.GetRenderWindow()
            self.slice_change_helper(renwin0, 0)
            renwin2 = self.sagittal.GetRenderWindow()
            self.slice_change_helper(renwin2, 1)

    def rib_seg_pipeline(self, do_mirror=False, mixed_precision=True):
        """
        分割肋骨

        :param do_mirror: 镜像
        :param mixed_precision: 混合精度
        """
        if os.path.exists(self.image_path):
            label_file = os.path.join(base_dir, 'predict_label/rib', os.path.basename(self.image_path))
            # seg_rib(self.image_path, do_mirror, mixed_precision, save_path=label_file)
            begin = time.perf_counter()

            msg = HQUMessageBox.status(self, self.tr('提示'), self.tr('分割进行中，请稍等...'),
                                       InThreadfunction=partial(seg_rib, self.image_path, do_mirror,
                                                                mixed_precision, label_file))
            msg.exec_()
            cost_time = time.perf_counter() - begin
            print(cost_time)
            if '' != label_file:
                print(label_file)
                self.label_main = read_img(label_file)
                if self.label_main is None:
                    msg_box = HQUMessageBox.warning(self, self.tr('警告'), self.tr('图像分割失败！'))
                    return
                self.label_origin = sitk.GetArrayFromImage(self.label_main)
                self.label = self.label_origin

                self.vtk_pipeline_label(self.transverse, 0)
                self.vtk_pipeline_label(self.sagittal, 1)
                self.vtk_pipeline_label(self.coronal, 2)

                self.seg_table_add_row('rib.nii.gz')
                HQUMessageBox.information(self,self.tr('分割成功'),self.tr('产生的新的分割文件位于\n%s')%(label_file))
        else:
            HQUMessageBox.error(self,self.tr('分割结果'),self.tr('分割失败,请校对算法参数'))

            return
        print('end add segment file')

    def pelvic_seg_pipeline(self, do_cut=False):
        """
        用hdc-net分割盆骨

        :param do_cut: 切割脊柱
        """
        if os.path.exists(self.image_path):
            label_file = os.path.join(base_dir, 'predict_label/pelvic', os.path.basename(self.image_path))
            # pelvic_segment(self.image_path, do_cut=do_cut, save_path=label_file)
            begin = time.perf_counter()
            msg = HQUMessageBox.status(self, self.tr('提示'), self.tr('分割进行中，请稍等...'),
                                       InThreadfunction=partial(pelvic_segment, self.image_path,
                                                                        do_cut, label_file))
            msg.exec_()
            cost_time = time.perf_counter() - begin
            print(cost_time)

            if '' != label_file:
                print(label_file)
                self.label_main = read_img(label_file)
                if self.label_main is None:
                    msg_box = HQUMessageBox.warning(self, 'Warning', 'Segmentation failed')

                    return
                self.label_origin = sitk.GetArrayFromImage(self.label_main)
                self.label = self.label_origin

                self.vtk_pipeline_label(self.transverse, 0)
                self.vtk_pipeline_label(self.sagittal, 1)
                self.vtk_pipeline_label(self.coronal, 2)

                self.seg_table_add_row('pelvic.nii.gz')
        else:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Please load image file first')

            return

        print('end add segment file')

    def pelvic_cs_net_seg_pipeline(self, do_cut=False):
        """
        用csnet分割盆骨

        :param do_cut: 切除脊柱
        """
        if os.path.exists(self.image_path):
            label_file = os.path.join(base_dir, 'predict_label/pelvic_CS_Net', os.path.basename(self.image_path))
            # pelvic_segment_cs_net(self.image_path, do_cut=do_cut, save_path=label_file)
            begin = time.perf_counter()
            msg = HQUMessageBox.status(self, self.tr('提示'), self.tr('分割进行中，请稍等...'),
                                       InThreadfunction=partial(pelvic_segment_cs_net, self.image_path,
                                                                        do_cut, label_file))
            msg.exec_()

            cost_time = time.perf_counter() - begin
            print(cost_time)
            if '' != label_file:
                print(label_file)
                self.label_main = read_img(label_file)
                if self.label_main is None:
                    msg_box = HQUMessageBox.warning(self, 'Warning', 'Segmentation failed')

                    return
                self.label_origin = sitk.GetArrayFromImage(self.label_main)
                self.label = self.label_origin

                self.vtk_pipeline_label(self.transverse, 0)
                self.vtk_pipeline_label(self.sagittal, 1)
                self.vtk_pipeline_label(self.coronal, 2)

                self.seg_table_add_row('pelvic.nii.gz')
        else:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Please load image file first')

            return

        print('end add segment file')

    def Choose_Directory(self):
        """
        添加三维重建文件
        """
        if not self.set_style:
            try:
                iren = self.restruct_3d.GetRenderWindow().GetInteractor()
                iren.SetInteractorStyle(vtkInteractorStyleJoystickActor())
            except:
                pass

        filenames, type = QFileDialog.getOpenFileNames(self,
                                                       "多文件选择",
                                                       "./",
                                                       "vtp Files (*.vtp);;"
                                                       "ply Files (*.ply);;"
                                                       "obj Files (*.obj);;"
                                                       "stl Files(*.stl);;"
                                                       "vtk Files (*.vtk);;")
        for file in filenames:
            if is_contain_chinese(file):
                msg_box = HQUMessageBox.warning(self, 'Warning', 'The path cannot contain Chinese')

                return
        if not filenames:
            pass
        else:
            files = filenames

            if files:
                assembly = vtkAssembly()
                renwin = self.restruct_3d.GetRenderWindow()
                for i, file in enumerate(files):
                    polydata = ReadPolyData(file)
                    if not polydata:
                        msg_box = HQUMessageBox.warning(self, 'Warning', 'Failed to load mesh')

                        return -1

                    randomColor = []
                    randomColor.append(np.random.randint(100, 255) / 255)
                    randomColor.append(np.random.randint(100, 255) / 255)
                    randomColor.append(np.random.randint(100, 255) / 255)

                    lut = self.make_colors(2, randomColor)
                    mapper = vtkPolyDataMapper()
                    mapper.SetInputData(polydata)
                    mapper.SetLookupTable(lut)
                    mapper.SetScalarRange(0, lut.GetNumberOfColors())
                    actor = vtkActor()

                    actor.GetProperty().SetDiffuseColor(randomColor)

                    actor.SetMapper(mapper)
                    assembly.AddPart(actor)
                    self.AddLine(actor, os.path.basename(file), i)
                x1, x2, y1, y2, z1, z2 = assembly.GetBounds()
                scale_actor = max(100 / (x2 - x1), 100 / (y2 - y1), 100 / (z2 - z1))
                assembly.SetScale(scale_actor, scale_actor, scale_actor)
                x1, x2, y1, y2, z1, z2 = assembly.GetBounds()
                print(int((x2 - x1) * (y2 - y1) * (z2 - z1)))
                assembly.SetPosition(0.0, 0.0, 0.0)
                self.Assembly.append(assembly)
                self.render_tobe.AddViewProp(assembly)
                colors = vtkNamedColors()
                # self.render_tobe.SetBackground(colors.GetColor3d("lightblue"))
                self.render_tobe.ResetCamera()
                renwin.AddRenderer(self.render_tobe)
                renwin.Render()

    def change_display_style(self):

        indexes = self.tableWidget_3d.selectionModel().selectedRows()
        for index in sorted(indexes):
            print('Row %d is selected' % index.row())

        iren = self.restruct_3d.GetRenderWindow().GetInteractor()
        if isinstance(iren.GetInteractorStyle(), vtkInteractorStyleJoystickCamera):
            style = vtkInteractorStyleJoystickActor()
            self.toolButton_3d.setIcon(QIcon('resources/brush_shape_square.png'))
        else:
            style = vtkInteractorStyleJoystickCamera()
            self.toolButton_3d.setIcon(QIcon('resources/combo_all_labels.png'))
        iren.SetInteractorStyle(style)

    def reset_3d(self):
        renwin = self.restruct_3d.GetRenderWindow()
        renders = renwin.GetRenderers()
        renders.InitTraversal()
        for i in range(renders.GetNumberOfItems()):
            render = renders.GetNextItem()
            renwin.RemoveRenderer(render)
        self.render_tobe = vtkRenderer()
        new_Assembly = []
        for ass in self.Assembly:
            Asem = vtkAssembly()
            parts = ass.GetParts()
            parts.InitTraversal()
            for i in range(parts.GetNumberOfItems()):
                part = parts.GetNextProp3D()
                Asem.AddPart(part)
                # for actor in ass:
                #     Asem.AddPart(actor)

            Asem.SetPosition(0.0, 0.0, 0.0)
            x1, x2, y1, y2, z1, z2 = Asem.GetBounds()
            scale_actor = max(100 / (x2 - x1), 100 / (y2 - y1), 100 / (z2 - z1))
            Asem.SetScale(scale_actor, scale_actor, scale_actor)
            self.render_tobe.AddActor(Asem)
            # self.render_tobe.ResetCamera()
            new_Assembly.append(Asem)
        self.render_tobe.ResetCamera()
        renwin.AddRenderer(self.render_tobe)
        renwin.Render()
        del self.Assembly
        self.Assembly = new_Assembly

    def horizontalSlider_change(self):
        try:
            it, it2 = self.selected
            cell = self.tableWidget_3d.cellWidget(it, 1)
            ren = self.render_tobe
            color = cell.color
            actors = ren.GetActors()
            actors.InitTraversal()
            actor_selected = None
            for i in range(actors.GetNumberOfItems()):
                actor = actors.GetNextItem()

                if actor.GetProperty().GetColor() == color:
                    actor_selected = actor
                    break
            if actor_selected is not None:
                print("pos:", self.restruct_3dWidget.horizontalSlider.sliderPosition())
                print('vaule:', self.restruct_3dWidget.horizontalSlider.value())
                value = float(self.restruct_3dWidget.horizontalSlider.sliderPosition()) / 10

                actor_selected.GetProperty().SetOpacity(
                    float(self.restruct_3dWidget.horizontalSlider.sliderPosition()) / 10)
                print(actor_selected.GetProperty().GetOpacity())
                print(value)
                self.restruct_3d.GetRenderWindow().Render()
        except:
            pass

    def classify(self):
        """
        热力图
        """
        dir_path = QFileDialog.getExistingDirectory(None, "选择文件夹", os.getcwd())
        if '' == dir_path:
            return
        heat_maps, row_images, patient_class = load_and_process_image(dir_path)
        if heat_maps is not None:
            self.classifyWindow = ClassifyWindow(row_images, heat_maps, patient_class)
            self.classifyWindow.show()
        else:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'No candidate image found')

            return -1

    def make_colors(self, n, color):
        lut = vtkLookupTable()
        lut.SetNumberOfColors(n)
        lut.SetTableRange(0, n - 1)
        lut.SetScaleToLinear()
        lut.Build()
        lut.SetTableValue(0, 0, 0, 0, 1)

        color = [1] + color + [1]
        lut.SetTableValue(*color)
        # lut.SetTableValue(2, 0, 1, 0, 1)
        # lut.SetTableValue(3, 1, 0, 0, 1)
        return lut

    def directory_dice(self):
        """
        计算两个目录的dice
        """
        pred_dir = QFileDialog.getExistingDirectory(self, "Open Predict Directory", '.')
        if '' == pred_dir:
            return
        target_dir = QFileDialog.getExistingDirectory(self, "Open Target Directory", '.')
        if '' == target_dir:
            return
        progress_bar_dialog = ProgressBarWithText(parent=self,
                                                  func=partial(directory_dice, pred_dir, target_dir, 3, 'result.xlsx'))
        progress_bar_dialog.exec()

    def update_image_spacing(self):
        spacing = [self.lineEdit_4.text(), self.lineEdit_3.text(), self.lineEdit_2.text()]
        try:
            new_spacing = [float(i) for i in spacing]
        except:
            print("非法字符")
        ori_spacing = self.main_image.GetSpacing()
        ori_size = self.main_image.GetSize()
        new_size = [int(round(ori_size[0] * (ori_spacing[0] / new_spacing[0]))),
                    int(round(ori_size[1] * (ori_spacing[1] / new_spacing[1]))),
                    int(round(ori_size[2] * (ori_spacing[2] / new_spacing[2])))]
        target_origin = self.main_image.GetOrigin()  # 目标的起点 [x,y,z]
        target_direction = self.main_image.GetDirection()
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(self.main_image)
        resampler.SetSize(new_size)  # 目标图像大小
        resampler.SetOutputOrigin(target_origin)
        resampler.SetOutputDirection(target_direction)
        resampler.SetOutputSpacing(new_spacing)
        print(sitk.GetArrayFromImage(self.main_image).dtype)
        dtype = sitk.GetArrayFromImage(self.main_image).dtype
        if dtype == np.int16:
            resampler.SetOutputPixelType(sitk.sitkInt16)
        elif dtype == np.uint8:
            resampler.SetOutputPixelType(sitk.sitkUInt8)
        elif dtype == np.float32:
            resampler.SetOutputPixelType(sitk.sitkFloat32)
        else:
            resampler.SetOutputPixelType(sitk.sitkInt32)
        resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))
        resampler.SetInterpolator(sitk.sitkLinear)
        itk_img_resampled = resampler.Execute(self.main_image)

        self.main_image = itk_img_resampled
        temp = sitk.GetArrayFromImage(self.main_image)  # (z,y,x),(A,C,S)
        self.main_image_shape = temp.shape
        # 获取各方向切片的个数 初始化滚轴
        self.dims = temp.shape[::-1]  # (x,y,z),(S,C,A)
        self.transverseWidget.getScrollBar().blockSignals(True)
        self.transverseWidget.getScrollBar().setMinimum(1)
        self.transverseWidget.getScrollBar().setMaximum(self.dims[2])
        self.transverseWidget.getScrollBar().setValue(self.dims[2] // 2)
        self.transverseWidget.getScrollBar().blockSignals(False)
        self.sagittalWidget.getScrollBar().blockSignals(True)
        self.sagittalWidget.getScrollBar().setMinimum(1)
        self.sagittalWidget.getScrollBar().setMaximum(self.dims[0])
        self.sagittalWidget.getScrollBar().setValue(self.dims[0] // 2)
        self.sagittalWidget.getScrollBar().blockSignals(False)
        self.coronalWidget.getScrollBar().blockSignals(True)
        self.coronalWidget.getScrollBar().setMinimum(1)
        self.coronalWidget.getScrollBar().setMaximum(self.dims[1])
        self.coronalWidget.getScrollBar().setValue(self.dims[1] // 2)
        self.coronalWidget.getScrollBar().blockSignals(False)

        spacing = self.main_image.GetSpacing()
        origin = self.main_image.GetOrigin()
        self.img_center = [origin[i] + spacing[i] * (self.dims[i] // 2 - 1) for i in range(3)]

        self.minimum = temp.min()
        self.maximum = temp.max()
        self.level = (self.minimum + self.maximum) // 2
        self.window = self.maximum - self.minimum
        self.image = temp
        self.reader1 = None
        # self.image = normalize(temp)

        self.vtk_pipeline_image(self.transverse, 0)
        self.vtk_pipeline_image(self.sagittal, 1)
        self.vtk_pipeline_image(self.coronal, 2)

        spacing = self.main_image.GetSpacing()
        self.lineEdit_4.setText("%.6f" % spacing[0])
        self.lineEdit_3.setText("%.6f" % spacing[1])
        self.lineEdit_2.setText("%.6f" % spacing[2])

        return 0

    def update_label_spacing(self):
        spacing = [self.lineEdit_4.text(), self.lineEdit_3.text(), self.lineEdit_2.text()]
        try:
            new_spacing = [float(i) for i in spacing]
        except:
            print("非法字符")
        ori_spacing = self.label_main.GetSpacing()
        ori_size = self.label_main.GetSize()
        new_size = [int(round(ori_size[0] * (ori_spacing[0] / new_spacing[0]))),
                    int(round(ori_size[1] * (ori_spacing[1] / new_spacing[1]))),
                    int(round(ori_size[2] * (ori_spacing[2] / new_spacing[2])))]
        target_origin = self.label_main.GetOrigin()  # 目标的起点 [x,y,z]
        target_direction = self.label_main.GetDirection()
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(self.label_main)
        resampler.SetSize(new_size)  # 目标图像大小
        resampler.SetOutputOrigin(target_origin)
        resampler.SetOutputDirection(target_direction)
        resampler.SetOutputSpacing(new_spacing)
        print(sitk.GetArrayFromImage(self.label_main).dtype)
        dtype = sitk.GetArrayFromImage(self.label_main).dtype
        if dtype == np.int16:
            resampler.SetOutputPixelType(sitk.sitkInt16)
        elif dtype == np.uint8:
            resampler.SetOutputPixelType(sitk.sitkUInt8)
        elif dtype == np.float32:
            resampler.SetOutputPixelType(sitk.sitkFloat32)
        else:
            resampler.SetOutputPixelType(sitk.sitkInt32)
        resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
        self.label_main = resampler.Execute(self.label_main)

        self.label_origin = sitk.GetArrayFromImage(self.label_main)
        if self.label_origin.shape == self.main_image_shape:
            self.label = self.label_origin

            self.vtk_pipeline_label(self.transverse, 0)
            self.vtk_pipeline_label(self.sagittal, 1)
            self.vtk_pipeline_label(self.coronal, 2)

    def update_spacing(self):
        self.update_image_spacing()
        if self.label_main:
            self.update_label_spacing()

    def reset_spacing(self):
        try:
            spacing = self.main_image.GetSpacing()
            self.lineEdit_4.setText("%.6f" % spacing[0])
            self.lineEdit_3.setText("%.6f" % spacing[1])
            self.lineEdit_2.setText("%.6f" % spacing[2])
        except:
            pass

    def directory_dice(self):
        """
        计算两个目录的dice
        """
        pred_dir = QFileDialog.getExistingDirectory(self, "Open Predict Directory", '.')
        if '' == pred_dir:
            return
        target_dir = QFileDialog.getExistingDirectory(self, "Open Target Directory", '.')
        if '' == target_dir:
            return
        progress_bar_dialog = ProgressBarWithText(parent=self,
                                                  func=partial(directory_dice, pred_dir, target_dir, 3, 'result.xlsx'))
        progress_bar_dialog.exec()

    def rib_batch_segmentation(self):
        """
        批量分割
        """
        root, save_path, result_path = '', '', ''
        path = QFileDialog.getOpenFileName(self, 'Open Excel', '~', 'excel (*.xlsx *.xls);;csv (*.csv)')[0]
        if '' == path:
            return
        # root = QFileDialog.getExistingDirectory(self, "Open Root Directory", '.')
        if '' == root:
            root = os.path.dirname(path)
            # return
        # save_path = QFileDialog.getExistingDirectory(self, 'Open Data Save Directory', '.')
        if '' == save_path:
            save_path = os.path.join(root, 'predict_rib')
            # return
        # result_path = QFileDialog.getSaveFileName(self, 'Save Result Excel', '.',
        #                                           'excel (*.xlsx *.xls);;csv (*.csv)')[0]
        if '' == result_path:
            result_path = os.path.join(root, 'rib_result.xlsx')
            # return
        progress_bar_dialog = ProgressBarWithText(parent=self,
                                                  func=partial(batch_segmentation, path, root, seg_rib, save_path,
                                                               result_path, 1))
        progress_bar_dialog.exec()

    def my_batch_segmentation(self):
        """
        批量分割
        """
        root, save_path, result_path = '', '', ''
        path = QFileDialog.getOpenFileName(self, 'Open Excel', '~', 'excel (*.xlsx *.xls);;csv (*.csv)')[0]
        if '' == path:
            return
        # root = QFileDialog.getExistingDirectory(self, "Open Root Directory", '.')
        if '' == root:
            root = os.path.dirname(path)
            # return
        # save_path = QFileDialog.getExistingDirectory(self, 'Open Data Save Directory', '.')
        if '' == save_path:
            save_path = os.path.join(root, 'predict_pelvic')
            # return
        # result_path = QFileDialog.getSaveFileName(self, 'Save Result Excel', '.',
        #                                           'excel (*.xlsx *.xls);;csv (*.csv)')[0]
        if '' == result_path:
            result_path = os.path.join(root, 'pelvic_result.xlsx')
            # return
        progress_bar_dialog = ProgressBarWithText(parent=self,
                                                  func=partial(batch_segmentation, path, root, pelvic_segment,
                                                               save_path,
                                                               result_path, 3))
        progress_bar_dialog.exec()

    def operative_helper(self, video_path, result_path, callback=None):
        """
        分割手术器械视频辅助函数

        :param video_path: 视频路径
        :param result_path: 结果路径
        :param callback: 回调，callback(int),返回处理百分比
        """
        try:
            if self.operative_model is None:
                self.operative_model = operative_load_model()
            print('end of loading model')
            os.makedirs(os.path.join(result_path, 'seg_mask'), exist_ok=True)
            os.makedirs(os.path.join(result_path, 'seg'), exist_ok=True)
            cap = cv2.VideoCapture(video_path)
            idx = 0
            total_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                t1 = time.time()
                seg_mask, origin_seg, seg = deal_single_image(self.operative_model, frame)
                cv2.imwrite(os.path.join(result_path, 'seg_mask', '{}.png'.format(str(idx).zfill(4))), seg_mask)
                cv2.imwrite(os.path.join(result_path, 'seg', '{}.png'.format(str(idx).zfill(4))), seg)
                t2 = time.time() - t1
                print(f'{idx} cost:{t2} s')
                idx += 1
                if idx < total_len and callback is not None:
                    callback(100. * idx // total_len)

            cap.release()
            cv2.destroyAllWindows()
        except:
            pass
        finally:
            if callback is not None:
                callback(100)

    def load_video(self):
        """
        分割手术器械视频
        """
        video_path = QFileDialog.getOpenFileName(self, 'Load video', '~', 'All Files (*.*)')[0]
        if '' != video_path:
            result_path = os.path.join(base_dir, 'result', 'image',
                                       time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
            begin = time.perf_counter()
            progress_bar_dialog = ProgressBarWithText(parent=self,
                                                      func=partial(self.operative_helper, video_path,
                                                                   result_path))
            progress_bar_dialog.exec()
            cost_time = time.perf_counter() - begin
            print(cost_time)
            self.video_window = playimg2(parent=None, data_path=os.path.join(result_path, 'seg'))
            self.video_window.show()
        print('end of load_video')

    def seg_table_clicked(self, r, w):
        """
        标签表格点击事件

        :param r: 行
        :param w: 列
        """
        if 1 == w:
            cell = self.tableWidget_seg.cellWidget(r, w)
            if cell is None:
                return
            cell.setPix()
            self.hide_show_label()
        elif 2 == w:
            self.label_main = None  # 标签，为None时不能建模
            self.image = None  # 主图像numpy
            self.label = None  # 标签numpy
            self.label_origin = None  # 标签numpy（原始的）

            # self.num_labels = None  # 标签个数
            # self.num2labels = None  # 每个标签对应的数值

            self.reader2 = None  # 标签转成vtkImageImporter
            self.label_color_map = None  # 标签颜色映射

            self.tableWidget_seg.setRowCount(0)
            self.tableWidget_seg.clearContents()
            # 刷新3个面
            self.change_axial()
            self.change_sagi()
            self.change_corn()

    def onClicked(self, it, it2):
        """
        三维重建表格点击

        :param it: 行
        :param it2: 列
        """
        self.restruct_3dWidget.horizontalSlider.setEnabled(True)
        self.selected = [it, it2]

        cell = self.tableWidget_3d.cellWidget(it, 1)
        actor_selected = None
        color = cell.color
        assembly = None
        for ass in self.Assembly:
            parts = ass.GetParts()
            parts.InitTraversal()
            for i in range(parts.GetNumberOfItems()):
                actor = parts.GetNextProp3D()
                if actor.GetProperty().GetColor() == color:
                    actor_selected = actor
                    assembly = ass
                    break
            if assembly is not None:
                break
        # actors = ren.GetActors()
        # actors.InitTraversal()

        # for i in range(actors.GetNumberOfItems()):
        #     actor = actors.GetNextItem()
        #     if actor.GetProperty().GetColor() == color:
        #         actor_selected = actor
        #     ren.RemoveActor(actor)

        if actor_selected is not None:
            if it2 == 1:
                cell.setPix()
                if not cell.open:
                    actor_selected.VisibilityOff()
                else:
                    actor_selected.VisibilityOn()
                self.restruct_3dWidget.horizontalSlider.setValue(round(actor_selected.GetProperty().GetOpacity() * 10))
                renwin = self.restruct_3d.GetRenderWindow()
                renwin.Render()
            elif it2 == 3:
                if assembly is not None:
                    assembly.RemovePart(actor_selected)
                    renwin = self.restruct_3d.GetRenderWindow()
                    renwin.Render()
                    self.tableWidget_3d.removeRow(it)
                    self.num_models -= 1
                    self.tableWidget_3d.setRowCount(self.num_models)
                    if self.tableWidget_3d.rowCount() == 0:
                        self.tableWidget_3d.setDisabled(True)
                    if assembly.GetParts().GetNumberOfItems() == 0:
                        self.Assembly.remove(assembly)
            else:
                self.restruct_3dWidget.horizontalSlider.setValue(round(actor_selected.GetProperty().GetOpacity() * 10))

    def hide_show_A(self):
        if self.G2.isHidden():
            self.toolButton_Transverse.setIcon(QIcon('resources/dl_axial.png'))
            self.G2.show()
            self.sagittalWidget.getScrollBar().show()
            self.actionhide_show_S.setEnabled(True)
            self.toolButton_Sagittal.show()
            self.G3.show()
            self.coronalWidget.getScrollBar().show()
            self.actionhide_show_C.setEnabled(True)
            self.toolButton_Coronal.show()
            self.G4.show()
            self.actionhide_show_3D.setEnabled(True)
            self.toolButton_3d.show()
            self.toolButton_reset_3d.show()
            self.verticalLayout_Transverse_2.addItem(self.spacerItem)
        else:
            self.toolButton_Transverse.setIcon(QIcon('resources/dl_fourviews.png'))
            self.G2.hide()
            self.sagittalWidget.getScrollBar().hide()
            self.actionhide_show_S.setEnabled(False)
            self.toolButton_Sagittal.hide()
            self.G3.hide()
            self.coronalWidget.getScrollBar().hide()
            self.actionhide_show_C.setEnabled(False)
            self.toolButton_Coronal.hide()
            self.G4.hide()
            self.actionhide_show_3D.setEnabled(False)
            self.toolButton_3d.hide()
            self.toolButton_reset_3d.hide()
            self.verticalLayout_Transverse_2.removeItem(self.spacerItem)

    def hide_show_C(self):
        if self.G1.isHidden():
            self.toolButton_Coronal.setIcon(QIcon('resources/dl_coronal.png'))
            self.G1.show()
            self.transverseWidget.getScrollBar().show()
            self.actionhide_show_A.setEnabled(True)
            self.toolButton_Transverse.show()
            self.G2.show()
            self.sagittalWidget.getScrollBar().show()
            self.actionhide_show_S.setEnabled(True)
            self.toolButton_Sagittal.show()
            self.G4.show()
            self.actionhide_show_3D.setEnabled(True)
            self.toolButton_3d.show()
            self.toolButton_reset_3d.show()
            self.verticalLayout_Transverse_2.addItem(self.spacerItem)
        else:
            self.toolButton_Coronal.setIcon(QIcon('resources/dl_fourviews.png'))
            self.G1.hide()
            self.transverseWidget.getScrollBar().hide()
            self.actionhide_show_A.setEnabled(False)
            self.toolButton_Transverse.hide()
            self.G2.hide()
            self.sagittalWidget.getScrollBar().hide()
            self.actionhide_show_S.setEnabled(False)
            self.toolButton_Sagittal.hide()
            self.G4.hide()
            self.actionhide_show_3D.setEnabled(False)
            self.toolButton_3d.hide()
            self.toolButton_reset_3d.hide()
            self.verticalLayout_Transverse_2.removeItem(self.spacerItem)

    def hide_show_S(self):
        if self.G1.isHidden():
            self.toolButton_Sagittal.setIcon(QIcon('resources/dl_sagittal.png'))
            self.G1.show()
            self.transverseWidget.getScrollBar().show()
            self.actionhide_show_A.setEnabled(True)
            self.toolButton_Transverse.show()
            self.G3.show()
            self.coronalWidget.getScrollBar().show()
            self.actionhide_show_C.setEnabled(True)
            self.toolButton_Coronal.show()
            self.G4.show()
            self.actionhide_show_3D.setEnabled(True)
            self.toolButton_3d.show()
            self.toolButton_reset_3d.show()
            self.verticalLayout_Transverse_2.addItem(self.spacerItem)
        else:
            self.toolButton_Sagittal.setIcon(QIcon('resources/dl_fourviews.png'))
            self.G1.hide()
            self.transverseWidget.getScrollBar().hide()
            self.toolButton_Transverse.hide()
            self.actionhide_show_A.setEnabled(False)
            self.G3.hide()
            self.coronalWidget.getScrollBar().hide()
            self.actionhide_show_C.setEnabled(False)
            self.toolButton_Coronal.hide()
            self.G4.hide()
            self.actionhide_show_3D.setEnabled(False)
            self.toolButton_3d.hide()
            self.toolButton_reset_3d.hide()
            self.verticalLayout_Transverse_2.removeItem(self.spacerItem)

    def hide_show_3D(self):
        if self.G1.isHidden():
            self.G1.show()
            self.transverseWidget.getScrollBar().show()
            self.actionhide_show_A.setEnabled(True)
            self.toolButton_Transverse.show()
            self.G2.show()
            self.sagittalWidget.getScrollBar().show()
            self.actionhide_show_S.setEnabled(True)
            self.toolButton_Sagittal.show()
            self.G3.show()
            self.coronalWidget.getScrollBar().show()
            self.actionhide_show_C.setEnabled(True)
            self.toolButton_Coronal.show()
            # self.toolButton_3d.show()
            # self.toolButton_reset_3d.show()
            # self.verticalLayout_Transverse_2.addItem(self.spacerItem)
        else:
            self.G1.hide()
            self.transverseWidget.getScrollBar().hide()
            self.toolButton_Transverse.hide()
            self.actionhide_show_A.setEnabled(False)
            self.G2.hide()
            self.sagittalWidget.getScrollBar().hide()
            self.actionhide_show_S.setEnabled(False)
            self.toolButton_Sagittal.hide()
            self.G3.hide()
            self.coronalWidget.getScrollBar().hide()
            self.actionhide_show_C.setEnabled(False)
            self.toolButton_Coronal.hide()
            # self.toolButton_3d.hide()
            # self.toolButton_reset_3d.hide()
            # self.verticalLayout_Transverse_2.removeItem(self.spacerItem)

    def hide_show_edit(self):
        self.widget.setVisible(not self.widget.isVisible())

    def hide_show_label(self):
        if self.label_origin is None:
            return
        if self.label is not None:
            self.label = None
        else:
            self.label = self.label_origin

        # 刷新3个面
        self.change_axial()
        self.change_sagi()
        self.change_corn()

    def scroll_bar_value_change(self, ori):
        """
        修改滚动条时，修改其他控件

        :param ori: 方向0:A(横断面z),1:S(矢状面x),2:C(冠状面y)
        """
        if 0 == ori:
            # self.label_slice.setText(
            #     '{} of {}'.format(self.transverseWidget.getScrollBar().value(), self.transverseWidget.getScrollBar().maximum()))
            self.textActors[0].SetInput(
                '{} of {}'.format(self.transverseWidget.getScrollBar().value(),
                                  self.transverseWidget.getScrollBar().maximum()))
        elif 1 == ori:
            # self.label_slice_2.setText(
            #     '{} of {}'.format(self.sagittalWidget.getScrollBar().value(), self.sagittalWidget.getScrollBar().maximum()))
            self.textActors[1].SetInput(
                '{} of {}'.format(self.sagittalWidget.getScrollBar().value(),
                                  self.sagittalWidget.getScrollBar().maximum()))
        elif 2 == ori:
            # self.label_slice_3.setText(
            #     '{} of {}'.format(self.coronalWidget.getScrollBar().value(), self.coronalWidget.getScrollBar().maximum()))
            self.textActors[2].SetInput(
                '{} of {}'.format(self.coronalWidget.getScrollBar().value(),
                                  self.coronalWidget.getScrollBar().maximum()))

    def slice_change_helper(self, renwin, ori):
        """
        切片变化后的辅助函数

        :param renwin: 窗口
        :param ori: 方向0:A(横断面z),1:S(矢状面x),2:C(冠状面y)
        """
        if self.main_image is None and self.label is None:
            return
        render = renwin.GetRenderers().GetFirstRenderer()
        renwin.RemoveRenderer(render)
        ren = vtkRenderer()
        if self.label is not None:
            image = self.get_slice(self.reader1, ori, True, self.img_center)
            mask = self.get_slice(self.reader2, ori, False, self.img_center)
            image.GetOutput().SetOrigin(self.Origins[ori])  # flip后会改变图像的origin，而十字线的坐标是由旧的origin算的，从而使得十字线中心偏移
            image.Update()
            mask.GetOutput().SetOrigin(self.Origins[ori])  # flip后会改变图像的origin，而十字线的坐标是由旧的origin算的，从而使得十字线中心偏移
            mask.Update()
            maskactor = vtkImageActor()
            imageactor = vtkImageActor()
            maskactor.SetInputData(mask.GetOutput())
            imageactor.SetInputData(image.GetOutput())
            ren.AddActor(maskactor)
            ren.AddActor(imageactor)
        else:
            if 1 == self.mode:
                image1 = self.get_slice(self.reader1, ori, True, self.img_center)
                image1.GetOutput().SetOrigin(self.Origins[ori])  # flip后会改变图像的origin，而十字线的坐标是由旧的origin算的，从而使得十字线中心偏移
                image1.Update()

                # self.fixed_image = read_img('img/T1_brain.nii.gz')
                # self.reader_fixed = self.numpyTovtkimage(sitk.GetArrayFromImage(self.fixed_image))
                image2 = self.get_slice(self.reader_fixed, ori, True, self.img_center)
                image2.GetOutput().SetOrigin(self.Origins[ori])  # flip后会改变图像的origin，而十字线的坐标是由旧的origin算的，从而使得十字线中心偏移
                image2.Update()

                checker = vtkImageCheckerboard()
                checker.SetInput1Data(image1.GetOutput())
                checker.SetInput2Data(image2.GetOutput())
                # checker.SetInputConnection(0, reader1.GetOutputPort())
                # checker.SetInputConnection(1, reader2.GetOutputPort())
                checker.SetNumberOfDivisions(9, 9, 1)

                imageactor = vtkImageActor()
                imageactor.GetMapper().SetInputConnection(checker.GetOutputPort())
                # imageactor.SetInputData(image.GetOutput())
                ren.AddActor(imageactor)
            else:
                image = self.get_slice(self.reader1, ori, True, self.img_center)
                image.GetOutput().SetOrigin(self.Origins[ori])  # flip后会改变图像的origin，而十字线的坐标是由旧的origin算的，从而使得十字线中心偏移
                image.Update()
                imageactor = vtkImageActor()
                imageactor.SetInputData(image.GetOutput())
                ren.AddActor(imageactor)
        line_ver, line_hor = cross_hair_actors(self.lines[ori][0], self.lines[ori][1], ori)
        ren.AddActor2D(self.textActors[ori])
        ren.AddActor(line_ver)
        ren.AddActor(line_hor)
        ren.SetBackground(0, 0, 0)
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.3)
        renwin.AddRenderer(ren)
        renwin.Render()

    def change_sagi(self):
        """
        矢状面变换事件S(x)
        """
        if self.main_image is None:
            return
        spacing = self.main_image.GetSpacing()
        origin = self.main_image.GetOrigin()
        self.img_center[0] = origin[0] + spacing[0] * (self.sagittalWidget.getScrollBar().value() - 1)
        self.scroll_bar_value_change(1)
        renwin = self.sagittal.GetRenderWindow()
        self.slice_change_helper(renwin, 1)

    def change_corn(self):
        """
        冠状面变换事件C(y)
        """
        if self.main_image is None:
            return
        spacing = self.main_image.GetSpacing()
        origin = self.main_image.GetOrigin()
        self.img_center[1] = origin[1] + spacing[1] * (self.coronalWidget.getScrollBar().value() - 1)
        self.scroll_bar_value_change(2)
        renwin = self.coronal.GetRenderWindow()
        self.slice_change_helper(renwin, 2)

    def change_axial(self):
        """
        横断面变换事件A(z)
        """
        if self.main_image is None:
            return
        spacing = self.main_image.GetSpacing()
        origin = self.main_image.GetOrigin()
        self.img_center[2] = origin[2] + spacing[2] * (self.transverseWidget.getScrollBar().value() - 1)
        self.scroll_bar_value_change(0)
        renwin = self.transverse.GetRenderWindow()
        self.slice_change_helper(renwin, 0)

    def update_all_windows(self):
        """
        更新所有窗口
        """
        self.slice_change_helper(self.transverse.GetRenderWindow(), 0)
        self.slice_change_helper(self.sagittal.GetRenderWindow(), 1)
        self.slice_change_helper(self.coronal.GetRenderWindow(), 2)

    def set_window_level(self, window, level):
        """
        设置窗宽窗位

        :param window: 窗宽
        :param level: 窗位
        """
        self.window = window
        self.level = level
        self.image_color_map = self.get_lookuptable(True)
        self.update_all_windows()

    def change_label_color(self):
        """
        更新颜色映射
        """
        # 更新颜色映射
        self.label_color_map = self.get_lookuptable(False)
        # 刷新窗口
        self.update_all_windows()

    def set_contrast(self):
        """
        设置窗宽窗位事件
        """
        if self.main_image is None:
            msg_box = HQUMessageBox.warning(self, 'Warning', 'Please load image file first')
            return
        self.contrast_window = ContrastWindow(self, self.minimum, self.maximum, self.window, self.level,
                                              self.set_window_level)
        self.contrast_window.exec_()

    def set_color_map(self):
        """
        更新所有窗口
        """
        self.label_editor_dialog_window = LabelEditorDialogWindow(self, self.change_label_color)
        self.label_editor_dialog_window.exec_()

    def clear_3d(self):
        """
        清空三维重建的框
        """
        renwin = self.restruct_3d.GetRenderWindow()
        renders = renwin.GetRenderers()
        renders.InitTraversal()
        for i in range(renders.GetNumberOfItems()):
            render = renders.GetNextItem()
            renwin.RemoveRenderer(render)

        self.polydatas = []

        self.ren_init()
        self.clicked = False
        # self.model_ren = vtkRenderer()
        self.render3d[0] = self.model_ren
        renwin.AddRenderer(self.render_tobe)
        renwin.Render()

    def show_floating_image(self):
        """
        显示浮动图
        """
        if self.floating_image_path == '':
            return
        self.mode = 0
        self.read_image_by_path(self.floating_image_path)

    def show_fixed_image(self):
        """
        显示参考图
        """
        if self.fixed_image_path == '':
            return
        self.mode = 0
        self.read_image_by_path(self.fixed_image_path)

    def show_registration_image(self):
        """
        显示配准结果
        """
        if self.registration_image_path == '':
            return
        self.mode = 0
        self.read_image_by_path(self.registration_image_path)

    def show_compare_image(self):
        """
        对比图片
        """
        self.mode = 1
        file_path1 = QFileDialog.getOpenFileName(self, 'Load Compare File1', '~',
                                                 'All Files (*.*);;'
                                                 'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz);;'
                                                 'NRRD (*.nrrd *.nhdr);;'
                                                 'DICOM (*.dcm);;'
                                                 'Gipl (*.gipl *.gipl.gz);;'
                                                 'Meta (*.mhd *.mha);;'
                                                 'MRC (*.mrc *.rec);;'
                                                 'MINC (*.mnc)'
                                                 'vtk (*.vtk)'
                                                 )[0]
        if '' != file_path1:
            file_path2 = QFileDialog.getOpenFileName(self, 'Load Compare File2', '~',
                                                     'All Files (*.*);;'
                                                     'NiFTI (*.nii.gz *.nii *.hdr *.img *.img.gz);;'
                                                     'NRRD (*.nrrd *.nhdr);;'
                                                     'DICOM (*.dcm);;'
                                                     'Gipl (*.gipl *.gipl.gz);;'
                                                     'Meta (*.mhd *.mha);;'
                                                     'MRC (*.mrc *.rec);;'
                                                     'MINC (*.mnc)'
                                                     'vtk (*.vtk)'
                                                     )[0]
            if '' != file_path2:
                # image1 = read_img(file_path1)
                image2 = read_img(file_path2)
                if image2 is None:
                    msg_box = HQUMessageBox.warning(self, 'Warning', 'Failed to load image')

                    return
                if self.read_image_by_path(file_path1) < 0:
                    return
                self.reader_fixed = self.numpyTovtkimage(sitk.GetArrayFromImage(image2))
                self.change_sagi()
                self.change_corn()
                self.change_axial()

    def read_image_by_path(self, main_file):
        """
        读取图片
        :param main_file: 图片路径
        :return: 0正常，<0读取失败
        """
        if '' != main_file:
            # if ReadImage(main_file) != False:
            self.var_init()
            self.clear_3d()

            self.image_path = main_file
            self.filename = os.path.basename(main_file)
            # self.clean_layout()
            reader2d = ReadImage(main_file)
            if reader2d:
                self.vtk_pipeline_image2d(self.transverse, reader2d)
            else:
                temp_main_image = read_img(main_file)  # (x,y,z),(S,C,A)
                if temp_main_image is None:
                    msg_box = HQUMessageBox.warning(self, 'Warning', 'Failed to load image')

                    return -1
                self.main_image = temp_main_image
                temp = sitk.GetArrayFromImage(self.main_image)  # (z,y,x),(A,C,S)
                self.main_image_shape = temp.shape
                # 获取各方向切片的个数 初始化滚轴
                self.dims = temp.shape[::-1]  # (x,y,z),(S,C,A)
                # A
                # self.transverseWidget.getScrollBar().valueChanged.disconnect(self.change_axial)
                self.transverseWidget.getScrollBar()
                self.transverseWidget.getScrollBar().blockSignals(True)
                self.transverseWidget.getScrollBar().setMinimum(1)
                self.transverseWidget.getScrollBar().setMaximum(self.dims[2])
                self.transverseWidget.getScrollBar().setValue(self.dims[2] // 2)
                # self.transverseWidget.getScrollBar().valueChanged.connect(self.change_axial)
                self.transverseWidget.getScrollBar().blockSignals(False)
                # self.label_slice.setText(
                #     '{} of {}'.format(self.transverseWidget.getScrollBar().value(), self.transverseWidget.getScrollBar().maximum()))
                # S
                # self.sagittalWidget.getScrollBar().valueChanged.disconnect(self.change_sagi)
                self.sagittalWidget.getScrollBar().blockSignals(True)
                self.sagittalWidget.getScrollBar().setMinimum(1)
                self.sagittalWidget.getScrollBar().setMaximum(self.dims[0])
                self.sagittalWidget.getScrollBar().setValue(self.dims[0] // 2)
                self.sagittalWidget.getScrollBar().blockSignals(False)
                # self.sagittalWidget.getScrollBar().valueChanged.connect(self.change_sagi)
                # self.label_slice_2.setText(
                #     '{} of {}'.format(self.sagittalWidget.getScrollBar().value(), self.sagittalWidget.getScrollBar().maximum()))
                # C
                # self.coronalWidget.getScrollBar().valueChanged.disconnect(self.change_corn)
                self.coronalWidget.getScrollBar().blockSignals(True)
                self.coronalWidget.getScrollBar().setMinimum(1)
                self.coronalWidget.getScrollBar().setMaximum(self.dims[1])
                self.coronalWidget.getScrollBar().setValue(self.dims[1] // 2)
                self.coronalWidget.getScrollBar().blockSignals(False)
                # self.coronalWidget.getScrollBar().valueChanged.connect(self.change_corn)
                # self.label_slice_3.setText(
                #     '{} of {}'.format(self.coronalWidget.getScrollBar().value(), self.coronalWidget.getScrollBar().maximum()))

                spacing = self.main_image.GetSpacing()
                origin = self.main_image.GetOrigin()
                self.img_center = [origin[i] + spacing[i] * (self.dims[i] // 2 - 1) for i in range(3)]

                self.minimum = temp.min()
                self.maximum = temp.max()
                self.level = (self.minimum + self.maximum) // 2
                self.window = self.maximum - self.minimum
                self.image = temp
                # self.image = normalize(temp)

                self.vtk_pipeline_image(self.transverse, 0)
                self.vtk_pipeline_image(self.sagittal, 1)
                self.vtk_pipeline_image(self.coronal, 2)

                spacing = self.main_image.GetSpacing()
                self.lineEdit_t.setText("%.6f" % spacing[0])
                self.lineEdit_s.setText("%.6f" % spacing[1])
                self.lineEdit_a.setText("%.6f" % spacing[2])

                return 0
            # self.lb3.set_sibling_nodes(sibling)
        return -2

    def initMaskWidget(self):
        """初始化一个遮罩"""
        self.darkWidget = QWidget(self)
        self.darkWidget.setObjectName("darkWidget")
        HLayout = QHBoxLayout(self.darkWidget)
        widget_iner = QWidget(self.darkWidget)
        widget_iner.setObjectName("widget_iner")
        HLayout.addWidget(widget_iner)
        HLayout.setContentsMargins(0, 0, 0, 0)
        self.darkWidget.setAttribute(Qt.WA_TranslucentBackground)
        self.darkWidget.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.darkWidget.setAutoFillBackground(True)
        self.darkWidget.setStyleSheet("#widget_iner{background:rgba(0,0,0,0.4);border-radius:5px;}")
        self.setAttribute(Qt.WA_QuitOnClose, True)
        self.darkWidget.setGeometry(self.x(), self.y(), self.width(), self.height())
        self.darkWidget.hide()
        QApplication.processEvents()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
