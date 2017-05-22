import requests
import json
import itertools
import os.path
import datetime
import time
import httplib2
import os

from Keys import caesarKey
from Keys import token
from Keys import headers

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#for google calendar integration
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class PullCanvas:
    def pullcourses(self):
        # pull courses from Canvas and return list of courses, do not store to JSON in this method
        params = {
            ('access_token', token),
        }
        auth = requests.get('https://canvas.instructure.com/api/v1/courses', params=params)
        r = requests.get('https://canvas.instructure.com/api/v1/users/self/favorites/courses', headers=headers)
        if "200" not in str(auth):
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

        ChangeJSON().writejson("lastPull.json", int(time.time()))

        return CourseMap

    def pullassignments(self):
        # pull assignments
        tempList = []

        courseId = self.getcourseid()

        print courseId
        for x in range(0, len(courseId)):
            nameOfCourse = str(courseId[x])
            print nameOfCourse
            asmt = requests.get(
                'https://canvas.instructure.com/api/v1/courses/' + nameOfCourse + '/assignments/?per_page=200',
                headers=headers)
            print asmt
            data = asmt.json()
            print data

            rawAsmtResponse = asmt.text
            asmtResponseList = json.loads(rawAsmtResponse)
            data = asmtResponseList
            print data
            for element in data:
                del element['muted']
                del element['due_date_required']
                del element['submissions_download_url']
                del element['locked_for_user']
                del element['in_closed_grading_period']
                del element['html_url']
                del element['intra_group_peer_reviews']
                del element['secure_params']
                del element['submission_types']
                del element['created_at']
                del element['updated_at']
                del element['grade_group_students_individually']
                del element['anonymous_peer_reviews']
                del element['post_to_sis']
                del element['automatic_peer_reviews']
                del element['group_category_id']
                del element['omit_from_final_grade']
                del element['lock_at']
                del element['unlock_at']
                del element['position']
                del element['moderated_grading']
                del element['only_visible_to_overrides']
                del element['peer_reviews']
                del element['grading_standard_id']
                del element['assignment_group_id']
                del element['max_name_length']
                del element['published']
                del element['description']

                tempList.append(element)

        print tempList
        return tempList

    def getcourseid(self):
        courses = ChangeJSON().openjson("courses.json")
        # print courses
        courseID = []
        for course in courses:
            courseID.append(courses[course])
        return courseID

    def getcoursecode(self):
        # return course_code for CAESAR manipulation
        courses = ChangeJSON().openjson("courses.json")
        courseCode = []
        for course in courses:
            courseCode.append(course)
        return courseCode

    def comparecourses(self, newCourses):
        # compare courses in JSON file with newly pulled courses to see if there is any changes and return a boolean
        oldCourses = ChangeJSON().openjson("courses.json")

        if len(oldCourses) != len(newCourses):
            return True
        else:
            for i in oldCourses:
                for j in newCourses:
                    if i['courseId'] != j['courseId']:
                        return True
        return False

    def compareassignment(self, newAssignments):
        # compare assignments in JSON file with newly pulled assignments and return a list of new assignments
        oldAssignments = ChangeJSON().openjson("assignments.json")

        if len(oldAssignments) != len(newAssignments):
            return True
        else:
            for i in oldAssignments:
                for j in newAssignments:
                    if i['id'] != j['id']:
                        return True
        return False


class Caesar:

    def pullterms(self):
        #pull terms information from CAESAR
        response = requests.get('http://api.asg.northwestern.edu/terms/', params=caesarKey)
        if "200" not in str(response):
            raise RuntimeError("CAESAR Authorization Failed")
        terms = response.json()
        return terms

    def pullschedule(self):
        classSch = []
        # Pull terms from CAESAR to match the terms of courses from CANVAS
        terms = self.pullterms()
        courseCode = PullCanvas().getcoursecode()

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
                #print courseYear, courseQuarter, termYear, termQuarter
                if courseYear == termYear and termQuarter[0:2] == courseQuarter:
                    courses['term'] = i[u'id']
                    break
            courses['subject'] = caesarDetails[1]
            courses['catalog_num'] = caesarDetails[2]
            courses['section'] = caesarDetails[3][3:]
            # API call uses 4 fields to narrow down search (term, subject, catalog_num and section)
            response = requests.get('http://api.asg.northwestern.edu/courses/', params=courses)
            cls = response.json()
            # Removing keys not needed from dictionary of course
            for ele in cls:
                del ele[u'topic']
                del ele[u'seats']
                del ele[u'course_id']
                del ele[u'class_num']
                del ele[u'id']
            classSch.append(cls)
        # dumping class schedule to JSON file
        cSch = list(itertools.chain.from_iterable(classSch))
        ChangeJSON().writejson("classSch.json", cSch)

    def getSchedule(self):
        if os.path.exists("./classSch.json") == False:
            self.pullschedule()
        schedule = ChangeJSON().openjson("classSch.json")
        return schedule

class GoogleCalendar:

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def addevents(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        tasks = []
        credentials = GoogleCalendar().get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print (now)
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        print (events)

        if not events:
            print('No upcoming events found.')
        for event in events:
            task = {}
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            task[u'name'] = event['summary']
            # change timezone
            task[u'due_at'] = event['end'].get['dateTime']
            # change timezone
            task[u'start'] = event['start'].get['dateTime']
            tasks.append(task)
            flatTask = list(itertools.chain.from_iterable(task))
            ChangeJSON().appendjson("assignments.json", flatTask)

class DeleteTask:
    def deletetask(self):
        pass


class ChangeJSON:
    def openjson(self, fileName):
        with open(fileName) as json_data:
            requestedFile = json.load(json_data)
        return requestedFile

    def writejson(self, fileName, list):
        with open(fileName, 'w') as outfile:
            json.dump(list, outfile)

    def appendjson(self, fileName, list):
        with open(fileName, 'a') as outfile:
            json.dump(list, outfile)

class PriorityView:
    pass


class ListView:
    pass


class CalendarView:
    def setintensity(self):
        if os.path.exists("./intensity.json") == False:
            intensity = {}
            assignmentlist = ChangeJSON().openjson("assignments.json")
            for assignment in assignmentlist:
                if assignment[u'due_at'] != None:
                    year, mth, dateTemp = assignment[u'due_at'].split('-')
                    date = dateTemp[:2]
                    if year not in intensity:
                        intensity[year] = {mth: {}}
                    if mth not in intensity[year]:
                        intensity[year][mth] = {date: 0}
                    if date not in intensity[year][mth]:
                        intensity[year][mth][date] = 1
                    else:
                        intensity[year][mth][date] += 1
            ChangeJSON().writejson("intensity.json", intensity)


class AddTask:

    def addtask(self):
        pass


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

    def completetask(self):
        # change end_dt to current dt
        # Stop stopwatch and record time taken
        pass


def main():
    if os.path.exists("./courses.json") == False:
        ChangeJSON().writejson("courses.json", PullCanvas().pullcourses())
    if os.path.exists("./assignments.json") == False:
        ChangeJSON().writejson("assignments.json", PullCanvas().pullassignments())
    if os.path.exists("./classSch.json") == False:
        Caesar().pullschedule()
    #if PullCanvas().comparecourses(PullCanvas().pullcourses()) == True:
        #ChangeJSON().writejson("courses.json", PullCanvas().pullcourses())
        #Caesar().pullschedule()
    #if PullCanvas().compareassignment(PullCanvas().pullassignments()) == True:
        #append new assignments to old assignment list
    CalendarView().setintensity()


if __name__ == '__main__':
    main()