#!/usr/bin/python
# This Python file uses the following encoding: utf-8
# pyuic5 mainwindow_simple.ui > tmp/mainwindow_simple.py
import sys
import pickle
import dill
import sip
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QSizePolicy, QLabel, QListWidget, QMenu, QInputDialog, QShortcut, qApp
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSettings

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.settings = QSettings("gui.ini", QSettings.IniFormat)
        self.files = []
        self.LabelButtons = {}
        self.LabelButtonsShortcuts = {}
        self.LabelButtonsShortcutsNames = {}
        self.fileNames = []
        self.filenameUnused = []
        self.currentFileName = ""
        self.LabelTable = []

        self.initUI()
      
    def initUI(self):
        uic.loadUi('mainwindow_simple.ui', self)
        self.MidColumn = self.findChild(QtWidgets.QFrame, 'MidColumn')
        self.RightColumn = self.findChild(QtWidgets.QFrame, 'RightColumn')
        self.LabelAddButton = self.findChild(QtWidgets.QPushButton, 'LabelAddButton')
        self.LabelAddButton.clicked.connect(self.labelAdd) 
        # Add label shortcut
        QtWidgets.QShortcut(Qt.Key_Enter, self.LabelAddButton, self.labelAdd)
        QtWidgets.QShortcut(Qt.Key_Return, self.LabelAddButton, self.labelAdd)
        self.LabelTextLine = self.findChild(QtWidgets.QLineEdit, 'LabelTextLine')
        # self.LabelsArea = self.findChild(QtWidgets.QScrollArea, 'LabelsArea')
        # self.scrollAreaWidgetContents_2 = self.findChild(QtWidgets.QWidget, 'scrollAreaWidgetContents_2')

        # Menu setup
        self.actionOpen_files.setShortcut("Ctrl+O")
        self.actionOpen_files.triggered.connect(self.files_open)
        self.actionOpen_session.triggered.connect(self.openSession)
        self.actionSave_session.triggered.connect(self.saveSession)
        self.actionSave_csv_file.setShortcut("Ctrl+S")
        self.actionSave_csv_file.triggered.connect(self.saveCSVfile)

        # Frame for a picture setup
        self.photo == self.findChild(QtWidgets.QLabel, 'photo')
        # self.horizontalLayout_mid = QtWidgets.QHBoxLayout(self.MidColumn)
        # self.horizontalLayout_mid.addWidget(self.photo)
        
        # Set photo in Mid Column
        self.photo.setText("")
        #self.currentFileName = 'apple.jpg'
        #self.setImage()

        # scroll area widget contents - layout
        self.scrollLayout = QtWidgets.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtWidgets.QVBoxLayout()

        # add all main to the main vLayout
        self.RightColumn.layout().addWidget(self.scrollArea)

        self.show()

    def labelAdd(self):
        NewButtonName = self.LabelTextLine.text()
        if NewButtonName.strip() != "":
            self.LabelTextLine.setText("") 

            pushButton = QtWidgets.QPushButton(NewButtonName)
            pushButton.clicked.connect(partial(self.labelPicture, labelName=NewButtonName))
            pushButton.setGeometry(QtCore.QRect(10, 40+len(self.LabelButtons)*30, 151, 25))

            pushButton.setObjectName("LabelButton_"+str(len(self.LabelButtons)))
            pushButton.labelName = NewButtonName                                         

            pushButton.setContextMenuPolicy(Qt.CustomContextMenu)
            pushButton.customContextMenuRequested.connect(partial(self.rightClickFunction, labelName=NewButtonName))
            pushButton.action_1 = QAction()
            pushButton.action_1.setObjectName('remove_button')                      
            pushButton.action_1.setText('Remove')

            pushButton.action_2 = QAction()
            pushButton.action_2.setObjectName('add_shortcut')                   
            pushButton.action_2.setText('Set shortcut')  
                
            pushButton.customMenu = QMenu('Menu', pushButton)       
            pushButton.customMenu.addAction(pushButton.action_1)
            pushButton.customMenu.addAction(pushButton.action_2)
            
            pushButton.action_1.triggered.connect(partial(self.removeButton, labelName=NewButtonName))
            pushButton.action_2.triggered.connect(partial(self.add_shortcut, labelName=NewButtonName))

            self.LabelButtonsShortcutsNames[NewButtonName] = "Ctrl+"+str(len(self.LabelButtons)+1)
            self.scrollLayout.addRow(pushButton)
            self.LabelButtons[NewButtonName] = pushButton


    def rightClickFunction(self, labelName) :
        pushButton = self.LabelButtons[labelName]
        pushButton.customMenu.popup(QtGui.QCursor.pos()) 

    def removeButton(self, labelName):
        pushButton = self.LabelButtons[labelName]
        pushButton.setParent(None)
        #self.LabelButtons[labelName] = None
        #del self.LabelButtons[labelName]

    def add_shortcut(self, labelName):
        text, result = QInputDialog.getText(self, 'Add shortcut', 'Enter new shortcut:', text=self.LabelButtonsShortcutsNames[labelName])
        pushButton = self.LabelButtons[labelName]
        if result:
            self.LabelButtonsShortcuts[labelName] = QShortcut(QtGui.QKeySequence(str(text)), pushButton)
            self.LabelButtonsShortcuts[labelName].activated.connect(partial(self.labelPicture, labelName=labelName)) 

    def labelPicture(self, labelName):
        self.LabelTable.append([self.currentFileName, labelName])
        if len(self.filenameUnused) > 1:
            self.currentFileName = self.filenameUnused[0]
            self.filenameUnused.pop(0)
            self.setImage()
        else:
            self.clearImage();
            self.currentFileName = "apple.jpg"
            #self.photo = None
    
    def setImage(self):
        #self.photo.clear()
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
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation))
        else:
            self.photo.setPixmap(pp.scaled(
                        h_max, w_max,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation))
        #self.photo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)   

    def openSession(self):
        names = QFileDialog.getOpenFileName(self, 'Open session', ("Session file (*.lbl);;All Files (*)"))
        sessionFile = names[0]
        with open(sessionFile, 'rb') as handle:
            intern_vars = pickle.load(handle)
        self.files,
        self.LabelButtons,
        self.LabelButtonsShortcuts,
        self.LabelButtonsShortcutsNames,
        self.fileNames,
        self.filenameUnused,
        self.currentFileName,
        self.LabelTable = intern_vars
        partial(self.guirestore, settings=self.settings)
    
    def saveSession(self):
        names = QFileDialog.getSaveFileName(self, 'Save session')
        sessionFile = names[0]
        self.guisave()
        intern_vars = [
            self.files,
            self.LabelButtons,
            self.LabelButtonsShortcuts,
            self.LabelButtonsShortcutsNames,
            self.fileNames,
            self.filenameUnused,
            self.currentFileName,
            self.LabelTable
        ]
        with open(sessionFile, 'wb') as handle:
            pickle.dump(intern_vars, handle)

    def guisave(self):
        #settings = QSettings("gui.ini", QSettings.IniFormat)
        for w in qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "":
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    self.settings.setValue("{}/{}".format(w.objectName(), name), w.property(name))

    def guirestore(self, settings):
        for w in qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "":
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    val = self.settings.value("{}/{}".format(w.objectName(), name), w.property(name))
                    w.setProperty(name, val)

    def clearImage(self):
        self.photo.clear()

    def files_open(self):
        names = QFileDialog.getOpenFileNames(self, 'Open file', ("Images (*.png *.jpg);;All Files (*)"))

        self.fileNames = names[0]
        self.currentFileName = names[0][0]
        if len(names) > 1:
            self.filenameUnused = names[0][1:]

        self.setImage()
    
    def saveCSVfile(self):
        names = QFileDialog.getSaveFileName(self, 'Save CSV file')
        with open(names[0], 'w') as f:
            for row in self.LabelTable:
                f.write(";".join(row)+"\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
