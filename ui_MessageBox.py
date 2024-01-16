# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_MessageBox.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MessageBox(object):
    def setupUi(self, MessageBox):
        MessageBox.setObjectName("MessageBox")
        MessageBox.setWindowModality(QtCore.Qt.NonModal)
        MessageBox.resize(664, 642)
        MessageBox.setMouseTracking(True)
        MessageBox.setStyleSheet("\n"
"/*------------------------------------全局样式-----------------------------------------*/\n"
"QWidget{font: 12px;color:#DCDCDC;font-family:\'微软雅黑\';}\n"
"QFrame{border-radius:5px;}\n"
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
"/*--------------------------------------特征样式---------------------------------------*/\n"
"#widget{background-color:qlineargradient(spread:pad,x1:0, y1:0, x2:0, y2:1,stop:0.7 #232323, stop:1 #121212 );border-radius:5px;}\n"
"#titel>QWidget{color:#DCDCDC;font:12pt;}\n"
"\n"
"#toolButton_close:hover\n"
"{border-bottom-color:rgba(196,43,28,0.5);\n"
"background-color:rgba(196,43,28,0.2);border-radius: 3px;}\n"
"\n"
"#widget_button{\n"
"background:transparent;\n"
"border:1px solid #333946;\n"
"border-right:0px;\n"
"border-left:0px;\n"
"border-bottom:0px;}\n"
"\n"
"#progressBar{ \n"
"    border-radius:5px;\n"
"    border-top:1px;         \n"
"    background-color:#2764c1;\n"
"    qproperty-textVisible:false;\n"
"}\n"
"#pushButton1{background:#2764c1;color:#DCDCDC;}\n"
"#pushButton1:hover{background:#4e9cd5;}\n"
"#widget_dark{background:rgba(0,0,0,0.4);}\n"
"")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(MessageBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_dark = QtWidgets.QWidget(MessageBox)
        self.widget_dark.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_dark.setObjectName("widget_dark")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_dark)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.widget = QtWidgets.QWidget(self.widget_dark)
        self.widget.setMinimumSize(QtCore.QSize(462, 205))
        self.widget.setMaximumSize(QtCore.QSize(462, 205))
        self.widget.setMouseTracking(True)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titel = QtWidgets.QWidget(self.widget)
        self.titel.setMinimumSize(QtCore.QSize(0, 22))
        self.titel.setMaximumSize(QtCore.QSize(16777215, 50))
        self.titel.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.titel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.titel.setObjectName("titel")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.titel)
        self.horizontalLayout_2.setContentsMargins(6, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_titel = QtWidgets.QLabel(self.titel)
        self.label_titel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_titel.setAutoFillBackground(False)
        self.label_titel.setScaledContents(False)
        self.label_titel.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titel.setObjectName("label_titel")
        self.horizontalLayout_2.addWidget(self.label_titel)
        spacerItem1 = QtWidgets.QSpacerItem(341, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.toolButton_close = QtWidgets.QToolButton(self.titel)
        self.toolButton_close.setMinimumSize(QtCore.QSize(30, 0))
        self.toolButton_close.setMaximumSize(QtCore.QSize(30, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/btn_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_close.setIcon(icon)
        self.toolButton_close.setObjectName("toolButton_close")
        self.horizontalLayout_2.addWidget(self.toolButton_close)
        self.verticalLayout.addWidget(self.titel)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_progress = QtWidgets.QWidget()
        self.page_progress.setObjectName("page_progress")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.page_progress)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(18, 30, 18, 18)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.progressBar = QtWidgets.QProgressBar(self.page_progress)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.label_titel_context = QtWidgets.QLabel(self.page_progress)
        self.label_titel_context.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_titel_context.setAutoFillBackground(False)
        self.label_titel_context.setScaledContents(False)
        self.label_titel_context.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titel_context.setWordWrap(True)
        self.label_titel_context.setObjectName("label_titel_context")
        self.verticalLayout_3.addWidget(self.label_titel_context)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.stackedWidget.addWidget(self.page_progress)
        self.page_image = QtWidgets.QWidget()
        self.page_image.setObjectName("page_image")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.page_image)
        self.horizontalLayout_5.setContentsMargins(0, 26, 0, 26)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_bk = QtWidgets.QWidget(self.page_image)
        self.widget_bk.setObjectName("widget_bk")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_bk)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.label_image = QtWidgets.QLabel(self.widget_bk)
        self.label_image.setMinimumSize(QtCore.QSize(50, 50))
        self.label_image.setMaximumSize(QtCore.QSize(50, 50))
        self.label_image.setText("")
        self.label_image.setPixmap(QtGui.QPixmap("resources/messageFailed.png"))
        self.label_image.setScaledContents(True)
        self.label_image.setObjectName("label_image")
        self.horizontalLayout_6.addWidget(self.label_image)
        spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.label_context = QtWidgets.QLabel(self.widget_bk)
        self.label_context.setScaledContents(True)
        self.label_context.setWordWrap(True)
        self.label_context.setObjectName("label_context")
        self.horizontalLayout_6.addWidget(self.label_context)
        self.horizontalLayout_5.addWidget(self.widget_bk)
        self.stackedWidget.addWidget(self.page_image)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.widget_button = QtWidgets.QWidget(self.widget)
        self.widget_button.setObjectName("widget_button")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_button)
        self.horizontalLayout.setContentsMargins(3, 8, 3, 3)
        self.horizontalLayout.setSpacing(18)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.pushButton2 = QtWidgets.QPushButton(self.widget_button)
        self.pushButton2.setMinimumSize(QtCore.QSize(70, 28))
        self.pushButton2.setObjectName("pushButton2")
        self.horizontalLayout.addWidget(self.pushButton2)
        self.pushButton1 = QtWidgets.QPushButton(self.widget_button)
        self.pushButton1.setMinimumSize(QtCore.QSize(70, 28))
        self.pushButton1.setObjectName("pushButton1")
        self.horizontalLayout.addWidget(self.pushButton1)
        self.verticalLayout.addWidget(self.widget_button)
        self.horizontalLayout_4.addWidget(self.widget)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addWidget(self.widget_dark)

        self.retranslateUi(MessageBox)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MessageBox)

    def retranslateUi(self, MessageBox):
        _translate = QtCore.QCoreApplication.translate
        MessageBox.setWindowTitle(_translate("MessageBox", "Form"))
        self.label_titel.setText(_translate("MessageBox", "程序关闭"))
        self.toolButton_close.setText(_translate("MessageBox", "x"))
        self.label_titel_context.setText(_translate("MessageBox", "您即将关闭应用程序，确定退出吗？"))
        self.label_context.setText(_translate("MessageBox", "您即将关闭应用程序，确定退出吗？"))
        self.pushButton2.setText(_translate("MessageBox", "取消"))
        self.pushButton1.setText(_translate("MessageBox", "确定"))

