from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from layout.layout import Ui_MainWindow
import core.main, sys, random, math, inspect, re

version = core.main.version
keys = list(core.main.script().keys)
keys.pop(0)
keys = tuple(keys)
# Global variables for use
# -Qt Stuff
height = 0
width = 0
fileMenu = None
editMenu = None
viewMenu = None
textEdit = None
table = None
functionBox = None
addFrame = None
addFunction = None
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

        # Open file
        self.openFile()

    def assign_variables(self):
        global fileMenu, editMenu, viewMenu
        fileMenu = self.menubar.addMenu('&File')
        editMenu = self.menubar.addMenu('&Edit')
        viewMenu = self.menubar.addMenu('&View')
        global textEdit, table, functionBox, addFrame, addFunction
        textEdit = self.tabWidget.findChild(QWidget,'tab2').findChild(QTextEdit,'textEdit')
        table = self.tabWidget.findChild(QWidget,'tab1').findChild(QTableWidget,'table')
        functionBox = self.tabWidget.findChild(QWidget,'tab1').findChild(QComboBox,'functionBox')
        addFrame = self.tabWidget.findChild(QWidget,'tab1').findChild(QPushButton,'addFrame')
        addFunction = self.tabWidget.findChild(QWidget,'tab1').findChild(QPushButton,'addFunction')
        # Actions
        self.MainWindow.closeEvent = self.closeEvent

    def setup_window(self):
        global height, width
        # Window formatting
        screen = app.primaryScreen()
        size = screen.availableGeometry()
        height = int(size.height())
        width = int(size.width())
        self.MainWindow.setWindowTitle(f'PyTAS Editor v{version}')
        self.MainWindow.setFixedSize(width, height)
        self.MainWindow.showMaximized()

        # Function box formatting
        functionBox.clear()
        functionBox.addItem('main')

        # Tabs formatting
        self.tabWidget.setGeometry(QRect(0, 0, int(width), int(height - 20)))

        self.tabWidget.currentChanged.connect(self.tabUpdate)

        # Table formatting
        table.setGeometry(QRect(int(width / 130), int(height / 23), int(width - width / 45), int(height - height / 7)))
        self.row_count = 1
        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setSectionResizeMode(QHeaderView.Stretch)

        table.setRowCount(self.row_count)
        table.setColumnCount(len(keys) + 4)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        item = QTableWidgetItem("Frame")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        table.setItem(0,0, item)

        item = QTableWidgetItem("L-Stick")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(0,1, item)
        item = QTableWidgetItem("R-Stick")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(0,2, item)
        item = QTableWidgetItem("<>")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(0,len(keys) + 3, item)
        for i in range(len(keys)):
            item = QTableWidgetItem(keys[i].replace('KEY_',''))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(0,i + 3, item)

        table.cellClicked.connect(self.tableUpdate)

        # Buttons formatting
        addFrame.setGeometry(QRect(int(width - width / 13), int(height - height / 10), 113, 32))
        addFrame.clicked.connect(self.add_Frame)
        addFunction.setGeometry(QRect(int(width - width / 7.5), int(height - height / 10), 113, 32))
        addFunction.clicked.connect(self.add_Function)

        # TextEdit formatting
        textEdit.setGeometry(QRect(int(width / 130), int(width / 70), int(width - width / 45), int(height - height / 8)))

        # FunctionBox formatting
        functionBox.setGeometry(QRect(0, 0, int(width - width / 130), int(height / 22)))
        functionBox.activated.connect(self.fill_table)

    def create_menu(self):
        # File menu
        openFile = QAction('&Open File', self.MainWindow)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.openFile)
        fileMenu.addAction(openFile)

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

        # Edit menu
        newFrame = QAction('&New Frame', self.MainWindow)
        newFrame.setShortcut('Ctrl+N')
        newFrame.triggered.connect(self.add_Frame)
        editMenu.addAction(newFrame)

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

    def setupFileEnv(self):
        buff = buffer
        for line in buff.split('\n'):
            if '.run(' in line:
                buff = buff.replace(line,'')
        buff = f'{buff}\n'
        'from core.main import script\nscript = script()'
        fileEnvironment = {}
        exec(buff, fileEnvironment, None)
        return fileEnvironment, buff

    def fill_text(self):
        textEdit.textChanged.connect(self.textUpdate)
        textEdit.setPlainText(buffer)

    def fill_table(self):
        # Receive justified data of file from core.main
        global buffer, frames, functions, table, functionBox
        if 'from core.main' not in buffer:
            raise Exception('Invalid PyTAS file!')
        elif buffer.count('main()') > 1:
            raise Exception('Cannot read, infinite recursion')
        fileEnvironment, buff = self.setupFileEnv()
        vals = fileEnvironment['script'].run(fileEnvironment['main'],output,True)
        # Begin interpreting functions
        functions = []
        for i in fileEnvironment:
            if i in ('__builtins__','script','main'):
                continue
            fileEnvironment['script'].__init__()
            f_vals = fileEnvironment['script'].run(fileEnvironment[i],output,True)
            if not f_vals:
                continue
            functions.append({
            'name':i,
            'data':f_vals,
            'frames':f_vals[-1]['Frame'],
            'length':len(f_vals),
            })
        # Get functionBox
        func = functionBox.currentText()
        # Begin interpreting main
        frames = []
        if func != 'main':
            if func == 'Create New Function':
                func, response = QInputDialog.getText(self.MainWindow, 'Function Name', 'Enter the function name:')
                if not response or not func:
                    functionBox.setCurrentText('main')
                    self.fill_table()
                    return
                buffer = f"def {func}():\n   script.wait(1)\n\n{buffer}"
                functionBox.addItem(func)
                functionBox.setCurrentText(func)
                self.fill_table()
                return
            vals = next(n for n in functions if n['name'] == func)['data']
        n = 0
        while n < len(vals):
            i = vals[n]
            if i['Caller'] not in (func,'wait'):
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
        functionBox.addItem('Create New Function')
        if func != 'main':
            functionBox.setCurrentText(func)
        # Clear table
        self.row_count = 1
        table.setRowCount(self.row_count)
        # Begin filling table
        self.row_count += len(frames)
        table.setRowCount(self.row_count)
        for n in range(1,len(frames) + 1):
            i = frames[n - 1]

            # Frame/Function
            if not i[0]:
                item = QSpinBox()
                item.setMinimum(0)
                item.setMaximum(999999)
                item.setValue(i[1]['Frame'])
                item.valueChanged.connect(self.spinUpdate)
            else:
                item = QComboBox()
                item.addItems([ i['name'] for i in functions if i['name'] != func and func not in self.getSource(i['name']) ])
                item.setCurrentText(i[1])
                item.currentIndexChanged.connect(self.comboUpdate)
            table.setCellWidget(n, 0, item)

            # Sticks
            h = 1
            for j in ['LeftStick','RightStick']:
                item = QTableWidgetItem()
                if i[0]:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                else:
                    item.setText(i[1][j])
                table.setItem(n, h, item)
                h += 1

            # Keys
            for j in range(len(keys)):
                item = QTableWidgetItem()
                if not i[0]:
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    if keys[j] in i[1]['Key'].split(';'):
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                else:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table.setItem(n, j + 3, item)

            item = QTableWidgetItem("X")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(n,len(keys) + 3, item)
        # Fill programmatic tab
        self.fill_text()
        # Properly setup variables
        self.sort_table()

    def sort_table(self):
        global table, frames
        # Interpret table
        frames = []
        possible_frame = 0
        func = functionBox.currentText()
        for i in range(1,table.rowCount()):
            val = table.cellWidget(i,0)
            if isinstance(val,QSpinBox):
                list = []
                for n in range(3,len(keys) + 3):
                    if table.item(i,n).checkState() == Qt.Checked:
                        list.append(keys[n-3])
                key = ''
                for n in range(len(list)):
                    if n > 0:
                        key = f'{key};'
                    key = f'{key}{list[n]}'
                if key == '':
                    key = 'NONE'
                lstick = table.item(i,1)
                rstick = table.item(i,2)
                frame = val.value()
                if possible_frame < frame:
                    possible_frame = frame
                elif possible_frame == frame:
                    frame += 1
                    possible_frame = frame
                else:
                    frame = possible_frame + 1
                    possible_frame = frame
                frames.append([False,{
                'Frame':frame,
                'Key':f'{key}',
                'LeftStick':f'{lstick.text()}',
                'RightStick':f'{rstick.text()}',
                'Caller':func,
                }])
            else:
                for n in functions:
                    if val.currentText() == n['name']:
                        l = n.copy()
                        l['Frame'] = possible_frame
                        frames.append([True,l])
                        possible_frame += l['frames']
                        break
        #for i in frames:
            #print(i[0])
            #for n in i[1]:
                #print(f'   {n}: {i[1][n]}')
        # Reorganize frames list
        def ex(elem):
            return int(elem[1]['Frame'])
        frames = sorted(frames,key=ex)
        last = 0
        # Make sure functions that start on the same frame as an input always go after
        for n in range(len(frames)):
            i = frames[n]
            if i[1]['Frame'] == last and not i[0]:
                i.insert(n - 1, l.pop(n))
        # Remove any frames that are placed inside of a function
        for i in frames:
            if i[0]:
                for n in range(i[1]['Frame'] + 1,i[1]['Frame'] + i[1]['frames']):
                    for e in [ frame for frame in frames if frame[1]['Frame'] == n ]:
                        e[1]['Frame'] = i[1]['Frame'] + i[1]['frames'] + 1
                        while len([ frame for frame in frames if frame[1]['Frame'] == e[1]['Frame'] and frame != e ]) > 0:
                            e[1]['Frame'] += 1
        return frames

    def write_table(self, frames):
        global buffer, functions
        func = functionBox.currentText()
        if func != 'main':
            function = self.getSource(func)
            # Interpret frames
            char = "'"
            text = f"def {func}():\n"
            lastframe = 0
            for i in frames:
                if not i[0]:
                    i = i[1]
                    if i['Key'] != 'NONE' or i['LeftStick'] != '0;0' or i['RightStick'] != '0;0':
                        text = f"{text}    script.input({i['Frame'] - lastframe},({','.join([ f'{char}{h}{char}' for h in i['Key'].split(';') ])},),{','.join(i['LeftStick'].split(';'))},{','.join(i['RightStick'].split(';'))})\n"
                    else:
                        text = f"{text}    script.wait({i['Frame'] - lastframe})\n"
                    lastframe = i['Frame']
                else:
                    i = i[1]
                    text = f"{text}    {i['name']}()\n"
                    lastframe += i['frames']
            if len(frames) > 0:
                text = text.rstrip()
                buffer = buffer.replace(function,text)
                fileEnvironment = self.setupFileEnv()[0]
                fileEnvironment['script'].__init__()
                f_vals = fileEnvironment['script'].run(fileEnvironment[func],output,True)
                functions.append({
                'name':func,
                'data':f_vals,
                'frames':f_vals[-1]['Frame'],
                'length':len(f_vals),
                })
                list = [ i for i in functions if i['name'] == func ]
                if len(list) > 1 or len(frames) == 0:
                    functions.remove(list[0])
            else:
                text = ''
                buffer = buffer.replace(function,text)
                functionBox.setCurrentText('main')
                list = [ i for i in functions if i['name'] == func ]
                functions.remove(list[0])
                buffer = buffer.replace(f'{func}()','pass')
                self.fill_table()
            return
        # Interpret frames
        text = "# This is an auto-generated PyTAS file"
        char = "'"
        for i in functions:
            lastframe = 0
            text = f"{text}\ndef {i['name']}():\n"
            for n in i['data']:
                if int(n['Frame']) <= lastframe:
                    continue
                if n['Caller'] == i['name'] or n['Caller'] == 'wait':
                    if n['Key'] != 'NONE' or n['LeftStick'] != '0;0' or n['RightStick'] != '0;0':
                        text = f"{text}    script.input({int(n['Frame']) - lastframe},({','.join([ f'{char}{h}{char}' for h in n['Key'].split(';') ])},),{','.join(n['LeftStick'].split(';'))},{','.join(n['RightStick'].split(';'))})\n"
                    else:
                        text = f"{text}    script.wait({int(n['Frame']) - lastframe})\n"
                    lastframe = int(n['Frame'])
                else:
                    text = f"{text}    {n['Caller']}()\n"
                    lastframe += int(next( f for f in functions if f['name'] == n['Caller'] )['frames'])

        # Next, let's create main
        text = f"{text}\ndef main():\n"
        lastframe = 0
        for i in frames:
            if not i[0]:
                i = i[1]
                if i['Key'] != 'NONE' or i['LeftStick'] != '0;0' or i['RightStick'] != '0;0':
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
        buffer = text

    def getSource(self, function):
        fileEnvironment, buff = self.setupFileEnv()
        lines = buff.split('\n')
        # Some of this is sampled from the Python inspect module
        # I did not fully author the code from here -
        object = fileEnvironment[function].__code__
        lnum = object.co_firstlineno - 1
        pat = re.compile(r'^\s*def\s')
        while lnum > 0:
            if pat.match(lines[lnum]): break
            lnum = lnum - 1
        return '\n'.join(inspect.getblock(lines[lnum:])) # - to here

    def add_Frame(self):
        # Add row
        self.row_count += 1
        table.setRowCount(self.row_count)

        # Set frame
        item = QSpinBox()
        item.setMinimum(0)
        item.setMaximum(999999)
        if len(frames) > 0:
            if frames[-1]:
                frame = frames[-1][1]['Frame'] + 1
            else:
                frame = frames[-1][1]['Frame'] + frames[-1][1]['frames'] + 1
        else:
            frame = 1
        item.setValue(frame)
        item.valueChanged.connect(self.spinUpdate)
        table.setCellWidget(self.row_count - 1, 0, item)

        # Sticks
        h = 1
        for j in ['LeftStick','RightStick']:
            item = QTableWidgetItem()
            item.setText('0;0')
            table.setItem(self.row_count - 1, h, item)
            h += 1

        # Set keys
        for j in range(len(keys)):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setCheckState(Qt.Unchecked)
            table.setItem(self.row_count - 1, j + 3, item)

        # Update table
        self.tableUpdate(0,0)

    def add_Function(self):
        funcs = [ i['name'] for i in functions if i['name'] != functionBox.currentText() and functionBox.currentText() not in self.getSource(i['name']) ]
        if not len(funcs) > 0:
            return
        # Add row
        self.row_count += 1
        table.setRowCount(self.row_count)

        # Set frame
        item = QComboBox()
        item.clear()
        item.addItems(funcs)
        item.currentIndexChanged.connect(self.comboUpdate)
        table.setCellWidget(self.row_count - 1, 0, item)

        # Sticks
        h = 1
        for j in ['LeftStick','RightStick']:
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(self.row_count - 1, h, item)
            h += 1

        # Set keys
        for j in range(len(keys)):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(self.row_count - 1, j + 3, item)

        # Update table
        self.tableUpdate(0,0)

    def changeStick(self, row, col):
        global table
        cell = table.item(row,col)
        first = table.cellWidget(row,0)
        if isinstance(first,QComboBox) or not cell:
            return
        if col == 1:
            stick = 'LeftStick'
        else:
            stick = 'RightStick'
        data = [ int(axis) for axis in cell.text().split(';') ]
        x = data[0]
        y = data[1]
        # Begin creating window
        class Ui_StickControl(object):
            def setupUi(self, MainWindow):
                self.MainWindow = MainWindow
                self.MainWindow.setWindowTitle(f'Frame #{first.value()} - {stick}')
                self.width = int(width / 5)
                self.height = int(height / 2)
                self.center = int(self.width / 2)
                self.radii = int(self.center / 1.25)
                if self.height < self.width:
                    self.height = int(self.width * 1.5)
                self.MainWindow.setFixedSize(self.width, self.height)
                self.MainWindow.paintEvent = self.paintEvent
                self.MainWindow.mousePressEvent = self.mousePressEvent
                self.MainWindow.mouseReleaseEvent = self.mouseReleaseEvent
                self.MainWindow.mouseMoveEvent = self.mouseMoveEvent
                self.MainWindow.setAutoFillBackground(True)

                self.centralwidget = QWidget(self.MainWindow)
                self.centralwidget.setObjectName("centralwidget")

                self.x = x
                self.y = y

                self.mouseClick = False

                self.xSpin = QSpinBox(self.centralwidget)
                self.xSpin.setGeometry(QRect(int(self.radii / 2), self.center + int(self.radii * 1.2), int(self.radii / 1.5), int(self.radii / 4)))
                self.xSpin.setMinimum(-32767)
                self.xSpin.setMaximum(32767)
                self.xSpin.setValue(x)
                self.xSpin.valueChanged.connect(self.xSpinUpdate)

                self.ySpin = QSpinBox(self.centralwidget)
                self.ySpin.setGeometry(QRect(int(self.radii * (4/3)), self.center + int(self.radii * 1.2), int(self.radii / 1.5), int(self.radii / 4)))
                self.ySpin.setMinimum(-32767)
                self.ySpin.setMaximum(32767)
                self.ySpin.setValue(y)
                self.ySpin.valueChanged.connect(self.ySpinUpdate)

            def paintEvent(self, event):
                self.centralwidget.painter = QPainter()
                self.centralwidget.painter.begin(self.MainWindow)
                self.centralwidget.painter.setPen(QPen(QColor(0,0,0), 3, Qt.SolidLine))
                self.centralwidget.painter.setBrush(QColor(40, 40, 40))
                self.centralwidget.painter.drawEllipse(QPoint(self.center,self.center), self.radii, self.radii)
                self.centralwidget.painter.drawLine(self.center - self.radii,self.center,self.center + self.radii,self.center)
                self.centralwidget.painter.drawLine(self.center,self.center - self.radii,self.center,self.center + self.radii)
                self.centralwidget.painter.setPen(QPen(QColor(255,0,0), 1, Qt.SolidLine))
                self.centralwidget.painter.setBrush(QColor(255, 0, 0))
                self.centralwidget.painter.drawEllipse(QPoint(int(self.center + (self.x * self.radii / 32767)),int(self.center + (self.y * self.radii / 32767))), 5, 5)
                self.centralwidget.painter.end()

            def xSpinUpdate(self):
                if math.sqrt( (int(self.center + (self.xSpin.value() * self.radii / 32767)) - self.center)**2 + (int(self.center + (self.ySpin.value() * self.radii / 32767)) - self.center)**2 ) <= self.radii:
                    self.x = self.xSpin.value()
                else:
                    self.xSpin.setValue(self.x)
                self.MainWindow.update()

            def ySpinUpdate(self):
                if math.sqrt( (int(self.center + (self.xSpin.value() * self.radii / 32767)) - self.center)**2 + (int(self.center + (self.ySpin.value() * self.radii / 32767)) - self.center)**2 ) <= self.radii:
                    self.y = self.ySpin.value()
                else:
                    self.ySpin.setValue(self.y)
                self.MainWindow.update()

            def mousePressEvent(self, event):
                self.mouseClick = True
                self.mouseMoveEvent(event)

            def mouseReleaseEvent(self, event):
                self.mouseClick = False

            def mouseMoveEvent(self, event):
                if not self.mouseClick:
                    return
                posx = event.pos().x()
                posy = event.pos().y()
                if math.sqrt( (posx - self.center)**2 + (posy - self.center)**2 ) <= self.radii:
                    self.x = int((posx - self.center) * 32767 / self.radii)
                    self.y = int((posy - self.center) * 32767 / self.radii)
                    self.xSpin.setValue(self.x)
                    self.ySpin.setValue(self.y)
        global stickControl
        stickControl = QWidget()
        def closeEvent(event: QCloseEvent):
            stickControl.close()
            self.MainWindow.setEnabled(True)
            x = Ui_StickControl.x
            y = Ui_StickControl.y
            item = QTableWidgetItem()
            item.setText(f'{x};{y}')
            table.setItem(row, col, item)
            self.tableUpdate(0,0)
        stickControl.closeEvent = closeEvent
        Ui_StickControl = Ui_StickControl()
        Ui_StickControl.setupUi(stickControl)
        self.MainWindow.setEnabled(False)
        stickControl.show()

    def removeRow(self, row):
        table.removeRow(row)
        self.row_count -= 1

    # Event-based functions
    def textUpdate(self):
        global buffer
        buffer = textEdit.toPlainText()

    def tableUpdate(self, row, col):
        if col == len(keys) + 3 and row != 0:
            self.removeRow(row)
        elif 3 > col > 0 and row != 0:
            self.changeStick(row, col)
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

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.exit()

    # QActions
    def openFile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setNameFilters(["Python files (*.py)",])
        dlg.selectNameFilter("Python files (*.py)")

        if dlg.exec_() == QDialog.Accepted:
            global buffer, filename
            filename = dlg.selectedFiles()[0]
        else:
            self.openFile()
            return
        # Buffer
        with open(filename,'r') as file:
            buffer = file.read()
        # A commonly-recurring function that pulls data from the buffer and writes it to the table
        self.fill_table()

        # Warn users
        self.notice()

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
    filename = './script.py'
    output = 'script1'
    buffer = None

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    window = GUI(MainWindow)
    window.setupUi(MainWindow)
    window.selfService()
    MainWindow.show()
    sys.exit(app.exec_())
