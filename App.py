import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from datetime import datetime
import calendar

class CalendarView(GridLayout):

    def __init__(self, **kwargs):
        super(CalendarView, self).__init__(**kwargs)
        self.cols = 7
        self.rows = 7
        #Need to start frommonday due to calendar class in python starting on Mon in week in default
        #Might be changeable but not worth the effort
        self.add_widget(Label(text='Mo', height = 50))
        self.add_widget(Label(text='Tu', height = 50))
        self.add_widget(Label(text='We', height = 50))
        self.add_widget(Label(text='Th', height = 50))
        self.add_widget(Label(text='Fr', height = 50))
        self.add_widget(Label(text='Sa', height = 50))
        self.add_widget(Label(text='Su', height = 50))
        #Check number of days in a month
        if datetime.now().month == 1 or datetime.now().month == 3 or datetime.now().month == 5 or datetime.now().month == 7 or datetime.now().month == 8 or datetime.now().month == 10 or datetime.now().month == 12:
            noDay = 31
        else:
            noDay = 30
        #Check which day is 1st of month
        days = calendar.monthrange(datetime.now().year,datetime.now().month)
        #Add blank index as Kivy Grid does not allow widget to be placed in particular column/row
        for day in range(days[0]):
            self.add_widget(Label(text = ' '))
        #Add the dates to the calendar
        for date in range(noDay):
            self.add_widget(Label(text = str(date+1)))


class CatnipApp(App):

    def build(self):
        calendar = CalendarView()
        #Clock.schedule_interval(calendar.update, 86400)
        return calendar

if __name__ == '__main__':
    CatnipApp().run()
