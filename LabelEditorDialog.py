# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LabelEditorDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LabelEditorDialog(object):
    def setupUi(self, LabelEditorDialog):
        LabelEditorDialog.setObjectName("LabelEditorDialog")
        LabelEditorDialog.resize(650, 547)
        LabelEditorDialog.setStyleSheet("\n"
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
"QTableWidget,QTableView{\n"
"color:#DCDCDC;\n"
"background-color:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0 #232323,stop:1 #121212 );\n"
"border:1px solid #242424;\n"
"}\n"
"QTableWidget::Item,QTableView::Item{border:0px solid rgb(255,0,0);border-bottom:1px solid #242424;}\n"
"\n"
"/*选中item*/\n"
"QTableWidget::item:selected,QTableView::item:selected{\n"
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
"QSpinBox::up-arrow { /* 向上箭头,图片大小为8x8 */\n"
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
"\n"
"#widget{background-color:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0.7 #232323,stop:1 #121212 );border-radius:5px;}\n"
"#btnLabelColor{background:rgba(151,151,151,0.1);border:7px solid;border-top:0px;border-right:0px;border-left:0px;border-bottom-color:#2764c1;}\n"
"")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(LabelEditorDialog)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(LabelEditorDialog)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_3.setStyleSheet("QGroupBox {\n"
"  background-origin: content;\n"
"  margin-top: 15px;\n"
"  font-weight: bold;\n"
"  font-size: 12px;\n"
"  padding: 5px;\n"
"  border-radius: 4px;\n"
"  border: 1px solid rgb(130,130,130);\n"
"}\n"
"QGroupBox::title {\n"
"  subcontrol-origin:     margin;\n"
"  subcontrol-position: top left;\n"
"}")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setContentsMargins(4, 4, 3, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lvLabels = QtWidgets.QTableView(self.groupBox_3)
        self.lvLabels.setStyleSheet("font-size:12px;")
        self.lvLabels.setAutoScrollMargin(16)
        self.lvLabels.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lvLabels.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.lvLabels.setAlternatingRowColors(False)
        self.lvLabels.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lvLabels.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lvLabels.setShowGrid(True)
        self.lvLabels.setCornerButtonEnabled(False)
        self.lvLabels.setObjectName("lvLabels")
        self.lvLabels.horizontalHeader().setVisible(False)
        self.lvLabels.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.lvLabels)
        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.grpSelectedLabel = QtWidgets.QGroupBox(self.widget)
        self.grpSelectedLabel.setStyleSheet("QGroupBox {\n"
"  background-origin: content;\n"
"  margin-top: 15px;\n"
"  font-weight: bold;\n"
"  font-size: 12px;\n"
"  padding: 5px;\n"
"  border-radius: 4px;\n"
"  border: 1px solid rgb(130,130,130);\n"
"}\n"
"QGroupBox::title {\n"
"  subcontrol-origin:     margin;\n"
"  subcontrol-position: top left;\n"
"}")
        self.grpSelectedLabel.setObjectName("grpSelectedLabel")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.grpSelectedLabel)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.grpSelectedLabel)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.inLabelDescription = QtWidgets.QLineEdit(self.grpSelectedLabel)
        self.inLabelDescription.setObjectName("inLabelDescription")
        self.verticalLayout_2.addWidget(self.inLabelDescription)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.widget_2 = QtWidgets.QWidget(self.grpSelectedLabel)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_6 = QtWidgets.QWidget(self.grpSelectedLabel)
        self.widget_6.setMinimumSize(QtCore.QSize(0, 100))
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_6)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.inGreen = QtWidgets.QSpinBox(self.widget_6)
        self.inGreen.setMinimumSize(QtCore.QSize(90, 0))
        self.inGreen.setMaximumSize(QtCore.QSize(56, 16777215))
        self.inGreen.setMaximum(255)
        self.inGreen.setObjectName("inGreen")
        self.gridLayout_3.addWidget(self.inGreen, 1, 3, 1, 2)
        self.label_8 = QtWidgets.QLabel(self.widget_6)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 2, 1, 1)
        self.inBlue = QtWidgets.QSpinBox(self.widget_6)
        self.inBlue.setMinimumSize(QtCore.QSize(90, 0))
        self.inBlue.setMaximumSize(QtCore.QSize(56, 16777215))
        self.inBlue.setMaximum(255)
        self.inBlue.setObjectName("inBlue")
        self.gridLayout_3.addWidget(self.inBlue, 2, 3, 1, 1)
        self.inRed = QtWidgets.QSpinBox(self.widget_6)
        self.inRed.setMinimumSize(QtCore.QSize(90, 0))
        self.inRed.setMaximumSize(QtCore.QSize(56, 16777215))
        self.inRed.setMaximum(255)
        self.inRed.setObjectName("inRed")
        self.gridLayout_3.addWidget(self.inRed, 0, 3, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.widget_6)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget_6)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 1, 1, 1, 1)
        self.inColorWheel = QtWidgets.QWidget(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inColorWheel.sizePolicy().hasHeightForWidth())
        self.inColorWheel.setSizePolicy(sizePolicy)
        self.inColorWheel.setMinimumSize(QtCore.QSize(120, 120))
        self.inColorWheel.setMaximumSize(QtCore.QSize(120, 120))
        self.inColorWheel.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.inColorWheel.setObjectName("inColorWheel")
        self.gridLayout_3.addWidget(self.inColorWheel, 0, 0, 4, 1)
        self.btnLabelColor = QtWidgets.QToolButton(self.widget_6)
        self.btnLabelColor.setMinimumSize(QtCore.QSize(123, 0))
        self.btnLabelColor.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btnLabelColor.setObjectName("btnLabelColor")
        self.gridLayout_3.addWidget(self.btnLabelColor, 3, 2, 1, 3)
        self.verticalLayout_2.addWidget(self.widget_6)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)
        self.widget_3 = QtWidgets.QWidget(self.grpSelectedLabel)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2.addWidget(self.widget_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.grpSelectedLabel)
        self.groupBox_2.setStyleSheet("QGroupBox {\n"
"  background-origin: content;\n"
"  margin-top: 15px;\n"
"  font-weight: normal;\n"
"  color: #f2f2f2;\n"
"  background-color: #353643;\n"
"  padding: 5px;\n"
"  border-radius: 0px;\n"
"  border-top: 1px solid rgb(130,130,130);\n"
"  border-left: none;\n"
"  border-right:none;\n"
"  border-bottom:none;\n"
"}\n"
"QGroupBox::title {\n"
"  subcontrol-origin:     margin;\n"
"  subcontrol-position: top left;\n"
"}")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.inLabelId = QtWidgets.QSpinBox(self.widget_4)
        self.inLabelId.setMinimumSize(QtCore.QSize(80, 0))
        self.inLabelId.setReadOnly(False)
        self.inLabelId.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inLabelId.setObjectName("inLabelId")
        self.horizontalLayout_4.addWidget(self.inLabelId)
        self.verticalLayout_6.addWidget(self.widget_4)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.gridLayout.addWidget(self.grpSelectedLabel, 0, 1, 1, 1)
        self.widget5 = QtWidgets.QWidget(self.widget)
        self.widget5.setObjectName("widget5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget5)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnNew = QtWidgets.QPushButton(self.widget5)
        self.btnNew.setMinimumSize(QtCore.QSize(70, 28))
        self.btnNew.setAutoDefault(False)
        self.btnNew.setObjectName("btnNew")
        self.horizontalLayout.addWidget(self.btnNew)
        self.btnDelete = QtWidgets.QPushButton(self.widget5)
        self.btnDelete.setMinimumSize(QtCore.QSize(70, 28))
        self.btnDelete.setAutoDefault(False)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout.addWidget(self.btnDelete)
        self.btnActions = QtWidgets.QPushButton(self.widget5)
        self.btnActions.setMinimumSize(QtCore.QSize(70, 28))
        self.btnActions.setAutoDefault(False)
        self.btnActions.setObjectName("btnActions")
        self.horizontalLayout.addWidget(self.btnActions)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.btnClose = QtWidgets.QPushButton(self.widget5)
        self.btnClose.setMinimumSize(QtCore.QSize(70, 28))
        self.btnClose.setAutoDefault(False)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.gridLayout.addWidget(self.widget5, 1, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.widget)
        self.actionResetLabels = QtWidgets.QAction(LabelEditorDialog)
        self.actionResetLabels.setObjectName("actionResetLabels")
        self.actionHide_all_labels = QtWidgets.QAction(LabelEditorDialog)
        self.actionHide_all_labels.setObjectName("actionHide_all_labels")
        self.actionHide_all_labels_in_3D_window = QtWidgets.QAction(LabelEditorDialog)
        self.actionHide_all_labels_in_3D_window.setObjectName("actionHide_all_labels_in_3D_window")
        self.actionShow_all_labels = QtWidgets.QAction(LabelEditorDialog)
        self.actionShow_all_labels.setObjectName("actionShow_all_labels")
        self.actionShow_all_labels_in_3D_window = QtWidgets.QAction(LabelEditorDialog)
        self.actionShow_all_labels_in_3D_window.setObjectName("actionShow_all_labels_in_3D_window")

        self.retranslateUi(LabelEditorDialog)
        QtCore.QMetaObject.connectSlotsByName(LabelEditorDialog)
        LabelEditorDialog.setTabOrder(self.lvLabels, self.inLabelDescription)
        LabelEditorDialog.setTabOrder(self.inLabelDescription, self.inRed)
        LabelEditorDialog.setTabOrder(self.inRed, self.inGreen)
        LabelEditorDialog.setTabOrder(self.inGreen, self.inBlue)
        LabelEditorDialog.setTabOrder(self.inBlue, self.inLabelId)
        LabelEditorDialog.setTabOrder(self.inLabelId, self.btnNew)
        LabelEditorDialog.setTabOrder(self.btnNew, self.btnDelete)
        LabelEditorDialog.setTabOrder(self.btnDelete, self.btnActions)
        LabelEditorDialog.setTabOrder(self.btnActions, self.btnClose)

    def retranslateUi(self, LabelEditorDialog):
        _translate = QtCore.QCoreApplication.translate
        LabelEditorDialog.setWindowTitle(_translate("LabelEditorDialog", "Segmentation Label Editor"))
        self.groupBox_3.setTitle(_translate("LabelEditorDialog", "可用的标签"))
        self.grpSelectedLabel.setTitle(_translate("LabelEditorDialog", "选择的标签"))
        self.label.setText(_translate("LabelEditorDialog", "描述"))
        self.label_2.setText(_translate("LabelEditorDialog", "颜色"))
        self.label_8.setText(_translate("LabelEditorDialog", "B:"))
        self.label_6.setText(_translate("LabelEditorDialog", "R:"))
        self.label_7.setText(_translate("LabelEditorDialog", "G:"))
        self.btnLabelColor.setText(_translate("LabelEditorDialog", "选择颜色"))
        self.groupBox_2.setTitle(_translate("LabelEditorDialog", "高级选项"))
        self.label_4.setText(_translate("LabelEditorDialog", "数值"))
        self.inLabelId.setToolTip(_translate("LabelEditorDialog", "The value that this label has in the segmentation image. If you change this value, voxels that have this value in the segmentation image will be changed to the new value."))
        self.btnNew.setText(_translate("LabelEditorDialog", "新建"))
        self.btnDelete.setText(_translate("LabelEditorDialog", "删除"))
        self.btnActions.setText(_translate("LabelEditorDialog", "高级"))
        self.btnClose.setText(_translate("LabelEditorDialog", "关闭"))
        self.actionResetLabels.setText(_translate("LabelEditorDialog", "Reset Label Descriptions"))
        self.actionResetLabels.setToolTip(_translate("LabelEditorDialog", "Restores label descriptions to the default values."))
        self.actionHide_all_labels.setText(_translate("LabelEditorDialog", "Hide all labels"))
        self.actionHide_all_labels_in_3D_window.setText(_translate("LabelEditorDialog", "Hide all labels in 3D window"))
        self.actionShow_all_labels.setText(_translate("LabelEditorDialog", "Show all labels"))
        self.actionShow_all_labels_in_3D_window.setText(_translate("LabelEditorDialog", "Show all labels in 3D window"))

