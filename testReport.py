##
# Python's program to calculate time difference between two datetime objects.
 
import datetime
from datetime import timedelta
from datetime import datetime
import psycopg2
conn = psycopg2.connect("dbname=ure user=postgres password=")
c = conn.cursor()

datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
date1 = '2016-04-16 10:01:28.585'
date2 = '2026-04-10 09:56:28.067'
datum_od = datetime.strptime(date1, datetimeFormat)
datum_do = datetime.strptime(date2, datetimeFormat)
zaposleniID=5

c.execute("""SELECT * FROM dogodek WHERE zaposleni_id =%s AND cas_datum BETWEEN %s AND %s ORDER BY cas_datum ASC;""", (zaposleniID, datum_od, datum_do))
counterTip=0
counter2=0
counter3=1
dateprihod=""
dateodhod=""
skupaj=datetime(1,1,1,0,0,0,0)


def dnevi_tedna(dan):
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



file = open("testporocilo.rtf", "w") 
file.write("Poročilo delovnih ur za Tatjana Lovrec od datuma do datuma.\n\n\n\n")
 
for row in c:
	# print(skupaj)
	counter2 +=1
	# print(counter2)
	if(row[4]=="prihod" and counterTip==0):
		dateprihod=row[3]
		counterTip=1
		dan= dnevi_tedna(row[3].weekday())
		msg0=str(counter3)+" "+str(row[3])+ " "+str(dan)+" "+str(row[4]+"\n")
		print(msg0)
		file.write(msg0)

	elif(row[4]=="odhod" and counterTip==1):
		counterTip=0
		dateodhod=row[3]
		msg=dateodhod-dateprihod
		counter3 +=1
		dan= dnevi_tedna(row[3].weekday())
		msg1= "  "+str(row[3])+" "+str(dan)+" "+ str(row[4])+ "   Delovne ure:"+ str(msg)+"\n\n" 
		print(msg1)
		file.write(msg1) 


		skupaj=skupaj+msg
	elif(row[4]=="odhod" and counterTip==0 and counter2==1):
		continue
	else:
		napaka_sporocilo=str(row[0])
		print("napaka pri vrsti", row[0] )
		break

		
	
izracun = skupaj-datetime(1,1,1,0,0,0,0)
print(msg,"\n")
print(izracun)
print(int(izracun.seconds/3600 +izracun.days*24) )
vsota = str(izracun.seconds/3600 +izracun.days*24)
file.write("\n\n")
file.write("Vsota ur:")
file.write(vsota)


 
file.close() 
