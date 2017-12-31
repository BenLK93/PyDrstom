import sqlite3
import datetime


def input_db(ime, datum, prihod, odhod):
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	
	# c.execute('''CREATE TABLE ure_zaposlenih(ime text, datum text, prihod text, odhod text, ure_skupaj text, datum_vnosa text)''')
	datum_vnosa = datetime.datetime.now()
	

	leto, mesec, dan = map(int, datum.split('-')) #razbijanje datuma in konverzija iz str v int
	datum_dd = datetime.date(leto, mesec, dan) #sestavljanje v datetime.date format

	ura, minuta = map(int, prihod.split(':')) #razbijanje vnešenega niza za uro prihoda
	cas_prihoda = datetime.time(ura, minuta)  # sestavljanje v datetime.time format
	cp = datetime.datetime.combine(datetime.date(leto, mesec, dan), datetime.time(ura, minuta)) #združujemo datetime.date in datetime.time v datetime.datime format

	ura, minuta = map(int, odhod.split(':'))
	cas_odhoda = datetime.time(ura, minuta)
	co = datetime.datetime.combine(datetime.date(leto, mesec, dan), datetime.time(ura, minuta))

	delovni_cas = co - cp   #potreben datime.datetime format za operand '-'

	cas_prihoda = str(cas_prihoda)
	cas_odhoda = str(cas_odhoda)
	delovni_cas = str(delovni_cas)



	c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?, ?)", (ime, datum, cas_prihoda, cas_odhoda, delovni_cas, datum_vnosa))

	conn.commit()

	for row in c.execute('SELECT rowid, ime, datum, prihod, odhod, ure_skupaj, datum_vnosa FROM ure_zaposlenih ORDER BY prihod'):
		print(row)

	conn.close()


def update_entry(rowid, ime, datum, prihod, odhod):
	
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	
	c.execute('UPDATE ure_zaposlenih SET ime=? WHERE rowid=?', (rowid, ime))

	conn.commit()

	for row in c.execute('SELECT * FROM test2 WHERE ime=? ', (data1, )):
		print(row)
	
	conn.close()


def delete_entry(rid):
	conn = sqlite3.connect('example.db')
	c = conn.cursor()

	c.execute('''DELETE FROM ure_zaposlenih WHERE rowid=? ''', (rid, ))

	conn.commit()

	conn.close()
	

def search_db():
	pass

	