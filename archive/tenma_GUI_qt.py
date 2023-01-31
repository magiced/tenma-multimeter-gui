import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar

class Window(QMainWindow):
    """ Main GUI Window """
    def __init__(self, parent=None):
        """ initialiser """
        super().__init__(parent)
        self.setWindowTitle('Tenma 72-2610 Serial Interface')
        self.setCentralWidget(QLabel("I'm a placeholder"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu('&Menu')
        self.menu.addAction('&Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage('COM PORT X')
        self.setStatusBar(status)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
