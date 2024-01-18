# -*- coding: utf-8 -*-
from ui_MessageBox import Ui_MessageBox
import PyQt5.sip as sip
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSignal, pyqtSlot, QThread, QRect, QTimer,QPoint
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QWidget, QHBoxLayout, QApplication, \
    QTableWidgetItem, QLabel, QDialog, QProgressBar, QHeaderView, QMessageBox


class ThreadObject(QObject):
    sig_finished = pyqtSignal()
    def __init__(self, func=None):
        super(ThreadObject, self).__init__()
        #self.sig_finished = pyqtSignal()
        self.func = func

    @pyqtSlot()
    def run(self):
        if self.func:
            try:
                self.func()
            except Exception as e:
                print(e)
        self.sig_finished.emit()


class HQUMessageBox(QDialog):
    """
    自定义的message
    支持
    progress
    自定义图片
    自定义gif
    自定义按钮
    """
    # 仅支持这几个按键
    YES = 0x01
    NO = 0x02
    CANCEL = 0x04
    CLOSE = 0x08
    OK = 0x10
    ret_val = 0




    def __init__(self, parent, title, text, showCancle, showOK):

        super().__init__(parent)
        self.ui = Ui_MessageBox()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModal)
        self.setAttribute(Qt.WA_QuitOnClose, True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setParent(parent)
        # 模态对话框不能模态，是因为窗口属性没有分配（这里的Qt.Dialog一定要加）
        self.setWindowFlags(Qt.FramelessWindowHint |Qt.Dialog)
        self.ui.label_titel.setText(title)
        self.ui.label_context.setText(text)
        self.ui.label_titel_context.setText(text)
        self.ui.pushButton1.setVisible(showOK)
        self.ui.pushButton2.setVisible(showCancle)
        if not showCancle and not showOK:
            self.ui.widget_button.setVisible(False)

        self.setGeometry(self.parentWidget().pos().x(),self.parentWidget().pos().y(),parent.width(),parent.height())

        self.Margins = 5

        self.ui.pushButton1.clicked.connect(self.OK)
        self.ui.pushButton2.clicked.connect(self.cancle)
        self.ui.toolButton_close.clicked.connect(self.cancle)
        QApplication.processEvents()

    def progressValue(self, currentValue: int, rangeList: list = []):
        if len(range) == 2:
            minValue, maxValue = rangeList[0], rangeList[1]
            self.ui.progressBar.setRange(minValue, maxValue)
        self.ui.progressBar.setValue(currentValue)

    def OK(self):
        HQUMessageBox.ret_val = HQUMessageBox.YES
        self.close()

    def cancle(self):
        HQUMessageBox.ret_val = HQUMessageBox.CANCEL
        self.close()

    @staticmethod
    def question(parent, title, text, showCancle=True, showOK=True):
        box = HQUMessageBox(parent, title, text, showCancle, showOK)
        box.ui.stackedWidget.setCurrentWidget(box.ui.page_image)
        box.ui.label_image.setPixmap(QPixmap("resources/messageWarning.png"))
        box.exec_()
        return HQUMessageBox.ret_val

    @staticmethod
    def information(parent, title, text, showCancle=False, showOK=True):
        box = HQUMessageBox(parent, title, text, showCancle, showOK)
        box.ui.stackedWidget.setCurrentWidget(box.ui.page_image)
        box.ui.label_image.setPixmap(QPixmap("resources/messagePass.png"))
        box.exec_()

    @staticmethod
    def warning(parent, title, text, showCancle=False, showOK=True):
        box = HQUMessageBox(parent, title, text, showCancle, showOK)
        box.ui.stackedWidget.setCurrentWidget(box.ui.page_image)
        box.ui.label_image.setPixmap(QPixmap("resources/messageWarning.png"))
        box.exec_()

    @staticmethod
    def error(parent, title, text, showCancle=False, showOK=True):
        box = HQUMessageBox(parent, title, text, showCancle, showOK)
        box.ui.stackedWidget.setCurrentWidget(box.ui.page_image)
        box.ui.label_image.setPixmap(QPixmap("resources/messageFailed.png"))
        box.exec_()

    @staticmethod
    def progress(parent, title, text, currentValue: int, rangeList: list = []):
        box = HQUMessageBox(parent, title, text, False, False)
        box.progressValue(currentValue, rangeList)
        box.ui.stackedWidget.setCurrentWidget(box.ui.page_progress)
        box.setWindowModality(Qt.WindowModal)
        box.show()
        return box

    @staticmethod
    def status(parent, title, text, InThreadfunction:QObject = None):
        """
        title 标题
        text 显示的文本
        InThreadfunction 这里的在线程中函数对象，若存在就开线程
        返回值是messagebox对象
        """
        box = HQUMessageBox(parent, title, text, False, False)
        box.ui.stackedWidget.setCurrentWidget(box.ui.page_image)
        box.ui.toolButton_close.setVisible(False)
        box.ui.widget_bk.setStyleSheet("#widget_bk{border:1px solid #333946;border-top:0px;border-right:0px;border-left:0px;}")
        gifMoive = QMovie("resources/data_handing.gif")
        gifMoive.start()
        box.ui.label_image.setMovie(gifMoive)
        box.setWindowModality(Qt.WindowModal)
        if InThreadfunction is None:
            box.show()
        else:
            box.thread = QThread(parent)
            box.runableObj = ThreadObject(func = InThreadfunction)
            box.runableObj.moveToThread(box.thread)
            box.thread.started.connect(box.runableObj.run)
            #box.thread.started.connect(lambda :box.show())
            box.runableObj.sig_finished.connect(lambda :box.close())
            box.thread.start()
        QApplication.processEvents()
        return box



