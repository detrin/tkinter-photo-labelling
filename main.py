#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit
from PySide2.QtCore import QFile, QObject
from PyQt5 import QtCore, QtGui, QtWidgets, uic

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

class Main(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        uic.loadUi('mainwindow_simple.ui', self)
        self.MidColumn = self.findChild(QtWidgets.QFrame, 'MidColumn')
        self.RightColumn = self.findChild(QtWidgets.QFrame, 'RightColumn')
        self.LabelAddButton = self.findChild(QtWidgets.QPushButton, 'LabelAddButton')
        self.LabelAddButton.clicked.connect(self.LabelAdd) 

        self.show()

    def LabelAdd(self):
        print('LabelAddButton')

    def ok_handler(self):
        language = 'None' if not self.line.text() else self.line.text()
        print('Favorite language: {}'.format(language))

    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileNames(self, 'Open File')
        file = open(name,'r')

        self.editor()

        with file:
            text = file.read()
            self.textEdit.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
