from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
import kivy 
kivy.require("1.9.0")
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import kivy.uix.behaviors.focus
from kivy.clock import Clock
import datetime


class rfid_input(BoxLayout):
	input_rfid = ObjectProperty()
	izpis = ObjectProperty()
	focus1 = ObjectProperty()
	

	def izpisi(self):	
		Clock.schedule_once(self.focus_input)
	def focus_input(self, Clock):

		ime=self.input_rfid.text
		
		if(ime=="0005057807"):
			self.izpis.text = str(datetime.datetime.now()) + " Čas zabeležen. Pozdravljen Ben!"
			self.izpis.background_color = (0.0, 1.0, 0.0, 1.0)
		else:
			self.izpis.text = "Oseba ni prepoznana"
			self.izpis.background_color = (1.0, 0.0, 0.0, 1.0)
			

		self.input_rfid.text = ""
		self.input_rfid.focus = True


class rfid_inputApp(App):
	def build(self):
		return rfid_input()

rfidApp = rfid_inputApp()
rfidApp.run()
