import requests
import json
import itertools
import os.path
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
        if auth != 200 or "200":
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

        return CourseMap

    def pullassignments(self):
        # pull assignments
        asmtList = []
        tempList = []

        for x in range(0, len(courseResponseList)):
            nameOfCourse = str(courseId[x])
            print nameOfCourse
            asmt = requests.get(
                'https://canvas.instructure.com/api/v1/courses/' + nameOfCourse + '/assignments/?per_page=200',
                headers=headers)
            rawAsmtResponse = asmt.text
            asmtResponseList = json.loads(rawAsmtResponse)
            data = asmtResponseList
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

    def getName(self):
        return courseCode

    def comparecourses(self, newCourses):
        # compare courses in JSON file with newly pulled courses to see if there is any changes and return a boolean
        oldCourses = ChangeJSON().openjson("courses.json")
        return change

    def compareassignment(self, newAssignment):
        # compare assignments in JSON dile with newly pulled assignments and return a boolean
        oldAssignments = ChangeJSON().openjson("assignments.json")
        return change



class Caesar:
    # def __init__(self):


    def pullterms(self):
        response = requests.get('http://api.asg.northwestern.edu/terms/', params=caesarKey)
        terms = response.json()
        return terms

    def pullschedule(self):
        classSch = []
        # Pull terms from CAESAR to match the terms of courses from CANVAS
        terms = self.pullterms()
        courseCode = PullCanvas().getname()

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


class DataEntry:
    def adddata(self):
        pass


class DeleteTask:
    def deletetask(self):
        pass


class CheckCourse:
    def checkcourses(self):
        pass


class ChangeJSON:
    def openjson(self, fileName):
        with open(fileName) as json_data:
            requestedFile = json.load(json_data)
        return requestedFile

    def writejson(self, fileName, list):
        with open(fileName, 'w') as outfile:
            json.dump(list, outfile)


class CheckTerm:
    # Seems like it is useless now that I integrated it into Caesar.pullSchedule
    def checkterm(self):
        pass


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


class CompleteTask:
    def completetask(self):
        # change end_dt to current dt
        # Stop stopwatch and record time taken
        pass


def main():
    pass


if __name__ == '__main__':
    main()
