import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import threading

defaultTextBuffer = "def main():\n   input(0,('KEY_A',),0,0,0,0)\n   "
class Window(QMainWindow):
    def __init__(self,app):
        self.app = app
        super(Window, self).__init__()
        self.setWindowTitle('PyTAS Editor')
        self.dark = False
        self.screen_size = self.get_screen()[1]
        self.text_buffer = defaultTextBuffer
        self.setFixedSize(int(self.screen_size.width()), int(self.screen_size.height()))
        self.move(0,0)
        self.create_menu()
        self.create_layout()
        self.show()

    def create_layout(self):
        if self.dark:
            self.setStyleSheet("background-color: #282C34; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
        layout = self.layout()

        self.tabs = QTabWidget()
        Editor = QWidget()
        Functions = QWidget()
        self.tabs.resize(int(self.screen_size.width()), int(self.screen_size.height() - self.screen_size.height() / 10))
        self.tabs.move(0, int(self.screen_size.height() / 32))
        self.tabs.addTab(Editor,"Visual")
        self.tabs.addTab(Functions,"Programmatic")

        Editor.layout = QVBoxLayout()
        pushButton1 = QPushButton("Useless button... for NOW")
        pushButton1.setStyleSheet("background-color: #c7c5c6;")
        if self.dark:
            pushButton1.setStyleSheet("background-color: #171616; color: #ffffff;")
        Editor.layout.addWidget(pushButton1)
        Editor.setLayout(Editor.layout)

        Functions.layout = QVBoxLayout()
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Your code is here! The main() function is what's run.")
        self.code_input.textChanged.connect(self.prg_chng)
        self.code_input.setPlainText(self.text_buffer)
        self.code_input.setStyleSheet("background-color: #282C34; color: #ffffff;")
        if self.dark:
            self.code_input.setStyleSheet("background-color: #000000; color: #ffffff;")
        Functions.layout.addWidget(self.code_input)
        Functions.setLayout(Functions.layout)
        layout.addWidget(self.tabs)

    def create_menu(self):
        exit = QAction('&Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(self.exit)

        toggle = QAction('&Toggle Dark Mode', self)
        toggle.setShortcut('Ctrl+D')
        toggle.triggered.connect(self.toggle_view)

        tab1 = QAction('&Switch To Visual', self)
        tab1.setShortcut('Ctrl+1')
        tab1.triggered.connect(self.switch_tab1)
        tab2 = QAction('&Switch To Programmatic', self)
        tab2.setShortcut('Ctrl+2')
        tab2.triggered.connect(self.switch_tab2)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exit)
        editMenu = menubar.addMenu('&Edit')
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(toggle)
        viewMenu.addAction(tab1)
        viewMenu.addAction(tab2)
    def get_screen(self):
        self.screen = self.app.primaryScreen()
        return [self.screen.size(), self.screen.availableGeometry()]
    def prg_chng(self):
        if self.code_input.toPlainText() == defaultTextBuffer:
            return
        self.text_buffer = self.code_input.toPlainText()
    def toggle_view(self):
        self.dark = not self.dark
        self.create_layout()
    def switch_tab1(self):
        self.tabs.setCurrentIndex(0)
    def switch_tab2(self):
        self.tabs.setCurrentIndex(1)
    def exit(self):
        sys.exit("Closed app")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window(app)

    sys.exit(app.exec())
