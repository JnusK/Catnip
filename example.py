from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from CatnipOO import PullCanvas


class PongGame(BoxLayout):

    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(PongGame, self).__init__(**kwargs)

        asmts = PullCanvas()
        AssignmentList = asmts.getassignmentname()
        self.orientation = "vertical"
        self.createListView(AssignmentList)

    def createListView(self, inputArray):
        layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for elem in inputArray:
            btn = Button(text=str(elem), size_hint_y=None, height=100)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        runTouchApp(root)


class PongApp(App):
    def build(self):
        return PongGame()



if __name__ == '__main__':
    PongApp().run()
