#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QSizePolicy
from PyQt5.QtGui import QIcon

class Pane(QtWidgets.QScrollArea):
    MinWidth = 186

    def __init__(self, alignment=0, parent=None):
        super().__init__(parent)
        self.mainWidget = QtWidgets.QWidget(self)
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.mainLayout.setAlignment(alignment)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setFixedWidth(Pane.MinWidth)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum,
                           QtWidgets.QSizePolicy.Ignored)
        self.setWidgetResizable(True)
        self.setWidget(self.mainWidget)
        self.verticalScrollBar().installEventFilter(self)
        
    def addWidget(self, widget):
        self.mainLayout.addWidget(widget)

    def removeWidget(self, widget):
        self.mainLayout.removeWidget(widget)

    def eventFilter(self, source, event):
        if isinstance(source, QtWidgets.QScrollBar):
            if event.type() == QtCore.QEvent.Show:
                self.setFixedWidth(Pane.MinWidth + source.width())
            elif event.type() == QtCore.QEvent.Hide:
                self.setFixedWidth(Pane.MinWidth)
        return super(Pane, self).eventFilter(source, event)

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        
        self.files = [];
        self.LabelButtons = [];

        self.initUI()
      
    def initUI(self):
        uic.loadUi('mainwindow_simple.ui', self)
        self.MidColumn = self.findChild(QtWidgets.QFrame, 'MidColumn')
        self.RightColumn = self.findChild(QtWidgets.QFrame, 'RightColumn')
        self.LabelAddButton = self.findChild(QtWidgets.QPushButton, 'LabelAddButton')
        self.LabelAddButton.clicked.connect(self.LabelAdd) 
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
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtWidgets.QVBoxLayout()

        # add all main to the main vLayout
        self.RightColumn.layout().addWidget(self.scrollArea)

        self.show()

    def LabelAdd(self):
        print(self.LabelTextLine.text())
        NewButtonName = self.LabelTextLine.text()
        self.LabelTextLine.setText("") 
        pushButton = QtWidgets.QPushButton(NewButtonName)
        pushButton.setGeometry(QtCore.QRect(10, 40+len(self.LabelButtons)*30, 151, 25))

        pushButton.setMinimumSize(QtCore.QSize(151, 25))
        pushButton.setMaximumSize(QtCore.QSize(151, 25))
        pushButton.setObjectName("LabelButton_"+str(len(self.LabelButtons)))
        #self.scrollAreaWidgetContents_2.layout().addWidget(pushButton)
        self.scrollLayout.addRow(pushButton)

        self.LabelButtons.append(NewButtonName)
        print(self.LabelButtons)

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
