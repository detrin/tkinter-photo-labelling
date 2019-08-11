from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QSizePolicy
import sys

filenames = []

class TestGui(QMainWindow):
    """ A Fast test gui show how to create buttons in a ScrollArea"""
    def __init__(self):
        super(TestGui, self).__init__()
        self.lay = QtWidgets.QHBoxLayout()
        self.sA = QtWidgets.QScrollArea()
        self.sA_lay = QtWidgets.QVBoxLayout()
        self.sA.setLayout(self.sA_lay)
        self.closeGui = QtWidgets.QPushButton("Close")
        self.add_file_button = QtWidgets.QPushButton("Add File")
        self.lay.addWidget(self.closeGui)
        self.lay.addWidget(self.add_file_button)
        self.lay.addWidget(self.sA)
        self.setLayout(self.lay)
        self.connect_()
        self.show()

    def connect_(self):
        self.add_file_button.clicked.connect(self.__add_file_to_list)
        self.closeGui.clicked.connect(self.close)
        return

    def __add_file_to_list(self):
        fname = QtGui.QFileDialog.getOpenFileName()
        global filenames
        filenames.append(fname)
        button = QtGui.QPushButton(fname)
        self.sA_lay.addWidget(button)
        return


if __name__ == '__main__':
     app = QApplication(sys.argv)
     tg = TestGui()
     sys.exit(app.exec_())