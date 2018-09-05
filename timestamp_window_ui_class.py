import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from timestamp_window_ui import *
import psycopg2
import datetime
from time import sleep

class MainWindow(QMainWindow, Ui_MainWindow):

    conn = psycopg2.connect("dbname=ure user=postgres password=")
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

        conn = psycopg2.connect("dbname=ure user=postgres password=")
        c = conn.cursor()
        c.execute("""SELECT *FROM chip;""")

        for row in c:
            # print(row)
            if (self.trenutni_ID[0]==row[2]):
                self.sporocilo.setText("")
                self.trenutni_ID.append(str(row[1]))

                print(row[0], row[1], row[2], row[3])
                zdl = str(row[1])
                c.execute("""SELECT * FROM zaposleni WHERE zaposleni_id=%s;""",(zdl))

                for row in c:
                    print(row)
                text1= "Pozdravljen/a " + str(row[2])+" "+str(row[3])
                self.pushButtonPrihod.show()
                self.pushButtonOdhod.show()
                self.pushButtonInfo.show()
                break
                
            else:
                print("wrong person")
                text1 = "Čip ni bil prepoznan"
                self.pushButtonPrihod.hide()
                self.pushButtonOdhod.hide()
                self.pushButtonInfo.hide()
                self.sporocilo.show()
                self.sporocilo.setText("NAPAČEN ČIP!")

                



        self.izpisID(text1)
              
    def izpisID(self,izpis_text):

        self.izpis.setText(izpis_text)


    def prihodGumb(self):
        conn = psycopg2.connect("dbname=ure user=postgres password=")
        c = conn.cursor()


        print(str(datetime.datetime.now()))
        print(self.trenutni_ID[0])

        try:

            idz = str(self.trenutni_ID[1])
            datum_cas = str(datetime.datetime.now())
            dogodek = "prihod"
            # print(ID)
            c.execute("""INSERT INTO dogodek(zaposleni_id, cas_datum, tip_dogodka) VALUES(%s, %s, %s);""", (idz, datum_cas, dogodek))
            # c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?)", (ID, ime, datum, cas, dogodek))
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

        conn = psycopg2.connect("dbname=ure user=postgres password=")
        c = conn.cursor()

        try:
            idz = str(self.trenutni_ID[1])
            datum_cas = datetime.datetime.now()
            dogodek = "odhod"
            # print(ID)
            c.execute("""INSERT INTO dogodek(zaposleni_id, cas_datum, tip_dogodka) VALUES(%s, %s, %s);""", (idz, datum_cas, dogodek))
            # c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?)", (ID, ime, datum, cas, dogodek))
            conn.commit()
            # print(ID)
            # c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?)", (ID, ime, datum, cas, dogodek))
            # conn.commit()
        except:
            print("error")
        conn.close()
        self.pushButtonPrihod.hide()
        self.pushButtonOdhod.hide()
        self.pushButtonInfo.hide()
        self.sporocilo.show()

    def infoGumb(self):
        conn = psycopg2.connect("dbname=ure user=postgres password=")
        c = conn.cursor()
        zid= str(self.trenutni_ID[1])
        print(zid)

        try:
            c.execute("""SELECT cas_datum FROM dogodek WHERE zaposleni_id=%s ORDER BY cas_datum DESC; """,(zid,))
            for row in c:
                date = row[0]
                print(date)
 
        except:
            print("error")

        conn.close()
