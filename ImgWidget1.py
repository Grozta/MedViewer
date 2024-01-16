#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class ImgWidget1(QLabel):

    def __init__(self, parent=None, index=0, color=None):
        self.visible_path = r'resources/icons8_invisible_12.png'
        self.invisible_path = r'resources/icons8_visible_12.png'

        super(ImgWidget1, self).__init__(parent)
        self.index = index  # 对应render的索引
        self.color = color
        self.open = True
        pic = QPixmap(self.invisible_path)
        self.setAlignment(Qt.AlignCenter)
        self.setPixmap(pic)

    def setPix(self):
        self.open = not self.open
        if not self.open:
            pic = QPixmap(self.visible_path)
            self.setPixmap(pic)
        else:
            pic = QPixmap(self.invisible_path)
            self.setPixmap(pic)

        # self.impAct1.setText(_translate("MainWindow", "top_left"))
        # self.impAct2.setText(_translate("MainWindow", "top_right"))
        # self.impAct3.setText(_translate("MainWindow", "bottom_left"))
        # self.impAct4.setText(_translate("MainWindow", "bottom_right"))
        # self.seg_rib.setText(_translate("MainWindow", "seg_rib"))
