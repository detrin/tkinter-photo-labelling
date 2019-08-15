#!/usr/bin/python
# This Python file uses the following encoding: utf-8
# pyuic5 mainwindow_simple.ui > tmp/mainwindow_simple.py
import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon, QPixmap

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        
        self.files = [];
        self.LabelButtons = [];
        self.fileNames = [];
        self.filenameUnused = [];
        self.currentFileName = "";
        self.LabelTable = [];

        self.initUI()
      
    def initUI(self):
        uic.loadUi('mainwindow_simple.ui', self)
        self.MidColumn = self.findChild(QtWidgets.QFrame, 'MidColumn')
        self.RightColumn = self.findChild(QtWidgets.QFrame, 'RightColumn')
        self.LabelAddButton = self.findChild(QtWidgets.QPushButton, 'LabelAddButton')
        self.LabelAddButton.clicked.connect(self.LabelAdd) 
        # Add label shortcut
        QtWidgets.QShortcut(QtCore.Qt.Key_Enter, self.LabelAddButton, self.LabelAdd)
        QtWidgets.QShortcut(QtCore.Qt.Key_Return, self.LabelAddButton, self.LabelAdd)
        self.LabelTextLine = self.findChild(QtWidgets.QLineEdit, 'LabelTextLine')
        # self.LabelsArea = self.findChild(QtWidgets.QScrollArea, 'LabelsArea')
        # self.scrollAreaWidgetContents_2 = self.findChild(QtWidgets.QWidget, 'scrollAreaWidgetContents_2')

        # Menu setup
        self.actionOpen_files.setShortcut("Ctrl+O")
        self.actionOpen_files.triggered.connect(self.files_open)

        # Frame for a picture setup
        self.photo == self.findChild(QtWidgets.QLabel, 'photo')
        # self.horizontalLayout_mid = QtWidgets.QHBoxLayout(self.MidColumn)
        # self.horizontalLayout_mid.addWidget(self.photo)
        
        # Set photo in Mid Column
        self.photo.setText("")
        self.currentFileName = 'apple.jpg'
        self.setImage()

        # scroll area widget contents - layout
        self.scrollLayout = QtWidgets.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtWidgets.QVBoxLayout()

        # add all main to the main vLayout
        self.RightColumn.layout().addWidget(self.scrollArea)

        self.show()

    def LabelAdd(self):
        NewButtonName = self.LabelTextLine.text()
        if NewButtonName.strip() != "":
            self.LabelTextLine.setText("") 
            
            pushButton = QtWidgets.QPushButton(NewButtonName)
            pushButton.clicked.connect(partial(self.LabelPicture, labelName=NewButtonName))
            pushButton.setGeometry(QtCore.QRect(10, 40+len(self.LabelButtons)*30, 151, 25))

            # pushButton.setMinimumSize(QtCore.QSize(151, 25))
            # pushButton.setMaximumSize(QtCore.QSize(151, 25))
            pushButton.setObjectName("LabelButton_"+str(len(self.LabelButtons)))
            pushButton.labelName = NewButtonName
            
            self.scrollLayout.addRow(pushButton)
            
            self.LabelButtons.append(NewButtonName)
            print(self.LabelButtons)
    
    def LabelPicture(self, labelName):
        self.LabelTable.append([self.currentFileName, labelName])
        if len(self.filenameUnused) > 1:
            self.currentFileName = self.filenameUnused[0]
            self.filenameUnused.pop(0)
            self.setImage()
        else:
            self.currentFileName = "apple.jpg"
            self.photo = None
    
    def setImage(self):
        #self.photo.clear()
        #self.photo = QLabel(self.MidColumn)
        image = QtGui.QImage(self.currentFileName)
        ratio = 1
        w_max = self.MidColumn.frameGeometry().width()*ratio
        h_max = self.MidColumn.frameGeometry().height()*ratio
        pp = QtGui.QPixmap.fromImage(image)
        w = pp.size().width()
        h = pp.size().height()
        if (w < w_max or h < h_max):
            self.photo.setPixmap(pp.scaled(
                        h, w,
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation))
        else:
            self.photo.setPixmap(pp.scaled(
                        h_max, w_max,
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation))
        #self.photo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)        

    def files_open(self):
        names = QFileDialog.getOpenFileNames(self, 'Open File', ("Images (*.png *.jpg)"))
        print(names)
        self.fileNames = names[0]
        self.currentFileName = names[0][0]
        if len(names) > 1:
            self.filenameUnused = names[0][1:]
        print(self.fileNames)
        print(self.currentFileName)
        self.setImage()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
