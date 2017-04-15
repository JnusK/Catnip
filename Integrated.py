import requests
import json
from collections import namedtuple

classSch = []

caesarKey = {
    'key' : 'BOGFWpQ90JmvNzrY',
}

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
term = []
subject = []
catNum = []
section = []
caesarDetails = []

for x in range(0, len(courseResponseList)):
    sampleCourse = courseResponseList[x]
    d = sampleCourse['id']
    c = sampleCourse['course_code']
    courseId.append(d)
    courseCode.append(c)
    ICourseMap = dict(zip(courseId, courseCode))
    CourseMap = {v: k for k, v in ICourseMap.iteritems()}
    print CourseMap
    print courseId
    print sampleCourse['course_code']

    #Getting Course Details for Caesar
    details = c.split('_')
    caesarDetails.append(details)

#===============Start of retrieving Class Schedule from CAESAR===========
print caesarDetails
response = requests.get('http://api.asg.northwestern.edu/terms/', params=caesarKey)
terms = response.json()
for course in caesarDetails:
    courses = {
        'key': 'BOGFWpQ90JmvNzrY',
        # 'class_num' : '31902',
        # 'term' : '4660',
        # 'subject' : 'EECS'
    }
    for i in terms:
        #Converting both canvas and caesar term to same format
        termYear, termQuarter = i[u'name'].split(' ')
        termQuarter = termQuarter.upper()
        courseYear = course[0][0:4]
        courseQuarter = course[0][4:6]
        #Check for term id
        print courseYear, courseQuarter, termYear, termQuarter
        if courseYear == termYear and termQuarter[0:2] == courseQuarter:
            courses['term'] = i[u'id']
            break
    courses['subject'] = course[1]
    courses['catalog_num'] = course[2]
    response = requests.get('http://api.asg.northwestern.edu/courses/', params=courses)
    print courses
    print response.json()
    #Have to include this loop due to 395 series of classes which share many same classes
    for i in response.json():
        tempClass = i
        print tempClass
        print i[u'subject'] + ' ' + i[u'catalog_num'] + ' ' + i[u'section'] + ' : ' + i[u'meeting_days'] + ' at ' + \
                i[u'room'] + ' from ' + i[u'start_time'] + ' to ' + i[u'end_time']
        a = raw_input('Is this the correct class?\r\nIf yes, enter y : ')
        if a == 'y':
            classSch.append(i)
            break

print classSch

#====================Main Menu==================================
def inputChoice():
    print 'Type a to view class schedule\r\nType b to display class assignment\r\nType q to quit'
    choice = raw_input('Choice : ')
    return choice


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
choice = inputChoice()
while choice != 'q' or choice != 'Q':
    if choice == 'a' or choice == 'A':
        print classSch
    if choice =='b' or choice == 'B':
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
    choice = inputChoice()
