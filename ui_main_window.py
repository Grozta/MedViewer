# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1404, 832)
        Form.setMouseTracking(True)
        Form.setStyleSheet("\n"
"/*------------------------------------全局样式-----------------------------------------*/\n"
"QWidget{font: 12px;color:#DCDCDC;font-family:\'微软雅黑\';}\n"
"QFrame{border-radius:5px;}\n"
"/*QScrollBar*/\n"
"QScrollArea{border:none}\n"
"QScrollBar{border:none;background:transparent;}\n"
"QScrollBar::add-page,QScrollBar::sub-page{background:transparent;}\n"
"QScrollBar::add-line,QScrollBar::sub-line { background: none; }\n"
"QScrollBar::handle{ background:rgba(91, 100, 116, 0.5); border-radius: 3px; width:3px}\n"
"QScrollBar:vertical{width:7px;padding-left:2px;padding-right:2px;}\n"
"QScrollBar:horizontal{height:7px;padding-top:2px;padding-bottom:2px;}\n"
"\n"
"/*QTabWidget*/\n"
"QTabWidget::pane{border:1px solid #1b1b1b;background:#1b1b1b;}\n"
"\n"
"QTabBar::tab{        \n"
"    width:84px;                    \n"
"    height:25;\n"
"    font: 16px;\n"
"    color:#DCDCDC;                     \n"
"    margin-top:0px;             \n"
"    margin-right:5px;\n"
"    margin-left:5px;\n"
"    background:#1b1b1b;\n"
"\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected {\n"
"\n"
"    /*border-image: url(:/common/images/common/左_normal.png);*/\n"
"}\n"
"QTabBar::tab:selected {\n"
"    color:#2764c1;     \n"
"    border:2px solid;\n"
"    border-top:0px;\n"
"    border-right:0px;\n"
"    border-left:0px;\n"
"    border-bottom-color:#2764c1;\n"
"}\n"
"QTabWidget::tab-bar {\n"
"alignment: left;\n"
"} \n"
"/*QTabWidget::pane{background:transparent;}*/\n"
"/*QStackedWidget*/\n"
"\n"
"/*QToolButton*/\n"
"QToolButton\n"
"{background:rgba(0,0,0,0); }\n"
"QToolButton:hover\n"
"{border:1px solid;border-top:0px;border-right:0px;border-left:0px;border-bottom-color:#2764c1;background:rgba(151,151,151,0.05);}\n"
"/*QPushButton*/\n"
"QPushButton\n"
"{background:#5E5E5E;border-radius:5px; }\n"
"QPushButton:hover\n"
"{border:1px solid #2764c1;}\n"
"/*QMenu*/\n"
"QMenu {\n"
"    background-color:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0.7 #1a1d23,stop:1 #1a1d23);\n"
"    border:1px solid #282c34;\n"
"    border-radius:8px;\n"
"    padding-left:2px;\n"
"}\n"
"QMenu::item {\n"
"    font-size:8pt;\n"
"    color: #DCDCDC;\n"
"    background-color:transparent;;\n"
"    padding-right: 2px;\n"
"    margin: 2px 1px;\n"
"}\n"
"QMenu::item:selected {\n"
"    border:1px ridge #259bd9;\n"
"    border-radius:2px;\n"
"}\n"
"QMenu::icon:checked {\n"
"    background:#259bd9;\n"
"    position: absolute;\n"
"    top: 1px;\n"
"    right: 1px;\n"
"    bottom: 1px;\n"
"    left: 1px;\n"
"}\n"
"QMenu::icon:checked:selected {\n"
"    background-color : #259bd9;\n"
"    background-image: url(:/space_selected.png);\n"
"}\n"
"QListWidget\n"
"{\n"
"    background-color:transparent;   \n"
"    font-size:12px;\n"
"    color: #f2f2f2;\n"
"}\n"
"/*\n"
"tabelwidget*/\n"
"QTableWidget{\n"
"color:#DCDCDC;\n"
"background-color:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0 #232323,stop:1 #121212 );\n"
"border:1px solid #242424;\n"
"}\n"
"QTableWidget::Item{border:0px solid rgb(255,0,0);border-bottom:1px solid #242424;}\n"
"\n"
"/*选中item*/\n"
"QTableWidget::item:selected{\n"
"color:#DCDCDC;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #484848,stop:1 #383838);\n"
"}\n"
"\n"
"/*\n"
"悬浮item*/\n"
"QTableWidget::item:hover{\n"
"background:rgba(0,0,0,0);\n"
"}\n"
"/*表头*/\n"
"QHeaderView::section{\n"
"text-align:center;\n"
"background:#5E5E5E;\n"
"padding:3px;\n"
"margin:0px;\n"
"color:#DCDCDC;\n"
"border:1px solid #242424;\n"
"border-left-width:0;\n"
"}\n"
"/*QLineEdit*/\n"
"QLineEdit {\n"
"    border: 1px solid #A0A0A0; /* 边框宽度为1px，颜色为#A0A0A0 */\n"
"    border-radius: 3px; /* 边框圆角 */\n"
"    padding-left: 5px; /* 文本距离左边界有5px */\n"
"    background-color: transparent; /* 背景颜色 */\n"
"    color: #DCDCDC; /* 文本颜色 */\n"
"    selection-background-color: #A0A0A0; /* 选中文本的背景颜色 */\n"
"    selection-color: #F2F2F2; /* 选中文本的颜色 */\n"
"    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
"    font-size: 10pt; /* 文本字体大小 */\n"
"}\n"
"\n"
"/*horizontal ：水平QSlider*/\n"
"QSlider::groove:horizontal {\n"
"border: 0px solid #bbb;\n"
"}\n"
"\n"
"/*1.滑动过的槽设计参数*/\n"
"QSlider::sub-page:horizontal {\n"
" /*槽颜色*/\n"
"background: #2764c1;\n"
" /*外环区域倒圆角度*/\n"
"border-radius: 2px;\n"
" /*上遮住区域高度*/\n"
"margin-top:8px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:8px;\n"
"/*width在这里无效，不写即可*/\n"
"}\n"
"\n"
"/*2.未滑动过的槽设计参数*/\n"
"QSlider::add-page:horizontal {\n"
"/*槽颜色*/\n"
"background: #5E5E5E;\n"
"/*外环大小0px就是不显示，默认也是0*/\n"
"border: 0px solid #777;\n"
"/*外环区域倒圆角度*/\n"
"border-radius: 2px;\n"
" /*上遮住区域高度*/\n"
"margin-top:9px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:9px;\n"
"}\n"
" \n"
"/*3.平时滑动的滑块设计参数*/\n"
"QSlider::handle:horizontal {\n"
"/*滑块颜色*/\n"
"background: rgb(193,204,208);\n"
"/*滑块的宽度*/\n"
"width: 5px;\n"
"/*滑块外环为1px，再加颜色*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*滑块外环倒圆角度*/\n"
"border-radius: 2px; \n"
" /*上遮住区域高度*/\n"
"margin-top:6px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:6px;\n"
"}\n"
"\n"
"/*4.手动拉动时显示的滑块设计参数*/\n"
"QSlider::handle:horizontal:hover {\n"
"/*滑块颜色*/\n"
"background: rgb(193,204,208);\n"
"/*滑块的宽度*/\n"
"width: 10px;\n"
"/*滑块外环为1px，再加颜色*/\n"
"border: 1px solid rgb(193,204,208);\n"
" /*滑块外环倒圆角度*/\n"
"border-radius: 5px; \n"
" /*上遮住区域高度*/\n"
"margin-top:4px;\n"
" /*下遮住区域高度*/\n"
"margin-bottom:4px;\n"
"}\n"
"/*QGroupBox*/\n"
"QGroupBox {\n"
"    /* 背景渐变色*/\n"
"    background-color:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0 #232323,stop:1 #121212 );\n"
"    /* 边框 */\n"
"    border: 1px solid #5E5E5E;\n"
"\n"
"    /* 倒角 */\n"
"    border-radius: 5px;\n"
"padding: -16 6px 0 6px;\n"
"\n"
"    /* 就像墙上挂着的两个相框,margin指的是相框与相框的距离\n"
"       padding指的是每个相框里照片与相框边框的距离*/\n"
"    margin-top: 8px; \n"
"}\n"
"/* 标题设置 */\n"
"QGroupBox::title {\n"
"    /* 位置 */\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left:10px; /* //线的偏离度 */\n"
"    margin-left: 0px;\n"
"    padding:0 1px;/* //文字在方框中位置的偏离度 */\n"
"    /* 内边框,上下和左右\n"
"    /* padding: 30px 15px; */\n"
"\n"
"    /* 颜色 \n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                      stop: 0 #FF0ECE, stop: 1 #FFFFFF);*/\n"
"}\n"
"\n"
"QSplitter::handle {\n"
"    /*image:url(:/images/444.bmp);*/\n"
"    border-radius: 3px;\n"
"}\n"
"QSplitter::handle:hover {\n"
"    /*image:url(:/images/444.bmp);*/\n"
"    background-color:rgba(70,130,180,0.3);\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QSplitter::handle:horizontal {\n"
"    \n"
"    width:5px;\n"
"}\n"
"\n"
"QSplitter::handle:vertical {\n"
"    \n"
"    width:5px;\n"
"}\n"
"\n"
"QSplitter::handle:pressed {\n"
"    \n"
"    background-color:rgba(70,130,180,0.1);\n"
"     border-radius: 3px;\n"
"}\n"
"QSpinBox {\n"
"    padding-top: 2px;\n"
"    padding-bottom: 2px;\n"
"    padding-left: 4px;\n"
"    padding-right: 15px;\n"
"    border: 1px solid rgb(64,64,64);\n"
"    border-radius: 3px;\n"
"    color: rgb(200,200,200);\n"
"    background-color: rgb(44,44,44);\n"
"    selection-color: rgb(235,235,235);\n"
"    selection-background-color: rgb(83,121,180);\n"
"    font-family: \"Microsoft Yahei\";\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QSpinBox:hover {\n"
"    background-color: rgb(59,59,59);\n"
"}\n"
"\n"
"QSpinBox::up-button { /* 向上按钮 */\n"
"    subcontrol-origin: border; /* 起始位置 */\n"
"    subcontrol-position: top right; /* 居于右上角 */\n"
"    border: none;\n"
"    width: 12px;\n"
"    margin-top: 2px;\n"
"    margin-right: 1px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QSpinBox::up-button:hover {\n"
"    border: none;\n"
"}\n"
"\n"
"QSpinBox::up-arrow { /* 向上箭头，图片大小为8x8 */\n"
"    image: url(resources/btn_spin_up.png);\n"
"}\n"
"\n"
"QSpinBox::up-arrow:hover {\n"
"    image: url(resources/btn_spin_up_hover.png);\n"
"}\n"
"\n"
"QSpinBox::up-arrow:disabled, QSpinBox::up-arrow:off {\n"
"    image: url(resources/btn_spin_up_disable.png);\n"
"}\n"
"\n"
"QSpinBox::down-button { /* 向下按钮 */\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    border: none;\n"
"    width: 12px;\n"
"    margin-top: 0px;\n"
"    margin-right: 1px;\n"
"    margin-bottom: 2px;\n"
"}\n"
"\n"
"QSpinBox::down-button:hover {\n"
"    border: none;\n"
"}\n"
"\n"
"QSpinBox::down-arrow { /* 向下箭头 */\n"
"    image: url(resources/btn_spin_down.png);\n"
"}\n"
"\n"
"QSpinBox::down-arrow:hover {\n"
"    image: url(resources/btn_spin_down_hover.png);\n"
"}\n"
"\n"
"QSpinBox::down-arrow:disabled, QSpinBox::down-arrow:off {\n"
"    image: url(resources/btn_spin_down_disable.png);\n"
"}\n"
"/*--------------------------------------特征样式---------------------------------------*/\n"
"#windowTitel #label_version{font:7pt;}\n"
"#widget{background-color:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0.7 #232323,stop:1 #121212 );border-radius:5px;}\n"
"#Form{background-color:rgba(255,255,255,0.01);}\n"
"#titel>QWidget{color:#DCDCDC;font:12pt;}\n"
"\n"
"#windowsControl>#toolButton_close:hover\n"
"{border-bottom-color:rgba(196,43,28,0.5);\n"
"background-color:rgba(196,43,28,0.2);border-radius: 3px;}\n"
"\n"
"#widget_line,#widget_line_2{\n"
"background:transparent;\n"
"border:15px solid #333946;\n"
"border-top:0px;\n"
"border-left:0px;\n"
"border-bottom:0px;}\n"
"\n"
"#tool{border:0px solid #333946;\n"
"border-top:0px;\n"
"border-right:0px;\n"
"border-left:0px;\n"
"border-bottom-color:qlineargradient(spread:pad,x1:0, y1:0, x2:1, y2:1,stop:0 #000000,stop:1 #2764c1);\n"
"}\n"
"\n"
"#progressBar{ \n"
"    border-top:1px;         \n"
"    background-color:#2764c1;\n"
"    qproperty-textVisible:false;\n"
"}\n"
"#toolButton_import{background:#259bd9;border-radius:8px;color:#DCDCDC;}\n"
"\n"
"#toolButton_import:hover{background:#259ba9;}\n"
"#page_home{background-color:transparent;}\n"
"#mian{background-color:transparent;}\n"
"#widget_edit,#widget_vtk{\n"
"background:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0.7 #232323,stop:1 #121212 );\n"
"/*background:#121212;*/\n"
"border:1px solid #5E5E5E;\n"
"border-radius:3px;\n"
"}\n"
"#widget_vtk{\n"
"background:transparent;\n"
"}\n"
"\n"
"")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMouseTracking(True)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titel = QtWidgets.QWidget(self.widget)
        self.titel.setMinimumSize(QtCore.QSize(0, 22))
        self.titel.setMaximumSize(QtCore.QSize(16777215, 22))
        self.titel.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.titel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.titel.setObjectName("titel")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.titel)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.windowTitel = QtWidgets.QWidget(self.titel)
        self.windowTitel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.windowTitel.setObjectName("windowTitel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.windowTitel)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_icon = QtWidgets.QLabel(self.windowTitel)
        self.label_icon.setMaximumSize(QtCore.QSize(25, 26))
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap("resources/test2.png"))
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout.addWidget(self.label_icon)
        self.label_text = QtWidgets.QLabel(self.windowTitel)
        self.label_text.setObjectName("label_text")
        self.horizontalLayout.addWidget(self.label_text)
        self.label_version = QtWidgets.QLabel(self.windowTitel)
        self.label_version.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label_version.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_version.setObjectName("label_version")
        self.horizontalLayout.addWidget(self.label_version)
        self.widget_line_2 = QtWidgets.QWidget(self.windowTitel)
        self.widget_line_2.setMinimumSize(QtCore.QSize(1, 8))
        self.widget_line_2.setMaximumSize(QtCore.QSize(16777215, 18))
        self.widget_line_2.setObjectName("widget_line_2")
        self.horizontalLayout.addWidget(self.widget_line_2)
        self.toolButton_ResetImage = QtWidgets.QToolButton(self.windowTitel)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icon_reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_ResetImage.setIcon(icon)
        self.toolButton_ResetImage.setObjectName("toolButton_ResetImage")
        self.horizontalLayout.addWidget(self.toolButton_ResetImage)
        self.toolButton_ImportImage = QtWidgets.QToolButton(self.windowTitel)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/icon_open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_ImportImage.setIcon(icon1)
        self.toolButton_ImportImage.setObjectName("toolButton_ImportImage")
        self.horizontalLayout.addWidget(self.toolButton_ImportImage)
        self.toolButton_ExportImage = QtWidgets.QToolButton(self.windowTitel)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/btn_report_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_ExportImage.setIcon(icon2)
        self.toolButton_ExportImage.setObjectName("toolButton_ExportImage")
        self.horizontalLayout.addWidget(self.toolButton_ExportImage)
        self.horizontalLayout_3.addWidget(self.windowTitel)
        self.label_titel = QtWidgets.QLabel(self.titel)
        self.label_titel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_titel.setAutoFillBackground(False)
        self.label_titel.setScaledContents(False)
        self.label_titel.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titel.setObjectName("label_titel")
        self.horizontalLayout_3.addWidget(self.label_titel)
        self.globleControl = QtWidgets.QWidget(self.titel)
        self.globleControl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.globleControl.setObjectName("globleControl")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.globleControl)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolButton_about = QtWidgets.QToolButton(self.globleControl)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("resources/icon_about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_about.setIcon(icon3)
        self.toolButton_about.setObjectName("toolButton_about")
        self.horizontalLayout_2.addWidget(self.toolButton_about)
        self.toolButton_system = QtWidgets.QToolButton(self.globleControl)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("resources/icon_setting.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_system.setIcon(icon4)
        self.toolButton_system.setObjectName("toolButton_system")
        self.horizontalLayout_2.addWidget(self.toolButton_system)
        self.toolButton_user = QtWidgets.QToolButton(self.globleControl)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("resources/icon_account.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_user.setIcon(icon5)
        self.toolButton_user.setObjectName("toolButton_user")
        self.horizontalLayout_2.addWidget(self.toolButton_user)
        self.widget_line = QtWidgets.QWidget(self.globleControl)
        self.widget_line.setMinimumSize(QtCore.QSize(1, 8))
        self.widget_line.setMaximumSize(QtCore.QSize(16777215, 18))
        self.widget_line.setObjectName("widget_line")
        self.horizontalLayout_2.addWidget(self.widget_line)
        self.horizontalLayout_3.addWidget(self.globleControl)
        self.windowsControl = QtWidgets.QWidget(self.titel)
        self.windowsControl.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.windowsControl.setObjectName("windowsControl")
        self.horizontalLayout_sysControl = QtWidgets.QHBoxLayout(self.windowsControl)
        self.horizontalLayout_sysControl.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_sysControl.setSpacing(0)
        self.horizontalLayout_sysControl.setObjectName("horizontalLayout_sysControl")
        self.toolButton_close = QtWidgets.QToolButton(self.windowsControl)
        self.toolButton_close.setMinimumSize(QtCore.QSize(30, 0))
        self.toolButton_close.setMaximumSize(QtCore.QSize(30, 16777215))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("resources/btn_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_close.setIcon(icon6)
        self.toolButton_close.setObjectName("toolButton_close")
        self.horizontalLayout_sysControl.addWidget(self.toolButton_close)
        self.toolButton_max = QtWidgets.QToolButton(self.windowsControl)
        self.toolButton_max.setMinimumSize(QtCore.QSize(30, 0))
        self.toolButton_max.setMaximumSize(QtCore.QSize(30, 16777215))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("resources/btn_window_04.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_max.setIcon(icon7)
        self.toolButton_max.setObjectName("toolButton_max")
        self.horizontalLayout_sysControl.addWidget(self.toolButton_max)
        self.toolButton_min = QtWidgets.QToolButton(self.windowsControl)
        self.toolButton_min.setMinimumSize(QtCore.QSize(30, 0))
        self.toolButton_min.setMaximumSize(QtCore.QSize(31, 16777215))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("resources/btn_shrink_02.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_min.setIcon(icon8)
        self.toolButton_min.setObjectName("toolButton_min")
        self.horizontalLayout_sysControl.addWidget(self.toolButton_min)
        self.horizontalLayout_3.addWidget(self.windowsControl)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addWidget(self.titel)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_home = QtWidgets.QWidget()
        self.page_home.setObjectName("page_home")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_home)
        self.verticalLayout_3.setContentsMargins(0, 3, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tool = QtWidgets.QWidget(self.page_home)
        self.tool.setObjectName("tool")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tool)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tabWidget = QtWidgets.QTabWidget(self.tool)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 22))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_segment = QtWidgets.QWidget()
        self.tab_segment.setObjectName("tab_segment")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.tab_segment)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.tabWidget.addTab(self.tab_segment, "")
        self.tab_registration = QtWidgets.QWidget()
        self.tab_registration.setObjectName("tab_registration")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_registration)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tabWidget.addTab(self.tab_registration, "")
        self.tab_keyPointCheck = QtWidgets.QWidget()
        self.tab_keyPointCheck.setObjectName("tab_keyPointCheck")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.tab_keyPointCheck)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(3)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.tabWidget.addTab(self.tab_keyPointCheck, "")
        self.tab_diagnoise = QtWidgets.QWidget()
        self.tab_diagnoise.setObjectName("tab_diagnoise")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_diagnoise)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tabWidget.addTab(self.tab_diagnoise, "")
        self.horizontalLayout_6.addWidget(self.tabWidget)
        self.verticalLayout_3.addWidget(self.tool)
        self.progressBar = QtWidgets.QProgressBar(self.page_home)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 1))
        self.progressBar.setProperty("value", 99)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.mian = QtWidgets.QWidget(self.page_home)
        self.mian.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.mian.setObjectName("mian")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.mian)
        self.horizontalLayout_16.setContentsMargins(1, -1, 1, -1)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.widget_edit = QtWidgets.QWidget(self.mian)
        self.widget_edit.setMinimumSize(QtCore.QSize(368, 0))
        self.widget_edit.setObjectName("widget_edit")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_edit)
        self.verticalLayout_9.setContentsMargins(9, 12, 9, 9)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.tabWidget_edit = QtWidgets.QTabWidget(self.widget_edit)
        self.tabWidget_edit.setObjectName("tabWidget_edit")
        self.tab_file_seg = QtWidgets.QWidget()
        self.tab_file_seg.setObjectName("tab_file_seg")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.tab_file_seg)
        self.horizontalLayout_19.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.tableWidget_seg = QtWidgets.QTableWidget(self.tab_file_seg)
        self.tableWidget_seg.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget_seg.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_seg.setAutoScrollMargin(8)
        self.tableWidget_seg.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_seg.setTabKeyNavigation(False)
        self.tableWidget_seg.setProperty("showDropIndicator", False)
        self.tableWidget_seg.setDragDropOverwriteMode(False)
        self.tableWidget_seg.setAlternatingRowColors(False)
        self.tableWidget_seg.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_seg.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_seg.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_seg.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_seg.setShowGrid(False)
        self.tableWidget_seg.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget_seg.setObjectName("tableWidget_seg")
        self.tableWidget_seg.setColumnCount(3)
        self.tableWidget_seg.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_seg.setHorizontalHeaderItem(2, item)
        self.tableWidget_seg.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_seg.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget_seg.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_seg.verticalHeader().setVisible(False)
        self.horizontalLayout_19.addWidget(self.tableWidget_seg)
        self.tabWidget_edit.addTab(self.tab_file_seg, "")
        self.tab_file_3d = QtWidgets.QWidget()
        self.tab_file_3d.setObjectName("tab_file_3d")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_file_3d)
        self.verticalLayout_8.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tableWidget_3d = QtWidgets.QTableWidget(self.tab_file_3d)
        self.tableWidget_3d.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_3d.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_3d.setAutoScrollMargin(8)
        self.tableWidget_3d.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_3d.setTabKeyNavigation(False)
        self.tableWidget_3d.setProperty("showDropIndicator", False)
        self.tableWidget_3d.setDragDropOverwriteMode(False)
        self.tableWidget_3d.setAlternatingRowColors(False)
        self.tableWidget_3d.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_3d.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_3d.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_3d.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_3d.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_3d.setShowGrid(False)
        self.tableWidget_3d.setWordWrap(False)
        self.tableWidget_3d.setObjectName("tableWidget_3d")
        self.tableWidget_3d.setColumnCount(4)
        self.tableWidget_3d.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3d.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3d.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3d.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3d.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3d.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3d.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3d.setHorizontalHeaderItem(3, item)
        self.tableWidget_3d.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_3d.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_3d.verticalHeader().setVisible(False)
        self.tableWidget_3d.verticalHeader().setHighlightSections(False)
        self.verticalLayout_8.addWidget(self.tableWidget_3d)
        self.tabWidget_edit.addTab(self.tab_file_3d, "")
        self.verticalLayout_9.addWidget(self.tabWidget_edit)
        self.widget_2 = QtWidgets.QWidget(self.widget_edit)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_14.setContentsMargins(-1, 27, -1, -1)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout_13.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.lineEdit_t = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_t.setMaximumSize(QtCore.QSize(85, 20))
        self.lineEdit_t.setObjectName("lineEdit_t")
        self.horizontalLayout_13.addWidget(self.lineEdit_t)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_12.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem2)
        self.lineEdit_s = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_s.setMaximumSize(QtCore.QSize(85, 20))
        self.lineEdit_s.setObjectName("lineEdit_s")
        self.horizontalLayout_12.addWidget(self.lineEdit_s)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_11.addWidget(self.label_5)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem4)
        self.lineEdit_a = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_a.setMaximumSize(QtCore.QSize(85, 20))
        self.lineEdit_a.setObjectName("lineEdit_a")
        self.horizontalLayout_11.addWidget(self.lineEdit_a)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_17.addLayout(self.verticalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_update = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_update.setMinimumSize(QtCore.QSize(60, 30))
        self.pushButton_update.setObjectName("pushButton_update")
        self.verticalLayout_5.addWidget(self.pushButton_update)
        self.pushButton_reset = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_reset.setMinimumSize(QtCore.QSize(60, 30))
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.verticalLayout_5.addWidget(self.pushButton_reset)
        self.horizontalLayout_17.addLayout(self.verticalLayout_5)
        self.horizontalLayout_14.addLayout(self.horizontalLayout_17)
        self.verticalLayout_10.addWidget(self.groupBox_2)
        self.verticalLayout_9.addWidget(self.widget_2)
        self.horizontalLayout_16.addWidget(self.widget_edit)
        self.widget_vtk = QtWidgets.QWidget(self.mian)
        self.widget_vtk.setObjectName("widget_vtk")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_vtk)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton = QtWidgets.QToolButton(self.widget_vtk)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 0, 1, 1)
        self.horizontalLayout_16.addWidget(self.widget_vtk)
        self.horizontalLayout_16.setStretch(1, 1)
        self.verticalLayout_3.addWidget(self.mian)
        self.verticalLayout_3.setStretch(2, 1)
        self.stackedWidget.addWidget(self.page_home)
        self.page_start = QtWidgets.QWidget()
        self.page_start.setObjectName("page_start")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_start)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem6 = QtWidgets.QSpacerItem(20, 209, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(18, -1, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem7)
        self.label_import = QtWidgets.QLabel(self.page_start)
        self.label_import.setMaximumSize(QtCore.QSize(142, 120))
        self.label_import.setText("")
        self.label_import.setPixmap(QtGui.QPixmap("resources/import_副本.png"))
        self.label_import.setObjectName("label_import")
        self.horizontalLayout_8.addWidget(self.label_import)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem8)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.toolButton_import = QtWidgets.QToolButton(self.page_start)
        self.toolButton_import.setMinimumSize(QtCore.QSize(120, 50))
        self.toolButton_import.setObjectName("toolButton_import")
        self.horizontalLayout_7.addWidget(self.toolButton_import)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem10)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem11 = QtWidgets.QSpacerItem(20, 209, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem11)
        self.stackedWidget.addWidget(self.page_start)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_edit.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_text.setText(_translate("Form", "ICML"))
        self.label_version.setText(_translate("Form", "V 0.0.1"))
        self.toolButton_ResetImage.setText(_translate("Form", "..."))
        self.toolButton_ImportImage.setText(_translate("Form", "..."))
        self.toolButton_ExportImage.setText(_translate("Form", "..."))
        self.label_titel.setText(_translate("Form", "骨科医学影像智能处理平台"))
        self.toolButton_about.setText(_translate("Form", "..."))
        self.toolButton_system.setText(_translate("Form", "..."))
        self.toolButton_user.setText(_translate("Form", "..."))
        self.toolButton_close.setText(_translate("Form", "x"))
        self.toolButton_max.setText(_translate("Form", "0"))
        self.toolButton_min.setText(_translate("Form", "-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_segment), _translate("Form", "图像分割"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_registration), _translate("Form", "图像配准"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_keyPointCheck), _translate("Form", "关键点检测"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_diagnoise), _translate("Form", "诊断辅助"))
        item = self.tableWidget_seg.verticalHeaderItem(0)
        item.setText(_translate("Form", "34"))
        item = self.tableWidget_seg.verticalHeaderItem(1)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget_seg.verticalHeaderItem(2)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_seg.verticalHeaderItem(3)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget_seg.verticalHeaderItem(4)
        item.setText(_translate("Form", "3"))
        item = self.tableWidget_seg.verticalHeaderItem(5)
        item.setText(_translate("Form", "4"))
        item = self.tableWidget_seg.verticalHeaderItem(6)
        item.setText(_translate("Form", "6"))
        item = self.tableWidget_seg.horizontalHeaderItem(0)
        item.setText(_translate("Form", "名称"))
        item = self.tableWidget_seg.horizontalHeaderItem(1)
        item.setText(_translate("Form", "可见"))
        item = self.tableWidget_seg.horizontalHeaderItem(2)
        item.setText(_translate("Form", "操作"))
        self.tabWidget_edit.setTabText(self.tabWidget_edit.indexOf(self.tab_file_seg), _translate("Form", "分割"))
        item = self.tableWidget_3d.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_3d.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget_3d.verticalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.tableWidget_3d.horizontalHeaderItem(0)
        item.setText(_translate("Form", "名称"))
        item = self.tableWidget_3d.horizontalHeaderItem(1)
        item.setText(_translate("Form", "可见"))
        item = self.tableWidget_3d.horizontalHeaderItem(2)
        item.setText(_translate("Form", "颜色"))
        item = self.tableWidget_3d.horizontalHeaderItem(3)
        item.setText(_translate("Form", "操作"))
        self.tabWidget_edit.setTabText(self.tabWidget_edit.indexOf(self.tab_file_3d), _translate("Form", "3D"))
        self.groupBox_2.setTitle(_translate("Form", "当前间距"))
        self.label.setText(_translate("Form", "横断面"))
        self.label_3.setText(_translate("Form", "冠状面"))
        self.label_5.setText(_translate("Form", "矢状面"))
        self.pushButton_update.setText(_translate("Form", "更新"))
        self.pushButton_reset.setText(_translate("Form", "重置"))
        self.toolButton.setText(_translate("Form", "..."))
        self.toolButton_import.setText(_translate("Form", "导入图像文件"))

