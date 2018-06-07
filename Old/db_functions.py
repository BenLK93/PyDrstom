import sqlite3
import datetime




def input_db(ime, datum, prihod, odhod, tip_dneva):
	conn = sqlite3.connect('drstom.db')
	c = conn.cursor()
	
	# c.execute('''CREATE TABLE ure_zaposlenih(ime text, datum text, prihod text, odhod text, ure_skupaj text, datum_vnosa text, tip_dneva)''')
	datum_vnosa = datetime.datetime.now()
	
	try:
		dan, mesec, leto = map(int, datum.split('.')) #razbijanje datuma in konverzija iz str v int
		datum_dd = datetime.date(leto, mesec, dan) #sestavljanje v datetime.date format
	except:
		pass
	try:
		ura, minuta = map(int, prihod.split('.')) #razbijanje vnešenega niza za uro prihoda
		cas_prihoda = datetime.time(ura, minuta)  # sestavljanje v datetime.time format
		cp = datetime.datetime.combine(datetime.date(leto, mesec, dan), datetime.time(ura, minuta)) #združujemo datetime.date in datetime.time v datetime.datime format
	except:
		pass
	try:
		ura, minuta = map(int, odhod.split('.'))
		cas_odhoda = datetime.time(ura, minuta)
		co = datetime.datetime.combine(datetime.date(leto, mesec, dan), datetime.time(ura, minuta))
	except:
		pass
	

	try:
		delovni_cas = co - cp   #potreben datime.datetime format za operand '-'

		cas_prihoda = str(cas_prihoda)
		cas_odhoda = str(cas_odhoda)
		delovni_cas = str(delovni_cas)
		datum_dd = str(datum_dd)



		c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?, ?, ?)", (ime, datum_dd, cas_prihoda, cas_odhoda, delovni_cas, datum_vnosa, tip_dneva))
		conn.commit()
		return True
	except:
		pass


	conn.close()


def input_db_drugo(ime, datum, tip_dneva):
	conn = sqlite3.connect('drstom.db')
	c = conn.cursor()

	datum_vnosa = datetime.datetime.now()

	try:
		dan, mesec, leto = map(int, datum.split('.')) #razbijanje datuma in konverzija iz str v int
		datum_dd = datetime.date(leto, mesec, dan) #sestavljanje v datetime.date format
	except:
		pass

	try:
		delovni_cas = "8:00:00" 

		cas_prihoda = "/"
		cas_odhoda = "/"
		datum_dd = str(datum_dd)



		c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?, ?, ?)", (ime, datum_dd, cas_prihoda, cas_odhoda, delovni_cas, datum_vnosa, tip_dneva))
		conn.commit()
		return True
	except:
		pass

	datum_vnosa = datetime.datetime.now()

def update_entry(rowid, ime, datum, prihod, odhod):
	
	conn = sqlite3.connect('drstom.db')
	c = conn.cursor()
	
	c.execute('UPDATE ure_zaposlenih SET ime=? WHERE rowid=?', (rowid, ime))

	conn.commit()

	for row in c.execute('SELECT * FROM test2 WHERE ime=? ', (data1, )):
		print(row)
	
	conn.close()


def delete_entry(rid):
	conn = sqlite3.connect('drstom.db')
	c = conn.cursor()

	c.execute('''DELETE FROM ure_zaposlenih WHERE rowid=? ''', (rid, ))

	conn.commit()

	conn.close()
	

def search_db():
	pass

	