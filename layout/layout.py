# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1300, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1301, 681))
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.table = QtWidgets.QTableWidget(self.tab1)
        self.table.setGeometry(QtCore.QRect(10, 30, 1271, 611))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.table.setFont(font)
        self.table.setColumnCount(18)
        self.table.setObjectName("table")
        self.table.setRowCount(0)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.functionBox = QtWidgets.QComboBox(self.tab1)
        self.functionBox.setGeometry(QtCore.QRect(0, 0, 1291, 32))
        self.functionBox.setObjectName("functionBox")
        self.tabWidget.addTab(self.tab1, "Visual")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.textEdit = QtWidgets.QTextEdit(self.tab2)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 1271, 631))
        self.textEdit.setObjectName("textEdit")
        self.tabWidget.addTab(self.tab2, "Programmatic")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 22))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Your code is here! The main() function is what\'s run."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())