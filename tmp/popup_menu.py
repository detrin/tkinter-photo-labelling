import sys
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMenu



class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.lbl = QtGui.QLabel("Ubuntu", self)

        self.combo = QtGui.QComboBox(self)
        self.combo.setContextMenuPolicy(Qt.CustomContextMenu)
        self.combo.customContextMenuRequested.connect(self.showMenu)
        self.combo.addItem("Ubuntu")
        self.combo.addItem("Mandriva")
        self.combo.addItem("Fedora")
        self.combo.addItem("Red Hat")
        self.combo.addItem("Gentoo")

        self.combo.move(50, 50)
        self.lbl.move(50, 150)

        self.combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QComboBox')
        self.show()

    def showMenu(self,pos):
        menu = QMenu()
        clear_action = menu.addAction("Clear Selection")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == clear_action:
            self.combo.setCurrentIndex(0)

    def onActivated(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()