import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import threading

class Window(QMainWindow):
    def __init__(self,app):
        self.app = app
        super(Window, self).__init__()
        self.setWindowTitle('PyTAS Editor')
        self.dark = True
        if self.dark:
            self.setStyleSheet("background-color: #282C34; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.screen_size = self.get_screen()[1]
        self.setFixedSize(int(self.screen_size.width()), int(self.screen_size.height()))
        self.move(0,0)
        self.create_menu()
        self.create_layout()
        self.show()

    def create_layout(self):
        layout = self.layout()

        tabs = QTabWidget()
        Editor = QWidget()
        Functions = QWidget()
        tabs.resize(int(self.screen_size.width()), int(self.screen_size.height() - self.screen_size.height() / 10))
        tabs.move(0, int(self.screen_size.height() / 32))
        tabs.addTab(Editor,"Editor")
        tabs.addTab(Functions,"Functions")

        Editor.layout = QVBoxLayout()
        pushButton1 = QPushButton("PyQt5 button")
        pushButton1.setStyleSheet("background-color: #c7c5c6;")
        if self.dark:
            pushButton1.setStyleSheet("background-color: #000000; color: #ffffff;")
        Editor.layout.addWidget(pushButton1)
        Editor.setLayout(Editor.layout)

        Functions.layout = QVBoxLayout()
        textbox = QTextEdit()
        textbox.setStyleSheet("background-color: #282C34; color: #ffffff;")
        if self.dark:
            textbox.setStyleSheet("background-color: #000000; color: #ffffff;")
        Functions.layout.addWidget(textbox)
        Functions.setLayout(Functions.layout)
        layout.addWidget(tabs)

    def create_menu(self):
        exit = QAction('&Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(self.exit)

        toggle = QAction('&Toggle Dark Mode', self)
        toggle.setShortcut('Ctrl+D')
        toggle.triggered.connect(self.toggle_view)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exit)
        editMenu = menubar.addMenu('&Edit')
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(toggle)
    def get_screen(self):
        self.screen = self.app.primaryScreen()
        return [self.screen.size(), self.screen.availableGeometry()]
    def test(self):
        print('test!')
    def toggle_view(self):
        self.dark = not self.dark
    def exit(self):
        sys.exit("Closed app")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window(app)

    sys.exit(app.exec())
