import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow
from browse_window_ui import *
import psycopg2
from datetime import timedelta
from datetime import date
from datetime import datetime
from datetime import time


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		conn = psycopg2.connect("dbname=ure user=postgres password=")
		c = conn.cursor()
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.pushButton_Iskanje.clicked.connect(self.iskanje)
		self.radioButton_DSC.setChecked(True)
		self.radioButton_Vse.setChecked(True)
		self.comboBoxZaposleni.addItem("Vsi")
		self.comboBox_ZaposleniImeSpremeni.addItem(" ")
		self.comboBox_ZaposleniImeVnos.addItem(" ")
		self.dateEdit_DatumOdIskanje.setDate(QDate.currentDate())
		datum_do=QDate.currentDate().addDays(1)
		self.dateEdit_DatumDoIskanje.setDate(datum_do)
		self.dateEdit_DatumVnosa.setDate(QDate.currentDate())
		self.dateEdit_DatumSpremeni.setDate(QDate.currentDate())
		self.pushButton_VnosDogodka.clicked.connect(self.vnos)
		self.pushButton_delete.clicked.connect(self.odstrani)
		self.pushButton_izberiNapako.clicked.connect(self.najdi_napako)
		self.pushButton_izracunajPonovno.clicked.connect(self.ponovno_izracunaj)
		self.pushButton_GenerirajPorocilo.clicked.connect(self.generiraj_porocilo)
		self.comboBox_DogodekVnos.addItem(" ")
		self.comboBox_DogodekSpremeni.addItem(" ")
		self.comboBox_DogodekVnos.addItem("odhod")
		self.comboBox_DogodekSpremeni.addItem("odhod")
		self.comboBox_DogodekVnos.addItem("prihod")
		self.comboBox_DogodekSpremeni.addItem("prihod")

		c.execute('''SELECT * FROM zaposleni''')
		for row in c:
			print(row)
			self.comboBoxZaposleni.addItem(row[2])
			self.comboBox_ZaposleniImeSpremeni.addItem(row[2])
			self.comboBox_ZaposleniImeVnos.addItem(row[2])
			self.comboBoxZaposleniPorocilo.addItem(row[2])


	def najdi_napako(self):
		allRows = self.tableWidget.rowCount()
		for row in range(0, allRows):
			twi0 = self.tableWidget.item(row,0).text()
			print(twi0)
			# twi1 = self.tableWidget.item(row,1).text()
			# twi2 = self.tableWidget.cellWidget(row,2).text()
			if(twi0 == self.label_napaka.text()):
				self.tableWidget.selectRow(row)
			else:
				print("ni napak")
			
			
	def ponovno_izracunaj(self):
		self.iskanje()
		
	def odstrani(self):
		conn = psycopg2.connect("dbname=ure user=postgres password=")
		c = conn.cursor()
		rowcount = self.tableWidget.currentRow() #get row index

		print(self.tableWidget.item(rowcount,0).text()) #print item on row r and column index 3(starts from 0)
		dogodek_id = self.tableWidget.item(rowcount,0).text()
		c.execute("""SELECT * FROM dogodek WHERE dogodek_id=%s""", (dogodek_id,))
		for row in c:
			print(row)

	def popravi(self):
		r = self.tableWidget.currentRow() #get row index
		print(self.tableWidget.item(r,3).text()) #print item on row r and column index 3(starts from 0)

	def vnos(self):
		conn = psycopg2.connect("dbname=ure user=postgres password=")
		c = conn.cursor()
		ura = self.timeEdit_UraVnos.time().toPyTime()
		print(ura)
		ime = self.comboBox_ZaposleniImeVnos.currentText()
		cas_datum = datetime.combine(self.dateEdit_DatumVnosa.date().toPyDate(), ura)
		print(cas_datum)
		tip_dogodka = self.comboBox_DogodekVnos.currentText()
		c.execute("""INSERT INTO dogodek (zaposleni_id, cas_datum, tip_dogodka) VALUES ((SELECT zaposleni_id FROM zaposleni WHERE ime=%s), %s, %s); """, (ime, cas_datum, tip_dogodka))
		conn.commit()
	def iskanje(self):
		conn = psycopg2.connect("dbname=ure user=postgres password=")
		c = conn.cursor()

		zaposleni = self.comboBoxZaposleni.currentText()

		c.execute("""SELECT zaposleni_id FROM zaposleni WHERE ime=%s """, (zaposleni,))
		zaposleniID = c.fetchone()
		
		datum_od = self.dateEdit_DatumOdIskanje.date().toPyDate()

		datum_do = self.dateEdit_DatumDoIskanje.date().toPyDate()

		datum_od2= datetime.combine(datum_od, time(0,0,0,111111))

		datum_do2= datetime.combine(datum_do, time(0,0,0,111111))
		# print(datum_od2, datum_do2)
		f_prihod = self.radioButton_prihod.isChecked()
		f_odhod = self.radioButton_odhod.isChecked()
		f_vsi = self.radioButton_Vse.isChecked()
		f_zaposleni = self.checkBox_zposleni.isChecked()
		f_order = self.radioButton_ASC.isChecked()
		# print(datum_do,datum_do, zaposleni)

		if(f_odhod==False and f_vsi!=True):
			f_dogodek="prihod"
		elif(f_prihod==True):
			pass
		else:
			f_dogodek="odhod"


		##
		if(f_zaposleni!="Vsi"):

			c.execute("""SELECT * FROM dogodek WHERE zaposleni_id =%s AND cas_datum BETWEEN %s AND %s ORDER BY cas_datum ASC;""", (zaposleniID, datum_od, datum_do))
			counterTip=0
			counter2=0
			dateprihod=""
			dateodhod=""
			skupaj=datetime(1,1,1,0,0,0,0)


			for row in c:
				print(skupaj)
				counter2 +=1
				print(counter2)
				if(row[4]=="prihod" and counterTip==0):
					dateprihod=row[3]
					counterTip=1

				elif(row[4]=="odhod" and counterTip==1):
					counterTip=0
					dateodhod=row[3]
					msg=dateodhod-dateprihod
					skupaj=skupaj+msg
				elif(row[4]=="odhod" and counterTip==0 and counter2==1):
					continue
				else:
					napaka_sporocilo=str(row[0])
					print("napaka pri vrsti", row[0] )
					self.label_napaka.setText(napaka_sporocilo)
					break

					
				print(row[0],row[3], row[4])
			izracun = skupaj-datetime(1,1,1,0,0,0,0)
			print(izracun)
			print(int(izracun.seconds/3600 +izracun.days*24) )
			self.label_vsota1.setText(str(izracun))
			self.label_vsota2.setText(str(izracun.seconds/3600 +izracun.days*24))
			self.label_datumIntOd.setText(self.dateEdit_DatumOdIskanje.text())
			self.label_datumIntDo.setText(self.dateEdit_DatumDoIskanje.text())

		else:
			pass

		##


		if(f_vsi == True and f_zaposleni == False and f_order == True):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE z.ime=%s AND cas_datum BETWEEN %s AND %s ORDER BY d.cas_datum ASC;""", (zaposleni, datum_od, datum_do))

		elif(f_vsi == True and f_zaposleni == False and f_order == False):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE z.ime=%s AND cas_datum BETWEEN %s AND %s ORDER BY d.cas_datum DESC;""", (zaposleni, datum_od, datum_do))

		elif(f_vsi == True and f_zaposleni == True and f_order == True):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE z.ime=%s AND cas_datum BETWEEN %s AND %s ORDER BY z.ime ASC;""", (zaposleni, datum_od, datum_do))

		elif(f_vsi == True and f_zaposleni == True and f_order == False):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE z.ime=%s AND cas_datum BETWEEN %s AND %s ORDER BY z.ime DESC;""", (zaposleni, datum_od, datum_do))



		elif(f_vsi == False and f_zaposleni == False and f_order == True):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE d.tip_dogodka=%s AND z.ime=%s AND d.cas_datum BETWEEN %s AND %s ORDER BY d.cas_datum ASC;""", (f_dogodek, zaposleni, datum_od, datum_do))
		elif(f_vsi == False and f_zaposleni == False and f_order == False):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE d.tip_dogodka=%s AND z.ime=%s AND d.cas_datum BETWEEN %s AND %s ORDER BY d.cas_datum DESC;""", (f_dogodek, zaposleni, datum_od, datum_do))
		elif(f_vsi == False and f_zaposleni == True and f_order == True):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE d.tip_dogodka=%s AND z.ime=%s AND d.cas_datum BETWEEN %s AND %s ORDER BY z.ime ASC;""", (f_dogodek, zaposleni, datum_od, datum_do))
		elif(f_vsi == False and f_zaposleni == True and f_order == False):
			c.execute("""SELECT d.dogodek_id, d.cas_datum, d.tip_dogodka, z.ime, z.priimek  FROM dogodek AS d INNER JOIN zaposleni AS z
ON d.zaposleni_id = z.zaposleni_id WHERE d.tip_dogodka=%s AND z.ime=%s AND d.cas_datum BETWEEN %s AND %s ORDER BY z.ime DESC;""", (f_dogodek, zaposleni, datum_od, datum_do))
		
		else:
			print("Error")
		# print(c.rowcount, "rowcount")
		self.tableWidget.setRowCount(c.rowcount)
		self.tableWidget.setColumnCount(5)


		##
		





		##

		for row, form in enumerate(c):
			print(form)
			for column, item in enumerate(form):
				# print(str(item))
				# item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
				
				self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))		
		
	def generiraj_porocilo(self):
		conn = psycopg2.connect("dbname=ure user=postgres password=")
		c = conn.cursor()

		ime = self.comboBoxZaposleniPorocilo.currentText()
		datum_do = self.dateEdit_DatumDoPorocilo.date().toPyDate()
		datum_od = self.dateEdit_DatumOdPorocilo.date().toPyDate()

		
		c.execute("""SELECT zaposleni_id FROM zaposleni WHERE ime=%s """, (ime,))
		zaposleniID = c.fetchone()

		# datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
		# date1 = '2016-04-16 10:01:28.585'
		# date2 = '2026-04-10 09:56:28.067'
		# datum_od = datetime.strptime(date1, datetimeFormat)
		# datum_do = datetime.strptime(date2, datetimeFormat)
		
		

		c.execute("""SELECT * FROM dogodek WHERE zaposleni_id =%s AND cas_datum BETWEEN %s AND %s ORDER BY cas_datum ASC;""", (zaposleniID, datum_od, datum_do))
		counterTip=0
		counter2=0
		counter3=1
		dateprihod=""
		dateodhod=""
		porocilo_text=""
		skupaj=datetime(1,1,1,0,0,0,0)

		file = open("testporocilo.rtf", "w") 

		naslov="Poročilo delovnih ur.\n" +"Zaposleni: " +str(ime)+"\n"+"Časovno obdobje: "+str(datum_od)+" - "+str(datum_do) +"\n"
		file.write(naslov)
		
		for row in c:
			# print(skupaj)
			counter2 +=1
			print(counter2)
			# print(counter2)
			if(row[4]=="prihod" and counterTip==0):
				
				dateprihod=row[3]
				counterTip=1
				dan= self.dnevi_tedna(row[3].weekday())
				msg0=str(counter3)+" "+str(row[3])+ " "+str(dan)+" "+str(row[4])+"\n"
				print(msg0)
				file.write(msg0)
				# porocilo_text += msg0




			elif(row[4]=="odhod" and counterTip==1):
				
				counterTip=0
				dateodhod=row[3]
				msg=dateodhod-dateprihod
				counter3 +=1
				dan1= self.dnevi_tedna(row[3].weekday())
				print(dan1)
				print(row[3].weekday())
				msg1= "  "+str(row[3])+"  "+str(dan1)+" "+ str(row[4])+ "   Delovne ure:"+ str(msg)+"\n\n" 
				print(msg1)
				# porocilo_text += msg1
				file.write(msg1)
				print(counter2)


				skupaj=skupaj+msg
			elif(row[4]=="odhod" and counterTip==0 and counter2==1):
				

				continue
			else:
				napaka_sporocilo=str(row[0])
				print("napaka pri vrsti", row[0] )
				break

				
			
		izracun = skupaj-datetime(1,1,1,0,0,0,0)
		# file.write(porocilo_text)
		# file.write(porocilo_text)
		print(izracun)
		print(int(izracun.seconds/3600 +izracun.days*24) )
		vsota = str(izracun.seconds/3600 +izracun.days*24)
		file.write("\n\n")
		file.write("Vsota ur:")
		file.write(vsota)

		# text= file.read()
		# self.textEdit.setText(text)


		 
		file.close() 

		file1 = open("testporocilo.rtf", "r")
		porocilo1 = file1.read()
		self.textEdit.setText(porocilo1)

	def dnevi_tedna(self, dan):
		if(dan==0):
			return "Pon    "
		elif(dan==1):
			return "Tor    "
		elif(dan==2):
			return "Sre    "
		elif(dan==3):
			return "Čet    "
		elif(dan==4):
			return "Pet    "
		elif(dan==5):
			return "Sob    "
		elif(dan==6):
			return "Ned    "
		else:
			return "//"
	# def rezultati_iz_baze(self):
	# 	conn = psycopg2.connect("dbname=ure user=postgres password=")
	# 	c = conn.cursor()
	# 	rowcount = c.execute('''SELECT COUNT(*) FROM ure_zaposlenih''').fetchone()[0]
	# 	self.tableWidget.setRowCount(rowcount)
	# 	self.tableWidget.setColumnCount(6)
	# 	c.execute('''SELECT rowid,* FROM ure_zaposlenih''')
		
	# 	print(c.rowcount)
	# 	for row, form in enumerate(c):
	# 		print(form)
	# 		for column, item in enumerate(form):
	# 			print(str(item))
	# 			# item.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )
				
	# 			self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))

				