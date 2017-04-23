import requests
import json
import itertools
import os.path
import datetime
import time
from Keys import caesarKey
from Keys import token
from Keys import headers


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

        #print courseId
        for x in range(0, len(courseId)):
            nameOfCourse = str(courseId[x])
            print nameOfCourse
            asmt = requests.get(
                'https://canvas.instructure.com/api/v1/courses/' + nameOfCourse + '/assignments/?per_page=200',
                headers=headers)
            #print asmt
            data = asmt.json()
            #print data

            rawAsmtResponse = asmt.text
            asmtResponseList = json.loads(rawAsmtResponse)
            data = asmtResponseList
            #print data
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

        return tempList

    def getcourseid(self):
        courses = ChangeJSON().openjson("courses.json")
        #print courses
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

    def getassignmentname(self):
        # return assignment name for UI manipulation
        asmt = ChangeJSON().openjson("assignments.json")
        asmtName = []
        for assignment in asmt:
            asmtName.append(assignment[u'name'])
        print asmtName
        return asmtName

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
        # compare assignments in JSON file with newly pulled assignments and return a boolean
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

    def appendjson(selfself, fileName, list):
        with open(fileName, 'a') as outfile:
            json.dump(list, outfile)

class PriorityView:
    pass


class ListView:
    pass


class CalendarView:
    pass


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
        courses = PullCanvas().pullcourses()
        ChangeJSON().writejson("courses.json", courses)
    if os.path.exists("./assignments.json") == False:
        assignments = PullCanvas().pullassignments()
        ChangeJSON().writejson("assignments.json", assignments)
    if os.path.exists("./classSch.json") == False:
        Caesar().pullschedule()


if __name__ == '__main__':
    main()
