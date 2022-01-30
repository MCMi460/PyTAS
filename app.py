from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from layout.layout import Ui_MainWindow
import core.main, sys, os, threading, random, time, math

version = core.main.version
# Now global variables for use
fileMenu = None
viewMenu = None
table = None
textEdit = None

class GUI(Ui_MainWindow):
    def __init__(self,MainWindow):
        self.MainWindow = MainWindow

    def selfService(self):
        self.assign_variables()

        self.setup_window()
        self.create_menu()

        self.fill_text()
        self.fill_table()

        #self.sidebar.findChild(QPushButton,'rewind_button').clicked.connect(self.rewind)

    def assign_variables(self):
        global fileMenu, viewMenu
        fileMenu = self.menubar.addMenu('&File')
        viewMenu = self.menubar.addMenu('&View')
        global textEdit, table
        textEdit = self.tabWidget.findChild(QWidget,'tab2').findChild(QTextEdit,'textEdit')

    def setup_window(self):
        self.MainWindow.setWindowTitle(f'PyTAS v{version}')

    def create_menu(self):
        saveFile = QAction('&Save File', self.MainWindow)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.askSave)
        fileMenu.addAction(saveFile)

        exit = QAction('&Quit', self.MainWindow)
        exit.setShortcut('Ctrl+Q')
        exit.triggered.connect(self.exit)
        fileMenu.addAction(exit)

        def switch_tab1():
            self.tabWidget.setCurrentIndex(0)
        tab1 = QAction('&Switch To Visual', self.MainWindow)
        tab1.setShortcut('Ctrl+1')
        tab1.triggered.connect(switch_tab1)
        def switch_tab2():
            self.tabWidget.setCurrentIndex(1)
        tab2 = QAction('&Switch To Programmatic', self.MainWindow)
        tab2.setShortcut('Ctrl+2')
        tab2.triggered.connect(switch_tab2)
        viewMenu.addAction(tab1)
        viewMenu.addAction(tab2)

    def fill_text(self):
        textEdit.textChanged.connect(self.textChanged)
        textEdit.setPlainText(buffer)

    def fill_table(self):
        # Receive justified data of file from core.main
        global buffer
        for line in buffer:
            if '.run(' in buffer:
                buffer.replace(line,'')
        buffer = f'{buffer}\n'
        'from core.main import script\nscript = script()'
        fileEnvironment = {}
        exec(buffer, fileEnvironment, None)
        vals = fileEnvironment['script'].run(fileEnvironment['main'],filename,True).split('\n')
        vals.remove('')
        # Begin interpreting functions
        # Clear table

        # Begin filling table

    # Event-based functions
    def textChanged(self):
        global buffer
        buffer = textEdit.toPlainText()
        # Call fill_table

    def askSave(self):
        dlg = QMessageBox()
        dlg.setWindowTitle("Save file")
        dlg.setText("Would you like to save your current progress?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ans = dlg.exec()
        if ans == QMessageBox.Yes:
            # Save file
            with open(filename,'w') as file:
                file.write(buffer)
            return True
        elif ans == QMessageBox.No:
            return False
        else:
            return None

    def exit(self):
        if self.askSave() is None:
            return
        sys.exit("Closed app")

if __name__ == '__main__':
    script = core.main.script()
    filename = './script.py'
    with open(filename,'r') as file:
        buffer = file.read()

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    window = GUI(MainWindow)
    window.setupUi(MainWindow)
    window.selfService()
    MainWindow.show()
    sys.exit(app.exec_())
