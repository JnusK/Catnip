from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty


class PongGame(BoxLayout):

    '''def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(PongGame, self).__init__(**kwargs)

        list_view = ListView(item_strings=[str(index) for index in range(50)])

        self.add_widget(list_view)'''

        numbers = []
        for x in range(0, 10):
            numbers[x]= x



class PongApp(App):
    def build(self):
        return PongGame()



if __name__ == '__main__':
    PongApp().run()
