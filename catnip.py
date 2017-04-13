import requests
import json
from collections import namedtuple

#===================API HEADERS + Course Names + Authentication====================
token = '1876~4zGcmCF0s4shtdLiasakdKVRn6bcZGl6Tkr42HqsuHMwh0wBF8Cf8vZMCyYyyN3s';
params = (
    ('access_token', token),
)
headers = {
    'Authorization': 'Bearer 1876~4zGcmCF0s4shtdLiasakdKVRn6bcZGl6Tkr42HqsuHMwh0wBF8Cf8vZMCyYyyN3s',
}

r = requests.get('https://canvas.instructure.com/api/v1/users/self/favorites/courses', headers=headers)
auth = requests.get('https://canvas.instructure.com/api/v1/courses', params=params)

#===================Getting Course ID====================
rawCourseResponse = str(r.text)
courseResponseList = json.loads(rawCourseResponse)
#print len(courseResponseList)
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
    #print CourseMap
    #print courseId
    #print sampleCourse['course_code']


#=================User Input Class====================

def let_user_pick(options):
    print("Please choose:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            element = options[i-1]
            print element
            return CourseMap.get(element)
    except:
        pass
    return None

#===================Canvas API stuff=====================
nameOfCourse = str(let_user_pick(courseCode))
print nameOfCourse
asmt = requests.get('https://canvas.instructure.com/api/v1/courses/'+ nameOfCourse +'/assignments/?per_page=200', headers=headers)
with open('data.txt', 'w') as outfile:
    json.dump(asmt.text, outfile)
#modlist = requests.get('https://canvas.instructure.com/api/v1/courses/18760000000050040/modules', headers=headers)
#print "Authentication Code:" + str(auth)
#=================Getting the Assignment ID==================
rawAsmtResponse = asmt.text
#print rawAsmtResponse
asmtResponseList = json.loads(rawAsmtResponse)
print len(asmtResponseList)
asmtId = []
asmtName = []

for x in range(0, len(asmtResponseList)):
    sampleAsmt = asmtResponseList[x]
    a = sampleAsmt['id']
    #print a
    asmtId.append(a)
    b = sampleAsmt['name']
    asmtName.append(b)

for i in range(0, len(asmtName)):
    print asmtName[i]
#print asmtId


#rawModResponse = modlist.text
#modResponseList = json.loads(rawModResponse)
