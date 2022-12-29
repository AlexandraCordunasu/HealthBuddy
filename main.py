import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

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
        
        
GUI = Builder.load_file("main.kv")
# IN LOC DE MAINAPP
class MyApp(App):
    def build(self):
        return GUI
    def change_screen(self,screen_name):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name
    
if __name__ == "__main__":
    MyApp().run()