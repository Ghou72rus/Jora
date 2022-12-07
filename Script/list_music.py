# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import json
import sys

import pyttsx3
from PyQt5 import QtCore, QtGui, QtWidgets
from ctypes import *
from PyQt5.QtWidgets import QAbstractItemView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.WIGHT, self.HEIGHT = self.screen_size()
        MainWindow.resize(self.WIGHT, self.HEIGHT - 100)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setGeometry(QtCore.QRect(0, 0, self.WIGHT, self.HEIGHT - 100))
        self.listView.setStyleSheet("font: 12pt;")
        self.listView.setObjectName("listView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_name_window(self, name_window):
        self.NAME_WINDOW = name_window
        return self.NAME_WINDOW

    def set_name_window(self):
        return self.NAME_WINDOW

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.showFullScreen()
        MainWindow.setWindowTitle(_translate(self.set_name_window(), self.set_name_window()))

    def Print(self, list):
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        self.number = 0
        for radio in list:
            self.number += 1
            self.str = str(self.number) + ". " + radio[0]
            item = QtGui.QStandardItem(self.str)
            model.appendRow(item)

    def screen_size(self):
        self.HEIGHT = windll.user32.GetSystemMetrics(1)
        self.WIGHT = windll.user32.GetSystemMetrics(0)
        return self.WIGHT, self.HEIGHT


def Speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[3].id)
    engine.say(text)
    engine.runAndWait()


def Print_list(name_file):
    type_file = name_file.replace("../Files/", '')
    type_file = type_file.split(".")
    try:
        if type_file[0] == "music":
            with open(name_file, "r") as file:
                temp = json.load(file)
                array = [row['Name'] for row in temp["music"]]
            return array
    except FileNotFoundError:
        Speak("Список с музыкой не найден")
        sys.exit(0)


def main(name_file):
    import sys
    name_window = "Radio list"
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.get_name_window(name_window)
    ui.setupUi(MainWindow)
    ui.Print(Print_list(name_file))
    MainWindow.show()
    app.exec_()


if __name__ == '__main__':
    main("../Files/music.json")
