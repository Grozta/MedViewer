# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contrast.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(434, 149)
        Widget.setStyleSheet("\n"
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
"    border: 1px solid #A0A0A0; /* 边框宽度为1px,颜色为#A0A0A0 */\n"
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
"/*horizontal ,水平QSlider*/\n"
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
"/*width在这里无效,不写即可*/\n"
"}\n"
"\n"
"/*2.未滑动过的槽设计参数*/\n"
"QSlider::add-page:horizontal {\n"
"/*槽颜色*/\n"
"background: #5E5E5E;\n"
"/*外环大小0px就是不显示,默认也是0*/\n"
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
"/*滑块外环为1px,再加颜色*/\n"
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
"/*滑块外环为1px,再加颜色*/\n"
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
"#apply_pushButton{background:#2764c1;color:#DCDCDC;}\n"
"#apply_pushButton:hover{background:#4e9cd5;}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Widget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.toolButton_close = QtWidgets.QToolButton(self.widget)
        self.toolButton_close.setMinimumSize(QtCore.QSize(30, 0))
        self.toolButton_close.setMaximumSize(QtCore.QSize(30, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/btn_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_close.setIcon(icon)
        self.toolButton_close.setObjectName("toolButton_close")
        self.horizontalLayout_2.addWidget(self.toolButton_close)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.window_spinBox = QtWidgets.QSpinBox(self.widget)
        self.window_spinBox.setObjectName("window_spinBox")
        self.gridLayout.addWidget(self.window_spinBox, 1, 1, 1, 1)
        self.level_spinBox = QtWidgets.QSpinBox(self.widget)
        self.level_spinBox.setObjectName("level_spinBox")
        self.gridLayout.addWidget(self.level_spinBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok_pushButton = QtWidgets.QPushButton(self.widget)
        self.ok_pushButton.setMinimumSize(QtCore.QSize(70, 28))
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.horizontalLayout.addWidget(self.ok_pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(218, 22, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.apply_pushButton = QtWidgets.QPushButton(self.widget)
        self.apply_pushButton.setMinimumSize(QtCore.QSize(70, 28))
        self.apply_pushButton.setObjectName("apply_pushButton")
        self.horizontalLayout.addWidget(self.apply_pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(218, 22, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.reset_pushButton = QtWidgets.QPushButton(self.widget)
        self.reset_pushButton.setMinimumSize(QtCore.QSize(70, 28))
        self.reset_pushButton.setObjectName("reset_pushButton")
        self.horizontalLayout.addWidget(self.reset_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)
        Widget.setTabOrder(self.level_spinBox, self.window_spinBox)
        Widget.setTabOrder(self.window_spinBox, self.ok_pushButton)
        Widget.setTabOrder(self.ok_pushButton, self.apply_pushButton)
        Widget.setTabOrder(self.apply_pushButton, self.reset_pushButton)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.toolButton_close.setText(_translate("Widget", "x"))
        self.label_2.setText(_translate("Widget", "窗宽大小: "))
        self.label.setText(_translate("Widget", "窗口位置: "))
        self.ok_pushButton.setText(_translate("Widget", "确定"))
        self.apply_pushButton.setText(_translate("Widget", "应用"))
        self.reset_pushButton.setText(_translate("Widget", "重置"))

