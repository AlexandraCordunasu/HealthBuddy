from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.app import App
import kivy.utils

class MyGrid(GridLayout):
    def __init__ (self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="First Name: "))
        self.name = TextInput(multiline=False)
        self.add_widget(self.name)

        self.add_widget(Label(text="Last Name: "))
        self.lastName = TextInput(multiline=False)
        self.add_widget(self.lastName)

        self.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.add_widget(self.email)

        self.add_widget(Label(text="Age: "))
        self.age = TextInput(multiline=False)
        self.add_widget(self.age)

        self.add_widget(Label(text="Height: "))
        self.height = TextInput(multiline=False)
        self.add_widget(self.height)

        self.add_widget(Label(text="Weight: "))
        self.weight = TextInput(multiline=False)
        self.add_widget(self.weight)

QUESTIONS = {
    "Sex M/F": [
        "masculin", "Feminin", "Prefer să nu spun"],
    "Cat de activ sunteți?": [
        "Stil de viață sedentar", "Activitate fizică medie", "Activitate fizică moderată", "Activitate fizică intensă-specifică antrenorilor și sportivilor"
    ],
    "Ce ideal aveți?": [
        "Slăbit","Luare in greutate","Mentinere"
    ],
    "Ce ati dori sa lucrati mai mult?" :[
        "Gambe","Coapse","Fesieri","Picioare","Abdomen","Piept","Spate","Biceps","Triceps","Umeri","Brate","Picioare"
    ],
    "Cate minute faceti sport pe zi?" : [
    "0 minute", "30 minute","45 minute","60 minute", "90 minute","120 minute","150 min","190 minute"
    ],
}



class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()
