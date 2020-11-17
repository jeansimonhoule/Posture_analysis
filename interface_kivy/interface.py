import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import os
from pathlib import Path

class MainWindow(Screen):
    def analyseBtn(self):
        sm.current = "analyse"
    
    def mesureBtn(self):
        sm.current = "mesure"
    
    def referenceBtn(self):
        sm.current = "reference"

class AnalyseWindow(Screen):
    firstchoice = ObjectProperty(None)
    secondchoice = ObjectProperty(None)
    fichiers = ObjectProperty(list)
    confirmDate = ObjectProperty(None)
    dropdown = ObjectProperty(None)
    btnSession = ObjectProperty(None)
    

    def get_possible_file(self):
        path = Path(os.path.abspath(__file__)).parents[1].joinpath("SAVED_DATA")
        self.fichiers = os.listdir(path)
    
    def available_session(self,day):
        path = Path(os.path.abspath(__file__)).parents[1].joinpath("SAVED_DATA").joinpath(day)
        self.sessions = os.listdir(path)
    
    def on_pre_enter(self,*args):
        self.get_possible_file()
        

    def confirm_date_btn(self):
        print(self.confirmDate.text)
        if self.confirmDate.text in self.fichiers:
            self.available_session(self.confirmDate.text)
            self.firstchoice.text = self.sessions[0]
            self.secondchoice.text = self.sessions[1]
            self.btnSession.background_color = 0,1,0,1
            #self.dropdown.open(self.btnSession)
        
        else:
            invalidFile()
    
    def lancer_analyse_btn(self):
        self.selected_session = (self.confirmDate.text,self.btnSession.text)
        print(self.selected_session)
        

        
        
    

    
    



class ResultWindow(Screen):
    pass

class MesureWindow(Screen):
    pass

class ReferenceWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


def invalidFile():
    pop = Popup(title='Date invalide',
    content=Label(text="Vérifier le format de la date"+'\n'+"Ou sinon vous avez pas fait de mesure ce jour la"),
    size_hint=(None, None), size=(400, 200))
    pop.open()



kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [MainWindow(name="main"), AnalyseWindow(name="analyse"),ResultWindow(name="result"),MesureWindow(name="mesure"),ReferenceWindow(name="reference")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "result"

class Posture_AnalysisApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    Posture_AnalysisApp().run()