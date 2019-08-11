import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(widget)
        self.mdi = QtWidgets.QMdiArea(self)
        self.leftScroll = Pane(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, self)
        self.rightScroll = Pane(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, self)
        layout.addWidget(self.leftScroll)
        layout.addWidget(self.mdi)
        layout.addWidget(self.rightScroll)
        self.setCentralWidget(widget)
        for scroll in self.leftScroll, self.rightScroll:
            for index in range(4):
                widget = QtWidgets.QTextEdit()
                widget.setText('one two three four five')
                scroll.addWidget(widget)

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

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 300)
    window.show()
    sys.exit(app.exec_())