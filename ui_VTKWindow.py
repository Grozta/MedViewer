# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_VTKWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VTKWindow(object):
    def setupUi(self, VTKWindow):
        VTKWindow.setObjectName("VTKWindow")
        VTKWindow.resize(463, 527)
        VTKWindow.setMouseTracking(True)
        VTKWindow.setStyleSheet("/*------------------------------------全局样式-----------------------------------------*/\n"
"QWidget{font: 12px;color:#DCDCDC;font-family:\'微软雅黑\';}\n"
"QFrame{border-radius:5px;}\n"
"/*QScrollBar*/\n"
"QScrollArea{border:none}\n"
"QScrollBar{border:none;background:transparent;}\n"
"QScrollBar::add-line:vertical {\n"
"background:none;\n"
"border:none;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"background:none;\n"
"border:none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical {\n"
"background:transparent;\n"
"border:none;\n"
"}\n"
"\n"
"QScrollBar::sub-page:vertical {\n"
"background:transparent;\n"
"border:none;\n"
"}\n"
"QScrollBar::add-page,QScrollBar::sub-page{background:transparent;}\n"
"QScrollBar::add-line,QScrollBar::sub-line { background: none; }\n"
"QScrollBar::handle{ background:rgba(91, 100, 116, 0.5); border-radius: 3px; width:4px;}\n"
"QScrollBar:vertical{width:8px;padding-left:1px;padding-right:1px;}\n"
"QScrollBar:horizontal{height:7px;padding-top:1px;padding-bottom:1px;}\n"
"QScrollBar::handle:vertical:hover { \n"
"border-radius: 3px;\n"
"background:#e6e6e6;\n"
"width:6px;\n"
"}\n"
"QScrollBar::handle:vertical:pressed {\n"
"border-radius: 3px;\n"
"background:#a5a5a5;\n"
"width:6px;\n"
"}\n"
"\n"
"QPushButton,QToolButton\n"
"{background:rgba(0,0,0,0); }\n"
"\n"
"\n"
"QScrollBar#verticalScrollBar{\n"
"background-color:qlineargradient(spread:pad,x1:0, y1:1, x2:1, y2:1,stop:0 #232323,stop:0.5 #121212,stop:1 #232323);\n"
"border-radius:3px;\n"
"border:1px solid #232323;}\n"
"\n"
"#renderWindow{\n"
"background-color:#000000;\n"
"border-radius:3px;\n"
"border:1px solid transparent;}\n"
"\n"
"#sliderWindow,#operatorWindow{\n"
"background-color:#000000;;border-radius:3px;}")
        self.verticalLayout = QtWidgets.QVBoxLayout(VTKWindow)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.renderWindow = QtWidgets.QWidget(VTKWindow)
        self.renderWindow.setMouseTracking(True)
        self.renderWindow.setObjectName("renderWindow")
        self.verticalLayout.addWidget(self.renderWindow)

        self.retranslateUi(VTKWindow)
        QtCore.QMetaObject.connectSlotsByName(VTKWindow)

    def retranslateUi(self, VTKWindow):
        _translate = QtCore.QCoreApplication.translate
        VTKWindow.setWindowTitle(_translate("VTKWindow", "Form"))

