import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from timestamp_window_ui import *
import sqlite3
import datetime
from time import sleep

class MainWindow(QMainWindow, Ui_MainWindow):

    conn = sqlite3.connect('drstom_ure_zaposleni.db')
    c = conn.cursor()
    trenutni_ID=[]
    def __init__(self):

        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.display_clock)
        self.timer.start(1000)
        self.cas.setText(str(datetime.datetime.now().strftime('%H:%M:%S')))
        self.datum.setText(str(datetime.datetime.now().strftime('%d.%m.%Y')))
        self.vnos.returnPressed.connect(self.vnosID)
        self.pushButtonPrihod.clicked.connect(self.prihodGumb)
        self.pushButtonOdhod.clicked.connect(self.odhodGumb)
        self.pushButtonInfo.clicked.connect(self.infoGumb)
        self.pushButtonPrihod.hide()
        self.pushButtonOdhod.hide()
        self.pushButtonInfo.hide()
        self.sporocilo.setText("Postavite čip na čitalec.")
        self.izpis2.setText("")

    def display_clock(self):

    	self.cas.setText(str(datetime.datetime.now().strftime('%H:%M:%S')))
    	self.datum.setText(str(datetime.datetime.now().strftime('%d.%m.%Y')))
        
    
    

    def vnosID(self):

        self.sporocilo.hide()
        self.trenutni_ID=[]

        self.trenutni_ID.append(str(self.vnos.text()))
        sleep(0.2)
        self.vnos.setText("")
        print(self.trenutni_ID[0])


        conn = sqlite3.connect('drstom_ure_zaposleni.db')
        c = conn.cursor()
        data = c.execute("""SELECT rowid,*FROM zaposleni;""")

        for row in data:
            print(row)
            if (str(self.trenutni_ID[0])==str(row[1])):
                self.sporocilo.setText("")
                self.trenutni_ID.append(str(row[2]))
                print(row[1])
                text1= "Pozdravljen/a " + str(self.trenutni_ID[1])
                self.pushButtonPrihod.show()
                self.pushButtonOdhod.show()
                self.pushButtonInfo.show()
                break
            else:
                print("wrong person")
                text1 = "Či ni bil prepoznan"
                self.pushButtonPrihod.hide()
                self.pushButtonOdhod.hide()
                self.pushButtonInfo.hide()
                self.sporocilo.show()
                self.sporocilo.setText("NAPAČEN ČIP!")

                



        self.izpisID(text1)
              
    def izpisID(self,izpis_text):

        self.izpis.setText(izpis_text)


    def prihodGumb(self):

        conn = sqlite3.connect('drstom_ure_zaposleni.db')
        c = conn.cursor()


        print(str(datetime.datetime.now()))
        print(self.trenutni_ID[0])

        try:

            ID = int(self.trenutni_ID[0])
            ime = str(self.trenutni_ID[1])
            cas = str(self.cas.text())
            datum = str(self.datum.text())
            dogodek = "prihod"
            # print(ID)
            c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?)", (ID, ime, datum, cas, dogodek))
            conn.commit()
        except:
            print("error")
        conn.close()
        self.pushButtonPrihod.hide()
        self.pushButtonOdhod.hide()
        self.pushButtonInfo.hide()
        self.sporocilo.show()
        self.sporocilo.setText("")

    def odhodGumb(self):

        conn = sqlite3.connect('drstom_ure_zaposleni.db')
        c = conn.cursor()

        try:
            ID = int(self.trenutni_ID[0])
            ime = str(self.trenutni_ID[1])
            cas = str(self.cas.text())
            datum = str(self.datum.text())
            dogodek = "odhod"
            # print(ID)
            c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?)", (ID, ime, datum, cas, dogodek))
            conn.commit()
        except:
            print("error")
        conn.close()
        self.pushButtonPrihod.hide()
        self.pushButtonOdhod.hide()
        self.pushButtonInfo.hide()
        self.sporocilo.show()

    def infoGumb(self):
        
        conn = sqlite3.connect('drstom_ure_zaposleni.db')
        c = conn.cursor()

        try:
            print(self.trenutni_ID[0]) 
            print(self.trenutni_ID[1])
            print(self.cas.text())
            print(self.datum.text())
            print("Odhod")
        except:
            print("error")

        conn.close()
