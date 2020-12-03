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

class UserWindow(Screen):
    pass

class AnalyseWindow(Screen):
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

    def on_leave(self):
        self.confirmDate.text = ""
        self.btnSession.text = "session"
        self.btnSession.background_color = 0.05,0.25,0.5,1


class ResultWindow(Screen):
    source1 = ObjectProperty(None)
    source2 = ObjectProperty(None)
    dropdown2 = ObjectProperty(None)
    analyse = ObjectProperty()
    btnResult = ObjectProperty(None)
    hourLabel = ObjectProperty(None)
    resultLabel= ObjectProperty(None)

    
    def on_enter(self):
        print("x:", self.analyse.selected_session)
        self.path = Path(os.path.abspath(__file__)).parent.joinpath("SAVED_DATA").joinpath(self.analyse.selected_session[0]).joinpath(self.analyse.selected_session[1])
        self.resultLabel.text="[color=330000]Good! \nYour posture was as good as tonymass9![/color]"
        self.source1.source = str(self.path.joinpath('result1.png'))
        self.available_time()
        self.get_posture()
        self.create_dropdown()
        self.source2.source =  str(Path(os.path.abspath(__file__)).parent.joinpath("posture_img").joinpath(self.postures[self.times[0]]+".png"))
        setattr(self.hourLabel,'text',"[color=3333ff]"+self.times[0]+"[/color]")

    def available_time(self):
        with open(self.path.joinpath('times.json'), 'r') as f:
            self.times = json.load(f)

    def get_posture(self):
        with open(self.path.joinpath('postures.json'), 'r') as f:
            self.postures = json.load(f)

    def create_dropdown(self):
        self.dropdown2 = DropDown()
        for time in self.times:
            btn = Button(text= time, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown2.select(btn.text))
            self.dropdown2.add_widget(btn)
        self.btnResult.bind(on_release=self.dropdown2.open)
        self.dropdown2.bind(on_select=lambda instance, x: self.display_posture(x))

    def display_posture(self,x):
        #setattr(self.btnResult,'text',x)
        self.source2.source = str(Path(os.path.abspath(__file__)).parent.joinpath("posture_img").joinpath(self.postures[x]+".png"))
        setattr(self.hourLabel,'text',"[color=3333ff]"+x+"[/color]")
    

class MesureWindow(Screen):
    mesureState = ObjectProperty(None)
    acc = Accelerometer()
    analysisBtn = ObjectProperty(None)
    analyse = ObjectProperty(None)

    def on_enter(self):
        self.click  = 0

    def mesure_Btn(self):
        self.click+=1
        if self.click == 1 :
            t2 = Thread(target=self.acc.save_data)
            t2.start()
            self.mesureState.text = "Currently analysing your posture..."
            self.analysisBtn.text = "Stop analysis"
            self.analysisBtn.background_color = (1,0,0,1)

        if self.click ==2 :
            self.acc.stop = True
            self.mesureState.text = "Posture analysis has been stopped"
            self.analysisBtn.text = "See the results"
            self.analysisBtn.background_color = (0,0,0,1)

        if self.click == 3 : 
            self.analyse.get_possible_file()
            day = self.acc.date
            self.analyse.available_session(day)
            session = self.analyse.sessions[-1]
            self.analyse.confirmDate.text = day
            self.analyse.btnSession.text = session
            self.analyse.btnSession.background_color = 0,1,0,1
            kv.current = "analyse"

    
class WindowManager(ScreenManager):
    pass


def invalidFile():
    pop = Popup(title='Date invalide',
    content=Label(text="Vérifier le format de la date"+'\n'+"Ou sinon vous avez pas fait de mesure ce jour la"),
    size_hint=(None, None), size=(400, 200))
    pop.open()



kv = Builder.load_file("my.kv")


class Posture_AnalysisApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    Posture_AnalysisApp().run()

