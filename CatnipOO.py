import requests
import json
from Keys import caesarKey
from Keys import token
from Keys import headers

class Canvas:

    def __init__(self):


    def pullcourses(self):


    def pullassignments(self):


class Caesar:

    #def __init__(self):

    def pullterms(self):
        response = requests.get('http://api.asg.northwestern.edu/terms/', params=caesarKey)
        terms = response.json()
        return terms

    def pullschedule(self):
        classSch = []
        terms = self.pullterms()
        caesarDetails = Canvas.getname()
        for course in caesarDetails:
            courses = caesarKey
            for i in terms:
                # Converting both canvas and caesar term to same format
                termYear, termQuarter = i[u'name'].split(' ')
                termQuarter = termQuarter.upper()
                courseYear = course[0][0:4]
                courseQuarter = course[0][4:6]
                # Check for term id
                print courseYear, courseQuarter, termYear, termQuarter
                if courseYear == termYear and termQuarter[0:2] == courseQuarter:
                    courses['term'] = i[u'id']
                    break
            courses['subject'] = course[1]
            courses['catalog_num'] = course[2]
            response = requests.get('http://api.asg.northwestern.edu/courses/', params=courses)
            counter = 0
            while counter == 0:
                for i in response.json():
                    tempClass = i
                    print tempClass
                    if i[u'room'] is None:
                        print i[u'subject'] + ' ' + i[u'catalog_num'] + ' ' + i[u'section'] + ' : ' + i[
                            u'meeting_days'] + ' at ' + "Room NOT Specified" + \
                            ' from ' + i[u'start_time'] + ' to ' + i[u'end_time']
                    else:
                        print i[u'subject'] + ' ' + i[u'catalog_num'] + ' ' + i[u'section'] + ' : ' + i[
                            u'meeting_days'] + ' at ' + \
                            i[u'room'] + ' from ' + i[u'start_time'] + ' to ' + i[u'end_time']
                    a = raw_input('Is this the correct class?\r\nIf yes, enter y : ')
                    if a == 'y':
                        classSch.append(i)
                        counter = 1
                        break
        return classSch

class DataEntry:

    def __init__(self):


class CheckCourse:

    def checkcourses(self):


class CheckTerm:

    def checkterm(self):


class PriorityView:


class ListView:


class CalendarView:


class AddTask:

    def __init__(self):
        

    def addtask(self):
