#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget, QWidget

from Classification.load_img import Ui_Form
from util import get_base_dir

base_dir = get_base_dir()


class ClassifyWindow(QWidget, Ui_Form):
    def __init__(self, row_images, heat_maps, patient_class):
        super(ClassifyWindow, self).__init__()
        # self.setFixedSize()
        self.setupUi(self)
        self.setWindowTitle('肩袖损伤诊断')
        self.setWindowIcon(QIcon(os.path.join(base_dir, 'resources', 'HQU_logo1.png')))
        self.row_images = row_images
        self.heat_maps = heat_maps
        # image = cv2.imread(images[0])
        self.img1.setScaledContents(True)
        self.img3.setScaledContents(True)
        self.img1.setPixmap(QPixmap(row_images[0]))
        self.img3.setPixmap(QPixmap(heat_maps[0]))

        self.btn_last.clicked.connect(self.last_one)
        self.btn_next.clicked.connect(self.next_one)
        self.current_slice = 0
        if patient_class == '0':
            self.Dice_Wrist.setText('正常')
        else:
            self.Dice_Wrist.setText('撕裂')
        self.center()

    def center(self):
        """
        界面居中显示
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def next_one(self):
        if self.current_slice <= len(self.row_images) - 1:
            self.current_slice += 1
            if self.current_slice > len(self.row_images) - 1:
                self.current_slice = len(self.row_images) - 1
            self.img1.setPixmap(QPixmap(self.row_images[self.current_slice]))
            self.img3.setPixmap(QPixmap(self.heat_maps[self.current_slice]))
        else:
            self.current_slice -= 1

    def last_one(self):
        if self.current_slice >= 0:
            self.current_slice -= 1
            if self.current_slice < 0:
                self.current_slice = 0
            self.img1.setPixmap(QPixmap(self.row_images[self.current_slice]))
            self.img3.setPixmap(QPixmap(self.heat_maps[self.current_slice]))
        else:
            self.current_slice += 1

    def closeEvent(self, event):
        """
        关闭事件
        :param event: 事件
        """
        self.close()
