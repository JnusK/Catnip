import requests
import json
import itertools
from Keys import caesarKey
from Keys import token
from Keys import headers

class PullCanvas:
    def __init__(self):
        self.courseName1 = x

    def pullcourses(self):
        #pull courses from Canvas 
        auth = requests.get('https://canvas.instructure.com/api/v1/courses', params=params)
        r = requests.get('https://canvas.instructure.com/api/v1/users/self/favorites/courses', headers=headers)
        if auth != 200 or "200"
            raise RuntimeError("Canvas Authorization Failed")
        rawCourseResponse = str(r.text)
        courseResponseList = json.loads(rawCourseResponse)

        courseId = []
        courseCode = []

        for x in range(0, len(courseResponseList)):
            sampleCourse = courseResponseList[x]
            d = sampleCourse['id']
            c = sampleCourse['course_code']
            courseId.append(d)
            courseCode.append(c)
            ICourseMap = dict(zip(courseId, courseCode))
            CourseMap = {v: k for k, v in ICourseMap.iteritems()}

        print CourseMap.keys()


    def pullassignments(self):
        #pull assignments
        
    def getName(self):
        #get name of courses from JSON file
        return courseCode

    def comparecourses(self):
        #compare courses in JSON file with newly pulled courses to see if there is any changes and return a boolean
        return change
    
    def compareassignment(self):
        #compare assignments in JSON dile with newly pulled assignments and return a boolean 
        return change

class Caesar:

    #def __init__(self):


    def pullterms(self):
        response = requests.get('http://api.asg.northwestern.edu/terms/', params=caesarKey)
        terms = response.json()
        return terms

    def pullschedule(self):
        classSch = []
        # Pull terms from CAESAR to match the terms of courses from CANVAS
        terms = self.pullterms()
        courseCode = Canvas.getname()

        for course in courseCode:
            courses = caesarKey
            caesarDetails = course.split('_')
            for i in terms:
                # Converting both canvas and caesar term to same format
                termYear, termQuarter = i[u'name'].split(' ')
                termQuarter = termQuarter.upper()
                courseYear = caesarDetails[0][0:4]
                courseQuarter = caesarDetails[0][4:6]
                # Check for term id
                print courseYear, courseQuarter, termYear, termQuarter
                if courseYear == termYear and termQuarter[0:2] == courseQuarter:
                    courses['term'] = i[u'id']
                    break
            courses['subject'] = caesarDetails[1]
            courses['catalog_num'] = caesarDetails[2]
            courses['section'] = caesarDetails[3][3:]
            # API call uses 4 fields to narrow down search (term, subject, catalog_num and section)
            response = requests.get('http://api.asg.northwestern.edu/courses/', params=courses)
            cls = response.json()
            #Removing keys not needed from dictionary of course
            for ele in cls:
                del ele[u'topic']
                del ele[u'seats']
                del ele[u'course_id']
                del ele[u'class_num']
                del ele[u'id']
            classSch.append(cls)
        with open('classSch.txt', 'w') as outfile:
            json.dump(cSch, outfile)

    def getSchedule(self):
        #Pseudocode
        if Database is None:
            self.pullschedule()
            #copy into DB
            return Schedule
        else:
            return Schedule

class DataEntry:

    def adddata(self):
        pass
    
class DeleteTask:

    def deletetask(self):
        pass

class CheckCourse:

    def checkcourses(self):


class CheckTerm:
#Seems like it is useless now that I integrated it into Caesar.pullSchedule
    def checkterm(self):


class PriorityView:


class ListView:


class CalendarView:


class AddTask:

    def addtask(self):

class Task:

    def __init__(self, name, course_code, start_dt, end_dt, weightage, details, time_taken):
        self.name = name
        self.course_code = course_code
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.weightage = weightage
        self.details = details
        self.time_taken = time_taken

    def getname(self):
        return self.name

    def getcourse(self):
        return self.course_code

    def getstartdt(self):
        return self.start_dt

    def getenddt(self):
        return self.end_dt

    def getweightage(self):
        return self.weightage

    def getdetails(self):
        return self.details

    def gettimetaken(self):
        return self.time_taken

class CompleteTask:

    def completetask(self):
        #change end_dt to current dt
        #Stop stopwatch and record time taken
