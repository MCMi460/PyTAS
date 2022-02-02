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
editMenu = None
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

    def notice(self):
        notice = QMessageBox()

        notice.setText('Warning!\nChanging files using the editor may result in unwanted changes in your file.\nPlease make sure you keep a backup before you save any changes.')
        notice.setWindowTitle("Warning!")
        notice.exec_()

    def selfService(self):
        # Assign variables for use
        self.assign_variables()

        # Setup GUI components
        self.setup_window()
        self.create_menu()

        # A commonly-recurring function that pulls data from the buffer and writes it to the table
        self.fill_table()

        self.notice()

    def assign_variables(self):
        global fileMenu, editMenu, viewMenu
        fileMenu = self.menubar.addMenu('&File')
        editMenu = self.menubar.addMenu('&Edit')
        viewMenu = self.menubar.addMenu('&View')
        global textEdit, table, functionBox
        textEdit = self.tabWidget.findChild(QWidget,'tab2').findChild(QTextEdit,'textEdit')
        table = self.tabWidget.findChild(QWidget,'tab1').findChild(QTableWidget,'table')
        functionBox = self.tabWidget.findChild(QWidget,'tab1').findChild(QComboBox,'functionBox')

    def setup_window(self):
        # Window formatting
        self.MainWindow.setWindowTitle(f'PyTAS Editor v{version}')

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

        table.cellClicked.connect(self.tableUpdate)

        # Tabs event call
        self.tabWidget.currentChanged.connect(self.tabUpdate)

    def create_menu(self):
        saveFile = QAction('&Save File', self.MainWindow)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.askSave)
        fileMenu.addAction(saveFile)

        runFile = QAction('&Run Script', self.MainWindow)
        runFile.setShortcut('F5')
        runFile.triggered.connect(self.runFile)
        fileMenu.addAction(runFile)

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
        textEdit.textChanged.connect(self.textUpdate)
        textEdit.setPlainText(buffer)

    def fill_table(self):
        # Receive justified data of file from core.main
        global buffer, frames, functions, table, functionBox
        if 'from core.main' not in buffer:
            raise Exception('Invalid PyTAS file!')
        buff = buffer
        for line in buff.split('\n'):
            if '.run(' in line:
                buff = buff.replace(line,'')
        buff = f'{buff}\n'
        'from core.main import script\nscript = script()'
        fileEnvironment = {}
        exec(buff, fileEnvironment, None)
        print(buff)
        vals = fileEnvironment['script'].run(fileEnvironment['main'],output,True)
        # Begin interpreting functions
        functions = []
        for i in fileEnvironment:
            if i in ('__builtins__','script','main'):
                continue
            fileEnvironment['script'].__init__()
            f_vals = fileEnvironment['script'].run(fileEnvironment[i],output,True)
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
                item.valueChanged.connect(self.spinUpdate)
            else:
                item = QComboBox()
                item.addItems([ i['name'] for i in functions ])
                item.currentIndexChanged.connect(self.comboUpdate)
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

            item = QTableWidgetItem("X")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(n,17, item)
        # Fill programmatic tab
        self.fill_text()

    def sort_table(self):
        global table
        # Interpret table
        frames = []
        possible_frame = 1
        for i in range(1,table.rowCount()):
            val = table.cellWidget(i,0)
            if isinstance(val,QSpinBox):
                list = []
                for n in range(1,17):
                    if table.item(i,n).checkState() == Qt.Checked:
                        list.append(keys[n-1])
                key = ''
                for i in range(len(list)):
                    if i > 0:
                        key = f'{key};'
                    key = f'{key}{list[i]}'
                if key == '':
                    key = 'NONE'
                frame = val.value()
                print(possible_frame,frame)
                frames.append([False,{
                'Frame':frame,
                'Key':f'{key}',
                'LeftStick':'0;0',
                'RightStick':'0;0',
                'Caller':'main',
                }])
                if possible_frame < frame:
                    possible_frame = frame
                elif possible_frame == frame:
                    frames.pop()
            else:
                for n in functions:
                    if val.currentText() == n['name']:
                        l = n.copy()
                        l['Frame'] = possible_frame
                        frames.append([True,l])
                        possible_frame += l['frames']
                        break
        # Reorganize frames list
        def ex(elem):
            return int(elem[1]['Frame'])
        #for i in frames:
            #print(i[0])
            #for n in i[1]:
                #print(f'   {n}: {i[1][n]}')
        frames = sorted(frames,key=ex)
        last = 0
        # Make sure functions that start on the same frame as an input always go after
        for n in range(len(frames)):
            i = frames[n]
            if i[1]['Frame'] == last and not i[0]:
                i.insert(n - 1, l.pop(n))
        # Remove any frames that are placed inside of a function
        inp = False
        re = []
        for i in range(1,frames[-1][1]['Frame']+1):
            net = [ frame for frame in frames if frame[1]['Frame'] == i ]
            try:frame = next(frame for frame in frames if frame[1]['Frame'] == i)
            except:frame = None
            if len(net) == 0:
                continue
            elif len(net) == 1:
                if inp:
                    re.append(frame)
                if frame[0]:
                    inp = True
                else:
                    inp = False
            elif len(net) == 2:
                if frame[0]:
                    inp = True
                else:
                    inp = False
                continue
            else:
                raise Exception('Rare internal error: Too many inputs in a frame')
        for i in re:
            frames.remove(i)
        print([ i[1]['Frame'] for i in frames ])
        return frames

    def write_table(self, frames):
        # Interpret frames
        text = "# This is an auto-generated PyTAS file"
        lastframe = 0
        char = "'"
        for i in functions:
            text = f"{text}\ndef {i['name']}():\n"
            for n in i['data']:
                if n['Key'] != 'NONE' and ';' in n['LeftStick'] and ';' in n['RightStick']:
                    text = f"{text}    script.input({int(n['Frame']) - lastframe},({','.join([ f'{char}{h}{char}' for h in n['Key'].split(';') ])},),{','.join(n['LeftStick'].split(';'))},{','.join(n['RightStick'].split(';'))})\n"
                else:
                    text = f"{text}    script.wait({int(n['Frame']) - lastframe})"
                lastframe = int(n['Frame'])

        # Next, let's create main
        text = f"{text}\ndef main():\n"
        lastframe = 0
        for i in frames:
            if not i[0]:
                i = i[1]
                if i['Key'] != 'NONE' and ';' in i['LeftStick'] and ';' in i['RightStick']:
                    text = f"{text}    script.input({i['Frame'] - lastframe},({','.join([ f'{char}{h}{char}' for h in i['Key'].split(';') ])},),{','.join(i['LeftStick'].split(';'))},{','.join(i['RightStick'].split(';'))})\n"
                else:
                    text = f"{text}    script.wait({i['Frame'] - lastframe})\n"
                lastframe = i['Frame']
            else:
                i = i[1]
                text = f"{text}    {i['name']}()\n"
                lastframe += i['frames']
        if len(frames) == 0:
            text = f"{text}    pass"

        text = f"{text}\nfrom core.main import script\nscript = script()\nscript.run(main)\n"
        # Write to buffer
        global buffer
        buffer = text

    def removeRow(self, row):
        table.removeRow(row)
        self.row_count -= 1

    # Event-based functions
    def textUpdate(self):
        global buffer
        buffer = textEdit.toPlainText()

    def tableUpdate(self, row, col):
        if col == 17 and row != 0:
            self.removeRow(row)
        global table

        # Sort table, write changes
        self.write_table(self.sort_table())
        # Fill table
        self.fill_table()

    def spinUpdate(self):
        self.tableUpdate(0,0)

    def comboUpdate(self):
        self.tableUpdate(0,0)

    def tabUpdate(self):
        # Fill table
        self.fill_table()

    # QActions
    def runFile(self):
        exec(buffer, globals(), None)
        notice = QMessageBox()

        notice.setText('Process Success!')
        notice.setWindowTitle('Process Success!')
        notice.setDetailedText(f'File output written to \'{filename}\'')
        notice.exec_()

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
    output = 'script1'
    with open(filename,'r') as file:
        buffer = file.read()

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    window = GUI(MainWindow)
    window.setupUi(MainWindow)
    window.selfService()
    MainWindow.show()
    sys.exit(app.exec_())
