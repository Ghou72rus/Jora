# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_ip.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import ctypes
import sys
import threading
import imutils
import requests
import numpy as np
import cv2
from Jora import Jora

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 240)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 150, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 70, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 320, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(lambda: self.get_ip_and_port())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Подтвердить"))

    def get_ip_and_port(self):
        cam = Cam()
        cam.get_url("http://" + self.lineEdit.text().strip() + "/shot.jpg")
        cam.start()
        MainWindow.close()


class Cam(threading.Thread):
    def __init__(self):
        super().__init__()
        self.url = ""

    def run(self) -> None:
        self.connect_camera(self.url)

    def connect_camera(self, text):
        try:
            try:
                while True:
                    img_resp = requests.get(text)
                    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                    img = cv2.imdecode(img_arr, -1)
                    user32 = ctypes.windll.user32
                    img = imutils.resize(img, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
                    cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.imshow("Camera", img)
                    if cv2.waitKey(1) == 27:
                        cv2.destroyAllWindows()
                        break
            except cv2.error:
                jora.Speak("Доступ к камере утерян")
        except requests.exceptions.ConnectionError:
            jora.Speak("Не удается подключиться к камере")

    def get_url(self, url):
        self.url = url


if __name__ == '__main__':
    jora = Jora()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
