import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow
from browse_window_ui import *
import sqlite3

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.pushButtonGetAll.clicked.connect(self.rezultati_iz_baze)

	def rezultati_iz_baze(self):
		conn = sqlite3.connect('drstom_ure_zaposleni.db')
		c = conn.cursor()
		rowcount = c.execute('''SELECT COUNT(*) FROM ure_zaposlenih''').fetchone()[0]
		self.tableWidget.setRowCount(rowcount)
		self.tableWidget.setColumnCount(6)
		c.execute('''SELECT rowid,* FROM ure_zaposlenih''')
		
		print(c.rowcount)
		for row, form in enumerate(c):
			print(form)
			for column, item in enumerate(form):
				print(str(item))
				# item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
				
				self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))

				