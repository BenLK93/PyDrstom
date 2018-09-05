##
# Python's program to calculate time difference between two datetime objects.
 
import datetime
from datetime import timedelta
import psycopg2
conn = psycopg2.connect("dbname=ure user=postgres password=")
c = conn.cursor()


c.execute("""SELECT * FROM dogodek where zaposleni_id=5 order by cas_datum asc;""")
counterTip=0
counter2=0
dateprihod=""
dateodhod=""
skupaj=datetime.datetime(1,1,1,0,0,0,0)

for row in c:
	print(skupaj)
	if(row[4]=="prihod" and counterTip==0):
		dateprihod=row[3]
		counterTip=1

	elif(row[4]=="odhod" and counterTip==1):
		counterTip=0
		dateodhod=row[3]
		msg=dateodhod-dateprihod
		skupaj=skupaj+msg
	else:
		print("napaka pri vrsti", row[0] )
		break

		
	print(row[0],row[3], row[4])
izracun = skupaj-datetime.datetime(1,1,1,0,0,0,0)
print(izracun)
print(int(izracun.seconds/3600 +izracun.days*24) )

# datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
# date1 = '2016-04-16 10:01:28.585'
# date2 = '2016-04-10 09:56:28.067'
# diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
 

# total_min = int(diff.days)*24

# print("Difference:", diff)

# print(total_min, "H:", diff.seconds/60, "min")




