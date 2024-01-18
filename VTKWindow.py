from ui_VTKWindow import Ui_VTKWindow
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSignal, pyqtSlot, QSize, QRect, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QSlider, QSizePolicy, QScrollBar, QToolButton, \
    QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap


class VTKWindow(QWidget, Ui_VTKWindow):

    def __init__(self, vtkInteractWindow=None, name='', parent=None):
        # 初始化ui
        self._name = name
        self._vtkInteractWindow = vtkInteractWindow
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        # 先显示vtk
        self.initVtk()
        # 显示控制UI
        self.initControl()

    def initControl(self):
        # 顶部的控制
        self.operatorWindow = QWidget(self)
        self.operatorWindow.setObjectName("operatorWindow")
        self.horizontalLayout = QHBoxLayout(self.operatorWindow)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setAlignment(Qt.AlignRight)
        icon = QIcon()
        self.toolButton_VtkMax = QToolButton(self.operatorWindow)
        icon.addPixmap(QPixmap("resources/vtkWindowMax.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_VtkMax.setIcon(icon)
        self.toolButton_VtkMax.setObjectName("toolButton_VtkMax")
        self.toolButton_VtkMax.setToolTip(self.tr("全屏显示"))
        self.horizontalLayout.addWidget(self.toolButton_VtkMax)
        self.toolButton_VtkMax.setVisible(False)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("resources/vtkWindowTrans.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_vtkTrans = QToolButton(self.operatorWindow)
        self.toolButton_vtkTrans.setIcon(icon1)
        self.toolButton_vtkTrans.setObjectName("toolButton_vtkTrans")
        self.toolButton_vtkTrans.setToolTip(self.tr("大屏显示"))
        self.horizontalLayout.addWidget(self.toolButton_vtkTrans)
        # 右侧的
        self.verticalScrollBar = QScrollBar(self.renderWindow)
        self.verticalScrollBar.setGeometry(QRect(430, 120, 8, 391))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalScrollBar.sizePolicy().hasHeightForWidth())
        self.verticalScrollBar.setSizePolicy(sizePolicy)
        self.verticalScrollBar.setMinimumSize(QSize(5, 0))
        self.verticalScrollBar.setMaximumSize(QSize(14, 16777215))
        self.verticalScrollBar.setMouseTracking(False)
        self.verticalScrollBar.setOrientation(Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        # 底部加一个slider和一个label
        self.sliderWindow = QWidget(self)
        self.sliderWindow.setObjectName("sliderWindow")
        self.hLayout_slider = QHBoxLayout(self.sliderWindow)
        self.hLayout_slider.setContentsMargins(0, 0, 0, 0)
        self.hLayout_slider.setObjectName("hLayout_slider")
        self.horizontalSlider = QSlider(self.renderWindow)
        self.horizontalSlider.setMaximumHeight(14)
        self.horizontalSlider.setRange(0,100)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.hLayout_slider.addWidget(self.horizontalSlider)
        self.sliderResLbel = QLabel(self.sliderWindow)
        self.sliderResLbel.setText("0%")
        self.sliderResLbel.setMaximumWidth(32)
        self.sliderResLbel.setMinimumWidth(32)
        self.sliderResLbel.setObjectName("sliderResLbel")
        self.hLayout_slider.addWidget(self.sliderResLbel)
        self.hLayout_slider.setSpacing(6)
        self.sliderWindow.setVisible(False)

        self.horizontalSlider.valueChanged.connect(self.HSliderValueChanged)
        # 初试化位置
        self.setControlGeometry()

    def HSliderValueChanged(self,value):
        self.sliderResLbel.setText("%s%%" % (int(value / self.horizontalSlider.maximum() * 100)))

    def initVtk(self):
        self.renderVLayout = QVBoxLayout(self.renderWindow)
        self.renderVLayout.setObjectName("renderVLayout")
        self.renderVLayout.setContentsMargins(2, 2, 2, 2)
        self.renderWindow.setLayout(self.renderVLayout)
        self.renderWindow.layout().setAlignment(Qt.AlignVCenter)
        # 设置操作窗口的对齐方式
        # self.operatorWindow.setLayoutDirection(Qt.RightToLeft)
        self.renderWindow.layout().addWidget(self._vtkInteractWindow)

    def getWindowName(self):
        return self._name

    def getVTKWindow(self):
        return self._vtkInteractWindow

    def getScrollBar(self):
        return self.verticalScrollBar

    def getHSlider(self):
        return self.horizontalSlider

    def getOperatorWidget(self):
        return self.operatorWindow

    def setControlGeometry(self):
        rightSpace = 10
        # 定位scrollBar 靠右，预留20个像素位置，上下预留20%位置
        scrollBarWidth = 8
        scrollBarHeight = self.renderWindow.height() * 0.6
        scrollBarX = self.renderWindow.width() - rightSpace - scrollBarWidth
        scrollBarY = self.renderWindow.height() * 0.2
        self.verticalScrollBar.setGeometry(scrollBarX, scrollBarY, scrollBarWidth, scrollBarHeight)
        # 定位操作widget 右对齐，预留20个像素位置
        operatorX = self.renderWindow.width() - self.operatorWindow.width() - rightSpace + 2
        operatorY = 3
        self.operatorWindow.setGeometry(operatorX, operatorY, self.operatorWindow.width(), self.operatorWindow.height())
        # 定位底部的3d使用的slider 长度为60%。高为30，底部边距render的0.05%
        sliderHeight = 14
        sliderWidth = int(self.renderWindow.width() * 0.7)
        sliderX = int(self.renderWindow.width() * 0.2)
        sliderY = int(self.renderWindow.height() * 0.95 - sliderHeight)
        self.sliderWindow.setGeometry(sliderX, sliderY, sliderWidth, sliderHeight)

    def resizeEvent(self, event) -> None:
        # super(VTKWindow, self).resizeEvent(event)
        self.setControlGeometry()
        return super().resizeEvent(event)

    def enterEvent(self, event):
        self.renderWindow.setStyleSheet("#renderWindow{border:1px solid #2764c1}; border-radius:3px;")
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.renderWindow.setStyleSheet("#renderWindow{border-color:transparent;}")
        return super().leaveEvent(event)

    # def mouseMoveEvent(self, event):
    #     if self.operatorWindow.geometry().contains(self.mapFromGlobal(event.pos())):
    #         self.operatorWindow.setStyleSheet("#operatorWindow{border: 1px solid  #5E5E5E;border-radius: 3px;}")
    #     else:
    #         self.operatorWindow.setStyleSheet("#operatorWindow{border-color:#000000;}")
    #
    #     if self.verticalScrollBar.geometry().contains(self.mapFromGlobal(event.pos())):
    #         self.verticalScrollBar.setStyleSheet("#verticalScrollBar{border: 1px solid  #5E5E5E;border-radius: 3px;}")
    #     else:
    #         self.verticalScrollBar.setStyleSheet("#verticalScrollBar{border-color:#000000;}")
    #
    #     return super(VTKWindow, self).mouseMoveEvent(event)
