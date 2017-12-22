import sqlite3

def input_db():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	
	#  c.execute('''CREATE ure_zaposlenih(entry_id INTEGER PRIMARY KEY AUTOINCREMENT, ime text, datum text, prihod text, odhod text, ure_skupaj text, datum vnosa text)''')

	c.execute("INSERT INTO ure_zaposlenih VALUES(?, ?, ?, ?, ?, ?)", (ime, datum, prihod, odhod, ure_dela, datum_vnosa))

	conn.commit()

	for row in c.execute('SELECT * FROM test2 ORDER BY ime'):
		print(row)

	conn.close()


def update_entry():
	
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	
	c.execute('UPDATE test2 SET ime=? WHERE ime=?', (data1,data2))

	conn.commit()

	for row in c.execute('SELECT * FROM test2 WHERE ime=? ', (data1, )):
		print(row)
	
	conn.close()


def delete_entry():
	pass

def search_db():

	for row in c.execute('SELECT * FROM test2 WHERE ime=? ', (data1, )):
		print(row)