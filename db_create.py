import sqlite3

conn = sqlite3.connect('drstom_ure_zaposleni.db')
c = conn.cursor()
# c.execute("""DROP TABLE zaposleni;""")
# c.execute("""CREATE TABLE IF NOT EXISTS zaposleni (id integer NOT NULL, name text NOT NULL, zaposlen_kot text, zaposlen_od text, zaposlen_do text); """)
# c.execute("""INSERT INTO zaposleni(id,name,zaposlen_kot,zaposlen_od,zaposlen_do) VALUES (1, "test1", "test11","test2018","test2019")""")
# c.execute("""INSERT INTO zaposleni(id,name,zaposlen_kot,zaposlen_od,zaposlen_do) VALUES (2, "test2", "test22","test2018","test2019")""")
# data= c.execute("""SELECT rowid, *FROM zaposleni""")

# for row in data:
# 	print (row)


# c.execute("""DROP TABLE IF EXISTS ure_zaposlenih;""")
# c.execute("""CREATE TABLE IF NOT EXISTS ure_zaposlenih(id integer NOT NULL, ime_zaposlenega text NOT NULL, datum text NOT NULL, cas text NOT NULL, dogodek text NOT NULL);""")
# c.execute("""INSERT INTO ure_zaposlenih(id, ime_zaposlenega, datum, cas, dogodek) VALUES (2, "test2", "1.3.2017", "8:00", "prihod")""")

# conn.commit()

data2= c.execute("""SELECT rowid, *FROM ure_zaposlenih""")

for row in data2:
	print(row)

	
conn.close()