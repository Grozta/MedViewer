# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LabelEditorDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LabelEditorDialog(object):
    def setupUi(self, LabelEditorDialog):
        LabelEditorDialog.setObjectName("LabelEditorDialog")
        LabelEditorDialog.resize(644, 537)
        LabelEditorDialog.setStyleSheet("background-color:#3c3f41;\n"
"color: #f2f2f2;")
        self.gridLayout = QtWidgets.QGridLayout(LabelEditorDialog)
        self.gridLayout.setContentsMargins(6, 24, 6, 6)
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(16)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(LabelEditorDialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnNew = QtWidgets.QPushButton(self.widget)
        self.btnNew.setAutoDefault(False)
        self.btnNew.setObjectName("btnNew")
        self.horizontalLayout.addWidget(self.btnNew)
        self.btnDelete = QtWidgets.QPushButton(self.widget)
        self.btnDelete.setAutoDefault(False)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout.addWidget(self.btnDelete)
        self.btnActions = QtWidgets.QPushButton(self.widget)
        self.btnActions.setAutoDefault(False)
        self.btnActions.setObjectName("btnActions")
        self.horizontalLayout.addWidget(self.btnActions)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnClose = QtWidgets.QPushButton(self.widget)
        self.btnClose.setAutoDefault(False)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 3)
        self.grpSelectedLabel = QtWidgets.QGroupBox(LabelEditorDialog)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.widget_2 = QtWidgets.QWidget(self.grpSelectedLabel)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_6 = QtWidgets.QWidget(self.grpSelectedLabel)
        self.widget_6.setMinimumSize(QtCore.QSize(0, 100))
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_6)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.inGreen = QtWidgets.QSpinBox(self.widget_6)
        self.inGreen.setMaximumSize(QtCore.QSize(56, 16777215))
        self.inGreen.setMaximum(255)
        self.inGreen.setObjectName("inGreen")
        self.gridLayout_3.addWidget(self.inGreen, 1, 3, 1, 2)
        self.label_8 = QtWidgets.QLabel(self.widget_6)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 2, 1, 1)
        self.inBlue = QtWidgets.QSpinBox(self.widget_6)
        self.inBlue.setMaximumSize(QtCore.QSize(56, 16777215))
        self.inBlue.setMaximum(255)
        self.inBlue.setObjectName("inBlue")
        self.gridLayout_3.addWidget(self.inBlue, 2, 3, 1, 1)
        self.inRed = QtWidgets.QSpinBox(self.widget_6)
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
        spacerItem3 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 1, 1, 1, 1)
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
        self.btnLabelColor.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btnLabelColor.setObjectName("btnLabelColor")
        self.gridLayout_3.addWidget(self.btnLabelColor, 3, 2, 1, 2)
        self.verticalLayout_2.addWidget(self.widget_6)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
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
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.inLabelId = QtWidgets.QSpinBox(self.widget_4)
        self.inLabelId.setMinimumSize(QtCore.QSize(64, 0))
        self.inLabelId.setReadOnly(False)
        self.inLabelId.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inLabelId.setObjectName("inLabelId")
        self.horizontalLayout_4.addWidget(self.inLabelId)
        self.verticalLayout_6.addWidget(self.widget_4)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.gridLayout.addWidget(self.grpSelectedLabel, 0, 2, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(LabelEditorDialog)
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
        self.lvLabels.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lvLabels.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.lvLabels.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lvLabels.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.lvLabels.setObjectName("lvLabels")
        self.lvLabels.horizontalHeader().setVisible(False)
        self.lvLabels.horizontalHeader().setDefaultSectionSize(60)
        self.lvLabels.horizontalHeader().setStretchLastSection(True)
        self.lvLabels.verticalHeader().setVisible(False)
        self.lvLabels.verticalHeader().setDefaultSectionSize(25)
        self.verticalLayout.addWidget(self.lvLabels)
        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 1, 1)
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
        self.btnNew.setText(_translate("LabelEditorDialog", "New"))
        self.btnDelete.setText(_translate("LabelEditorDialog", "Delete"))
        self.btnActions.setText(_translate("LabelEditorDialog", "Actions..."))
        self.btnClose.setText(_translate("LabelEditorDialog", "Close"))
        self.grpSelectedLabel.setTitle(_translate("LabelEditorDialog", "Selected Label"))
        self.label.setText(_translate("LabelEditorDialog", "Description:"))
        self.label_2.setText(_translate("LabelEditorDialog", "Color:"))
        self.label_8.setText(_translate("LabelEditorDialog", "B:"))
        self.label_6.setText(_translate("LabelEditorDialog", "R:"))
        self.label_7.setText(_translate("LabelEditorDialog", "G:"))
        self.btnLabelColor.setText(_translate("LabelEditorDialog", "Choose..."))
        self.groupBox_2.setTitle(_translate("LabelEditorDialog", "Advanced Options:"))
        self.label_4.setText(_translate("LabelEditorDialog", "Numeric value:"))
        self.inLabelId.setToolTip(_translate("LabelEditorDialog", "The value that this label has in the segmentation image. If you change this value, voxels that have this value in the segmentation image will be changed to the new value."))
        self.groupBox_3.setTitle(_translate("LabelEditorDialog", "Available Labels:"))
        self.actionResetLabels.setText(_translate("LabelEditorDialog", "Reset Label Descriptions"))
        self.actionResetLabels.setToolTip(_translate("LabelEditorDialog", "Restores label descriptions to the default values."))
        self.actionHide_all_labels.setText(_translate("LabelEditorDialog", "Hide all labels"))
        self.actionHide_all_labels_in_3D_window.setText(_translate("LabelEditorDialog", "Hide all labels in 3D window"))
        self.actionShow_all_labels.setText(_translate("LabelEditorDialog", "Show all labels"))
        self.actionShow_all_labels_in_3D_window.setText(_translate("LabelEditorDialog", "Show all labels in 3D window"))
