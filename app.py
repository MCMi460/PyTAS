from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from layout.layout import Ui_MainWindow
import core.main, sys, os, threading, random, time, math

version = core.main.version
keys = list(core.main.script().keys)
keys.pop(0)
keys = tuple(keys)
# Global variables for use
# -Qt Stuff
fileMenu = None
viewMenu = None
textEdit = None
table = None
functionBox = None
# -PyTAS stuff
frames = []
functions = []

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
        global textEdit, table, functionBox
        textEdit = self.tabWidget.findChild(QWidget,'tab2').findChild(QTextEdit,'textEdit')
        table = self.tabWidget.findChild(QWidget,'tab1').findChild(QTableWidget,'table')
        functionBox = self.tabWidget.findChild(QWidget,'tab1').findChild(QComboBox,'functionBox')

    def setup_window(self):
        # Window formatting
        self.MainWindow.setWindowTitle(f'PyTAS v{version}')

        # Function box formatting
        functionBox.clear()
        functionBox.addItem('main')

        # Table formatting
        self.row_count = 1
        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setSectionResizeMode(QHeaderView.Stretch)

        table.setRowCount(self.row_count)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        item = QTableWidgetItem("Frame")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        table.setItem(0,0, item)

        item = QTableWidgetItem("<>")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(0,17, item)
        for i in range(len(keys)):
            item = QTableWidgetItem(keys[i])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(0,i + 1, item)

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
        global buffer, frames, functions, table, functionBox
        buff = buffer
        for line in buff.split('\n'):
            if '.run(' in line:
                buff = buff.replace(line,'')
        buff = f'{buff}\n'
        'from core.main import script\nscript = script()'
        fileEnvironment = {}
        exec(buff, fileEnvironment, None)
        vals = fileEnvironment['script'].run(fileEnvironment['main'],filename,True)
        # Begin interpreting functions
        functions = []
        for i in fileEnvironment:
            if i in ('__builtins__','script','main'):
                continue
            fileEnvironment['script'].__init__()
            f_vals = fileEnvironment['script'].run(fileEnvironment[i],filename,True)
            functions.append({
            'name':i,
            'data':f_vals,
            'frames':f_vals[-1]['Frame'],
            'length':len(f_vals),
            })
        # Begin interpreting main
        frames = []
        n = 0
        while n < len(vals):
            i = vals[n]
            if i['Caller'] not in ('main','wait'):
                n += next(n for n in functions if n['name'] == i['Caller'])['length']
                frames.append([True,i['Caller']])
            else:
                frames.append([False,i])
                n += 1
        # Clear functionBox
        functionBox.clear()
        # Begin filling functionBox
        functionBox.addItem('main')
        functionBox.addItems([ i['name'] for i in functions ])
        # Clear table
        self.row_count = 1
        table.setRowCount(self.row_count)
        # Begin filling table
        self.row_count += len(frames)
        table.setRowCount(self.row_count)
        for n in range(1,len(frames) + 1):
            i = frames[n - 1]

            if not i[0]:
                item = QSpinBox()
                item.setMinimum(0)
                item.setMaximum(999999)
                item.setValue(i[1]['Frame'])
            else:
                item = QComboBox()
                item.addItems([ i['name'] for i in functions ])
            table.setCellWidget(n, 0, item)

            for j in range(16):
                item = QTableWidgetItem()
                if not i[0]:
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if keys[j] in i[1]['Key'].split(';'):
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                else:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table.setItem(n, j + 1, item)

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
