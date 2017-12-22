import kivy 
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
import db_functions as dbf


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
	#Vnos v db
	def vnos_v_db(self):
		ime_v = self.ime_iz_vnosa.text
		datum_v = self.datum_iz_vnosa.text
		prihod_v = self.prihod_iz_vnosa.text
		odhod_v = self.odhod_iz_vnosa.text
		print(ime_v, datum_v, prihod_v, odhod_v)

	def iskanje(self):

		ime_i = self.ime_iskanje.text
		datumiod = self.datumod_iskanje.text
		datumido = self.datumdo_iskanje.text
		datumvod = self.datumvod_iskanje.text
		datumvdo = self.datumvdo_iskanje.text
		print(ime_i, datumiod, datumido, datumvod, datumido) 




class DelovneUreApp(App):
	def build(self):
		return DelovneUre()


UreApp = DelovneUreApp()
UreApp.run()