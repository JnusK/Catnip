import requests
import json
from Keys import caesarKey
from Keys import token
from Keys import headers

class PullCanvas:
    def __init__(self):
        self.courseName1 = x

    def pullcourses(self):
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

    def getName(self):
        return courseCode


class Caesar:

    def __init__(self):


    def pullterms(self):


    def pullschedule(self):


class DataEntry:

    def __init__(self):


class CheckCourse:

    def checkcourses(self):


class CheckTerm:

    def checkterm(self):
