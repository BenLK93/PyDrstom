import psycopg2
import datetime
conn = psycopg2.connect("dbname=ure user=postgres password=")
zid=2
c = conn.cursor()
ime="Anne Marrie"
d1=datetime.datetime(2018, 9, 5, 1, 11, 56)
d2=datetime.datetime(2008, 8, 5, 1, 11, 56)
c.execute("""SELECT *FROM dogodek;""")
print(c.rowcount)
for row in c:
	print(row)

print (d1)