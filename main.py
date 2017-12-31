from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '990')
Config.set('graphics', 'resizable', False)
import kivy 
kivy.require("1.9.0")
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
import datetime
import db_functions
import sqlite3



class PrikazListButton(ListItemButton):
    pass

class UpdatePopup():
	pass

class DelovneUre(BoxLayout):
	#Spremenljivke razreda
	ime_iz_vnosa = ObjectProperty()
	datum_iz_vnosa = ObjectProperty()
	prihod_iz_vnosa = ObjectProperty()
	odhod_iz_vnosa = ObjectProperty()

	ime_iskanje = ObjectProperty()
	datumod_iskanje = ObjectProperty()
	datumdo_iskanje = ObjectProperty()
	datumvod_iskanje = ObjectProperty()
	datumvdo_iskanje = ObjectProperty()
	dbprikaz = ObjectProperty()
	#Vnos v db
	def vnos_v_db(self):
		ime_v = self.ime_iz_vnosa.text
		datum_v = self.datum_iz_vnosa.text
		prihod_v = self.prihod_iz_vnosa.text
		odhod_v = self.odhod_iz_vnosa.text
		db_functions.input_db(ime_v, datum_v, prihod_v, odhod_v)
		self.vnos_msg.text = "VNOS USTVARJEN za {} dan {} cas od {} do {}. Čas vnosa {}".format(ime_v, datum_v, prihod_v, odhod_v, datetime.datetime.now())

	def iskanje(self): 

		conn = sqlite3.connect('example.db')
		c = conn.cursor()
		name = self.ime_iskanje.text
		od = self.datumod_iskanje.text
		do = self.datumdo_iskanje.text
		result = c.execute('SELECT rowid, ime, datum, prihod, odhod, ure_skupaj, datum_vnosa FROM ure_zaposlenih WHERE ime=? AND datum BETWEEN ? AND ? ORDER BY datum', (name, od, do))
		self.dbprikaz.adapter.data.clear()
		for row in result:

			rowid = row[0]
			ime = row[1]
			datum = row[2]
			prihod = row[3]
			odhod = row[4]
			ure_skupaj = row[5]
			datum_vnosa = row[6]
			# Get the students name from textinput
			vrstica = ' ' + str(rowid) + '| Ime: |' + ime + '| Datum: |' + str(datum) + '| Prihod: |' + str(prihod) + '| Odhod: |' + str(odhod) + '| Ure dela: |' + str(ure_skupaj) + '|-----Datum vnosa---|: ' + str(datum_vnosa)

			#Add to list view

			self.dbprikaz.adapter.data.extend([vrstica])

		#Reset list view
		
		self.dbprikaz._trigger_reset_populate()

		
		conn.close()

	def delete_item(self, *args):
 
        # If a list item is selected
        
		if self.dbprikaz.adapter.selection: 
            # Get the text from the item selected
			selection = self.dbprikaz.adapter.selection[0].text
			sel = selection.split(' ')
			print(sel[1])
			rid = sel[1]
			db_functions.delete_entry(rid)
			self.dbprikaz.adapter.data.remove(selection)

	def clear_list(self):
		#Clearing list view.
		empty = '..List CLeared..'
		self.dbprikaz.adapter.data.clear()
		self.dbprikaz.adapter.data.extend([empty])
		self.dbprikaz._trigger_reset_populate()
		
class DelovneUreApp(App):
	def build(self):
		return DelovneUre()


UreApp = DelovneUreApp()
UreApp.run()