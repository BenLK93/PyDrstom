import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

def tick():
    print('tick')

timer = QTimer()
timer.timeout.connect(tick)
timer.start(1000)

# run event loop so python doesn't exit
app.exec_()