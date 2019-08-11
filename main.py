#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QSizePolicy
from PyQt5.QtGui import QIcon

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        
        self.files = [];
        self.LabelButtons = [];
        self.filenames = [];

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
        self.photo = QtWidgets.QLabel(self.MidColumn)
        # self.horizontalLayout_mid = QtWidgets.QHBoxLayout(self.MidColumn)
        # self.horizontalLayout_mid.addWidget(self.photo)
        
        # Set photo in Mid Column
        self.photo.setText("")
        myPixmap = QtGui.QPixmap('apple.jpg')
        myPixmap.scaled(self.photo.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        #self.photo.setScaledContents(True)
        self.photo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        self.photo.setPixmap(myPixmap)
        # self.photo.setAlignment(QtCore.Qt.AlignCenter)
        # self.MidColumn.setAlignment( QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter );
        # Move photo to the center
        vector = self.MidColumn.rect().center() - QtCore.QRect(QtCore.QPoint(), self.photo.sizeHint()).center()
        self.photo.move(vector)
        self.photo.setObjectName("photo")

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
        print(labelName)

    def ok_handler(self):
        language = 'None' if not self.line.text() else self.line.text()
        print('Favorite language: {}'.format(language))

    def files_open(self):
        names = QFileDialog.getOpenFileNames(self, 'Open File', ("Images (*.png *.jpg)"))
        print(names)
        file = open(names[0],'r')

        self.editor()

        with file:
            text = file.read()
            self.textEdit.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
