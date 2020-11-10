import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window

class MainWindow(Screen):
    pass

class AnalyseWindow(Screen):
    pass

class MesureWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class FullImage(Image):
    pass

kv = Builder.load_file("my.kv")

class Posture_AnalysisApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    Posture_AnalysisApp().run()