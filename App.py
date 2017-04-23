import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.event import EventDispatcher

from CatnipOO import ChangeJSON

import datetime
import calendar

#Builder.load_file('CalendarView.kv')

class CalendarView(GridLayout):

    def __init__(self, **kwargs):
        super(CalendarView, self).__init__(**kwargs)
        mth = datetime.datetime.now().month
        year = datetime.datetime.now().year
        self.cols = 7
        self.rows = 8
        #Need to start frommonday due to calendar class in python starting on Mon in week in default
        #Might be changeable but not worth the effort
        self.add_widget(Button(text='<'))
        self.add_widget(Label(text=' '))
        self.add_widget(Label(text=' '))
        self.add_widget(Label(text=calendar.month_name[mth]))
        self.add_widget(Label(text=' '))
        self.add_widget(Label(text=' '))
        self.add_widget(Button(text='>'))
        self.add_widget(Label(text='Mo', height = 30))
        self.add_widget(Label(text='Tu', height = 30))
        self.add_widget(Label(text='We', height = 30))
        self.add_widget(Label(text='Th', height = 30))
        self.add_widget(Label(text='Fr', height = 30))
        self.add_widget(Label(text='Sa', height = 30))
        self.add_widget(Label(text='Su', height = 30))
        #Check number of days in a month
        if datetime.datetime.now().month == 1 or datetime.datetime.now().month == 3 or datetime.datetime.now().month == 5 or datetime.datetime.now().month == 7 or datetime.datetime.now().month == 8 or datetime.datetime.now().month == 10 or datetime.datetime.now().month == 12:
            noDay = 31
        else:
            noDay = 30
        #Check which day is 1st of month
        days = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)
        #Add blank index as Kivy Grid does not allow widget to be placed in particular column/row
        for day in range(days[0]):
            self.add_widget(Label(text = ' '))
        intensityList = ChangeJSON().openjson("intensity.json")
        #Add the dates to the calendar
        tmpYear = intensityList.get(str(year))
        if int(mth) < 10:
            tmpMth = tmpYear.get('0'+str(mth))
        else:
            tmpMth = tmpYear.get(str(mth))
        print tmpMth
        for date in range(noDay):
            #set color for intensity of work
            #Make a JSON that has the color for each date and when calendar is open, pull color info from that file
            if date < 9:
                strdate = '0' + str(date+1)
            else:
                strdate = str(date+1)
            if strdate in tmpMth:
                intensity = tmpMth[str(strdate)]
                if intensity < 3:
                    Button.background_color = 1, 0.8, 1, 1
                elif intensity < 5:
                    Button.background_color = 0.8, 0, 1, 1
                elif intensity > 5:
                    Button.background_color = 0.4, 0.2, 4, 1
            else:
                Button.background_color = 1, 1, 1, 1
            #Button.color = 0, 1, 0, 1
            self.add_widget(Button(text = strdate))



class CatnipApp(App):

    def build(self):
        calendar = CalendarView()
        #Clock.schedule_interval(calendar.update, 86400)
        return calendar

if __name__ == '__main__':
    CatnipApp().run()
