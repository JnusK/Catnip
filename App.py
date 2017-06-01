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
import pytz
import dateutil.parser
import dateutil.tz

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

class PriorityView(GridLayout):
    def __init__(self, **kwargs):
        super(PriorityView, self).__init__(**kwargs)
        self.cols = 4
        self.rows = 5
        taskCount = 0
        tasks = []
        counter = 0
        requestedList = ChangeJSON().openjson("assignments.json")
        for task in requestedList:
            #something is wrong with the 'has_submitted_submissions', it is not reading boolean
            if 'has_submitted_submissions' != True:
                print task['name']
                if 'start' in task:
                    if task['start'][-1] == 'Z':
                        taskDT = dateutil.parser.parse(task['start'])
                    elif task['start'][-6] == '+':
                        dtParse = dateutil.parser.parse(task['start'])
                        taskDT = dtParse.astimezone(pytz.utc)
                    elif task['start'][-3] == '-':
                        dtParse = dateutil.parser.parse(task['start'])
                        taskDT = pytz.utc.localize(dtParse)
                    else:
                        dtParse = dateutil.parser.parse(task['start'])
                        taskDT = pytz.utc.localize(dtParse)

                elif 'due_at' in task and task['due_at'] != None:
                    if task['due_at'][-1] == 'Z':       #For tasks with timezone at UTC
                        #datetime.datetime.strptime does not make aware datetime
                        #taskDT = datetime.datetime.strptime(task['due_at'], '%Y-%m-%dT%H:%M:%SZ')
                        #dateutil.parser.parse makes aware datetime
                        taskDT = dateutil.parser.parse(task['due_at'])
                    elif task['due_at'][-6] == '+':     #For tasks with other timezones
                        #dt = task['due_at'][:19]
                        #taskDT = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
                        dtParse = dateutil.parser.parse(task['due_at'])
                        taskDT = dtParse.astimezone(pytz.utc)
                    elif task['due_at'][-3] == '-': #Detect tasks with no timezone and time
                        dtParse = dateutil.parser.parse(task['due_at'])
                        taskDT = pytz.utc.localize(dtParse)
                    else:   #Detect tasks with no timezone
                        dtParse = dateutil.parser.parse(task['due_at'])
                        taskDT = pytz.utc.localize(dtParse)
                #Get current aware datetime
                now = datetime.datetime.now(dateutil.tz.tzlocal())
                awareTask = taskDT.astimezone(pytz.utc)
                difference = awareTask - now
                print difference
                if difference < datetime.timedelta(days=5) and difference > datetime.timedelta(days=0):
                    tasks.append(task)
                    counter = counter + 1
        Button.background_color = 1, 0.8, 1, 1
        self.add_widget(Button(text=str(now.day)))
        Button.background_color = 1, 0.8, 1, 0.5
        self.add_widget(Button(text=str((now + datetime.timedelta(days=1)).day)))
        self.add_widget(Button(text=str((now + datetime.timedelta(days=2)).day)))
        self.add_widget(Button(text=str((now + datetime.timedelta(days=3)).day)))
        Label.background_color = 0, 0, 0, 0
        for x in range(8-counter/2):
            self.add_widget(Label(text=' '))
        for item in tasks:
            if item['category'] == 0:
                Button.background_color = 1, 0, 0, 1
            elif item['category'] == 1:
                Button.background_color = 0, 0, 1, 1
            else:
                Button.background_color = 1, 0.5, 0.25, 1
            self.add_widget(Button(text=item['name']))
        for x in range(8-counter/2):
            self.add_widget(Label(text=' '))




class CatnipApp(App):

    def build(self):
        #calendar = CalendarView()
        #Clock.schedule_interval(calendar.update, 86400)
        #return calendar
        priority = PriorityView()
        return priority

if __name__ == '__main__':
    CatnipApp().run()
