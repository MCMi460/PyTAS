import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import threading
from core.utility import *

defaultTextBuffer = """def roll_cancel():
    script.input(1,('KEY_B',),0,0,0,0)
    script.input(5,('KEY_ZL',),0,0,0,0)
    script.input(35,('KEY_ZL','KEY_Y',),0,0,0,0)
    script.input(2,('KEY_X','KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)

# Put your inputs here!
def main():
    for i in range(5):
        roll_cancel()
        script.wait(60)
    # All Python syntax should work!
"""
scriptRunBuffer = """from core.main import script
script = script()
script.run(main)"""
keys = (
'KEY_A',
'KEY_B',
'KEY_X',
'KEY_Y',
'KEY_LSTICK',
'KEY_RSTICK',
'KEY_L',
'KEY_R',
'KEY_ZL',
'KEY_ZR',
'KEY_PLUS',
'KEY_MINUS',
'KEY_DLEFT',
'KEY_DUP',
'KEY_DRIGHT',
'KEY_DDOWN',
)
defaultInputBuffer = """script.input(1,('NONE',),0,0,0,0)"""
class Window(QMainWindow):
    def __init__(self,app):
        self.app = app
        super(Window, self).__init__()
        self.setWindowTitle('PyTAS Editor')
        self.dark = True
        self.screen_size = self.get_screen()[1]
        self.setup_files()
        self.setFixedSize(int(self.screen_size.width()), int(self.screen_size.height()))
        self.move(0,0)
        self.create_menu()
        self.row_count = 1
        self.key_data = []
        self.frame_data = []
        self.create_layout()
        self.tabIndex = 0
        self.loadTableFromBuffer()
        self.show()

    def setup_files(self):
        self.text_buffer = defaultTextBuffer
        self.file_path = './script.py'
        try:
            self.file = File(self.file_path)
            self.file.set_buffer()
            self.text_buffer = self.file.read_buffer()
            self.text_buffer = self.text_buffer.replace(scriptRunBuffer,'')
            self.text_buffer = self.text_buffer.rstrip('\n')
        except Exception as e:
            error = QMessageBox()
            error.setText("A fatal error occured when opening your file.")
            error.setInformativeText(f"Try checking {self.file_path}'s directory for errors.")
            error.setWindowTitle("Error!")
            error.setDetailedText(f"{e}")
            error.exec_()
            self.file_path = None

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
        pushButton1 = QPushButton("Add Frame")
        pushButton1.clicked.connect(self.add_row)
        pushButton1.setStyleSheet("background-color: #c7c5c6;")
        if self.dark:
            pushButton1.setStyleSheet("background-color: #171616; color: #ffffff;")
        Editor.layout.addWidget(pushButton1)

        self.table = QTableWidget()

        self.table.setColumnCount(18)

        self.set_tableheaderLayout()

        vertHeader = self.table.verticalHeader()
        vertHeader.setVisible(False)

        header = self.table.horizontalHeader()
        header.setVisible(False)
        header.setDefaultAlignment(Qt.AlignCenter)
        #header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.clicked.connect(self.table_clicked)
        Editor.layout.addWidget(self.table)

        # Set editor layout. Don't screw with this one, Mi460
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

        runFile = QAction('&Run Script', self)
        runFile.setShortcut('F5')
        runFile.triggered.connect(self.runFile)

        saveFile = QAction('&Save File', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.askSave)

        toggle = QAction('&Toggle Light Mode', self)
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
        fileMenu.addAction(runFile)
        fileMenu.addAction(saveFile)
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
    def set_tableheaderLayout(self):
        self.table.setRowCount(self.row_count)
        self.table.setItem(0,0, QTableWidgetItem("Frame"))

        for i in range(len(self.frame_data)):
            self.table.setItem(i+1,0, QTableWidgetItem(str(self.frame_data[i])))

        self.table.setItem(0,17, QTableWidgetItem("Delete"))
        for i in range(len(keys)):
            self.table.setItem(0,i + 1, QTableWidgetItem(keys[i]))
        for i in range(1,17):
            for n in range(1,self.row_count):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                if self.key_data == []:
                    item.setCheckState(Qt.Unchecked)
                else:
                    try:
                        if keys[i - 1] in self.key_data[n - 1]:
                            item.setCheckState(Qt.Checked)
                        else:
                            raise Exception()
                    except:
                        item.setCheckState(Qt.Unchecked)
                self.table.setItem(n, i, item)
        for n in range(1,self.row_count):
            self.table.setItem(n,17, QTableWidgetItem("Delete"))
    def loadTableFromBuffer(self):
        self.set_tableheaderLayout()
        exec(self.text_buffer+'\n'+scriptRunBuffer.replace('script.run(main)',''), globals(), None)
        data = script.run(main,True).split('\n')
        data.remove('')
        self.row_count = len(data) + 1
        self.frame_data = []
        for i in range(len(data)):
            if data[i] == '':
                continue
            self.frame_data.append(data[i].split(' ')[0])
            _k = data[i].split(' ')[1].split(';')
            self.key_data.append(_k)
            #self.key_data.append()
        self.set_tableheaderLayout()
    def table_clicked(self, item):
        if item.column() == 17 and item.row() != 0:
            self.remove_row(item.row())
        self.key_data = []
        for i in range(1,self.table.rowCount()):
            _k = []
            for n in range(1,17):
                if self.table.item(i,n).checkState() == Qt.Checked:
                    _k.append(keys[n - 1])
            self.key_data.append(_k)
        self.set_tableheaderLayout()
    def add_row(self):
        self.row_count += 1
        self.set_tableheaderLayout()
    def remove_row(self,row):
        row -= 1
        self.table.removeRow(row)
        self.frame_data.pop(row)
        self.key_data.pop(row)
        self.row_count -= 1
    def toggle_view(self):
        self.dark = not self.dark
        self.tabIndex = self.tabs.currentIndex()
        self.create_layout()
        self.tabs.setCurrentIndex(self.tabIndex)
    def switch_tab1(self):
        self.tabs.setCurrentIndex(0)
    def switch_tab2(self):
        self.tabs.setCurrentIndex(1)
    def openCurrentFile(self):
        open_folder(self.file.file)
    def runFile(self):
        if self.text_buffer != self.file.read_buffer():
            if not self.askSave():
                return
        try:
            exec(self.text_buffer+'\n'+scriptRunBuffer.replace('script.run(main)',''), globals(), None)
            script.run(main)
        except Exception as e:
            error = QMessageBox()

            error.setText("A fatal error occured when running your script.")
            error.setInformativeText(f"Try running {self.file_path} as a standalone file.")
            error.setWindowTitle("Error!")
            error.setDetailedText(f"{e}")
            error.exec_()
            return
        try:
            open_folder('./output')
        except:
            pass
    def askSave(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Save file")
        dlg.setText("Would you like to save your current progress?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ans = dlg.exec()
        if ans == QMessageBox.Yes:
            self.file.write(self.text_buffer+'\n'+scriptRunBuffer)
            self.file.set_buffer()
            return True
        else:
            return False
    def exit(self):
        sys.exit("Closed app")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window(app)

    sys.exit(app.exec())
