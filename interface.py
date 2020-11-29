import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

import os
import json
from pathlib import Path
from accelerometer import Accelerometer
from threading import Thread
from data_analysis import Data




class MainWindow(Screen):
    pass

class AnalyseWindow(Screen):
    """firstchoice = ObjectProperty(None)
    secondchoice = ObjectProperty(None)"""
    fichiers = ObjectProperty(list)
    confirmDate = ObjectProperty(None)
    dropdown = ObjectProperty(None)
    btnSession = ObjectProperty(None)
    selected_session = ObjectProperty(None)
    
    def on_pre_enter(self,*args):
        self.get_possible_file()

    def get_possible_file(self):
        path = Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA")
        self.fichiers = os.listdir(path)
    
    def available_session(self,day):
        path = Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA").joinpath(day)
        self.sessions = os.listdir(path)

    def confirm_date_btn(self):
        print(self.confirmDate.text)
        if self.confirmDate.text in self.fichiers:
            self.available_session(self.confirmDate.text)
            self.create_dropdown()
            self.btnSession.background_color = 0,1,0,1
        
        else:
            invalidFile()

    def create_dropdown(self):
        self.dropdown = DropDown()
        for session in self.sessions:
            btn = Button(text= session, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.btnSession.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.btnSession, 'text', x))
    

    def lancer_analyse_btn(self):
        self.selected_session = (self.confirmDate.text,self.btnSession.text)
        data = Data(self.selected_session[1],self.selected_session[0])
        data.analyze_my_data()


class ResultWindow(Screen):
    source1 = ObjectProperty(None)
    source2 = ObjectProperty(None)
    dropdown2 = ObjectProperty(None)
    analyse = ObjectProperty()
    btnResult = ObjectProperty(None)

    
    def on_enter(self):
        print("x:", self.analyse.selected_session)
        self.path = Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA").joinpath(self.analyse.selected_session[0]).joinpath(self.analyse.selected_session[1])
        self.source1.source = str(self.path.joinpath('result1.png'))
        self.source2.source = str(self.path.joinpath('result2.png'))
        self.available_time()
        self.create_dropdown()

    def available_time(self):
        with open(self.path.joinpath('times.json'), 'r') as f:
            self.times = json.load(f)


    def create_dropdown(self):
        self.dropdown2 = DropDown()
        for time in self.times:
            btn = Button(text= time, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown2.select(btn.text))
            self.dropdown2.add_widget(btn)
        self.btnResult.bind(on_release=self.dropdown2.open)
        self.dropdown2.bind(on_select=lambda instance, x: self.display_posture(x))

    def display_posture(self,x):
        setattr(self.btnResult,'text',x)
        self.source2.source = str(Path(os.path.abspath(__file__)).parent.joinpath("posture_img").joinpath('bleu.png'))

    

class MesureWindow(Screen):
    mesureState = ObjectProperty(None)
    acc = Accelerometer()
    def mesure_Btn(self):
        t2 = Thread(target=self.acc.save_data)
        t2.start()
        self.mesureState.text = "Session démarré!!!!! Bonne chance"


    
    



class ReferenceWindow(Screen):
    count = NumericProperty(30) # countdown de 30 secondes
    referenceLabel = ObjectProperty(None)
    #progBar = ObjectProperty(None)
    capteur_ref = Accelerometer()

    #click est zéro lorsque on entre sur la page
    def on_enter(self):
        self.click = 0

    #création d'un thread afin de ne pas freeze le GUI
    def getRef_btn(self):
        self.click += 1
        if self.click <= 1:
            self.countdown()
            t = Thread(target=self.capteur_ref.save_reference)
            t.start()
        else:
            pass

    def countdown(self):
        self.event = Clock.schedule_interval(self.update_label,1)

    def update_label(self,time_limit):
        self.referenceLabel.text = str(self.count)
        self.count = self.count -1
        if self.count < 0:
            self.referenceLabel.text = "La référence est enregistrée"
            self.event.cancel()

    
class WindowManager(ScreenManager):
    pass


def invalidFile():
    pop = Popup(title='Date invalide',
    content=Label(text="Vérifier le format de la date"+'\n'+"Ou sinon vous avez pas fait de mesure ce jour la"),
    size_hint=(None, None), size=(400, 200))
    pop.open()




kv = Builder.load_file("my.kv")

#sm = WindowManager()


class Posture_AnalysisApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    Posture_AnalysisApp().run()

