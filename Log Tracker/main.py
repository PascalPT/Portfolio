import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.config import Config
from kivy.utils import platform
#from kivy.uix.screenmanager import Screen
import os.path


Config.read(str(os.path.join(os.path.expanduser('~'), 'myApp.ini')))
Config.set('kivy','keyboard_mode','system')
Config.write()

if platform in ('lin','win','mac'):
    Window.maximize()
else:
    Window.fullscreen = True

Window.clearcolor = (0, 0, 0, 1)

class ImportPopup(Popup):
    pass
class ExportPopup(Popup):
    pass
class CleanPopup(Popup):
    pass
class SearchPopup(Popup):
    pass

class Pop_FloatLayout(FloatLayout):
    def OpenPopup(self,window):
        if window == "Import":
            WindowScreen = ImportPopup()
        elif window == "Export":
            WindowScreen = ExportPopup()
        elif window == "Clean":
            WindowScreen = CleanPopup()
        elif window == "Search":
            WindowScreen = SearchPopup()
        WindowScreen.open()

class ManagerApp(App):
    def build(self):
        return Pop_FloatLayout()

Manager = ManagerApp()
Manager.run()
