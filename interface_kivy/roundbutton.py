from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.base import runTouchApp

kv="""
<RoundedButton@Button>:
    background_color: 0,0,0,0  # the last zero is the critical on, make invisible
    canvas.before:
        Color:
            rgba: (.4,.4,.4,1) if self.state=='normal' else (0,.8,.7,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [50,]
"""
class RoundedButton(Button):
    pass

Builder.load_string(kv)

runTouchApp(RoundedButton(text="Hit Me!"))