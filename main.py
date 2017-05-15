from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from example import PongGame
from CatnipOO import PullCanvas

class HBoxWidget(Widget):
    def __init__(self, **kwargs):
        super(HBoxWidget, self).__init__(**kwargs)

        #h1=Button(text="hi", size_hint_y=None, height=100, pos=(500, 500))
        #self.add_widget(h1)
        #self.add_widget(Button(text="hey", size_hint_y=None, height=100))

        asmts = PullCanvas()
        AssignmentList = asmts.getassignmentname()
        self.orientation = "vertical"
        self.pos=(0,100)
        listview = self.createListView(AssignmentList)
        print VBoxWidget
        self.add_widget(listview)

    def createListView(self, inputArray):
        layout = GridLayout(cols=1, spacing=0, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for elem in inputArray:
            btn = Button(text=str(elem), size_hint_y=None, height=100)
            layout.add_widget(btn)
        root = ScrollView(size_hint=(1, None), size=(1600, 1000), pos=(0, 100))
        root.add_widget(layout)
        return root
        #runTouchApp(root)

class VBoxWidget(Widget):
    def __init__(self, **kwargs):
        super(VBoxWidget, self).__init__(**kwargs)

        b1 = ToggleButton(text="priority", size_hint_y=None, height=100,  pos=(0, 0), width=400, group="menu", background_color=(1, 0, 1, 0.5))
        b2 = ToggleButton(text="listview", size_hint_y=None, height=100,  pos=(400, 0), width=400, group="menu", state="down")
        b3 = ToggleButton(text="monthly", size_hint_y=None, height=100,  pos=(800, 0), width=400, group="menu")
        b4 = ToggleButton(text="settings", size_hint_y=None, height=100,  pos=(1200, 0), width=400, group="menu")
        self.add_widget(b1)
        self.add_widget(b2)
        self.add_widget(b3)
        self.add_widget(b4)
        #menubar = self.addMenuBar()
        #self.add_widget(menubar)

class TopBarWidget(Widget):
    def __init__(self, **kwargs):
        super(TopBarWidget, self).__init__(**kwargs)





class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        self.add_widget(HBoxWidget())
        self.add_widget(VBoxWidget())



class TestApp(App):
    def build(self):
        return ContainerBox()

if __name__ == '__main__':
    TestApp().run()
