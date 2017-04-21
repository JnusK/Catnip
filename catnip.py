import requests
import json
from collections import namedtuple
from Keys import token

#===================API HEADERS + Course Names + Authentication====================
token = '1876~4zGcmCF0s4shtdLiasakdKVRn6bcZGl6Tkr42HqsuHMwh0wBF8Cf8vZMCyYyyN3s';

params = (
    ('access_token', token),
)

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
    CourseMap = {v: k for k, v in ICourseMap.iteritems()} #flips coursemap

    #print courseId
    #print sampleCourse['course_code']
print CourseMap

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

print data
with open('assignments.txt', 'w') as outfile:
    json.dump(data, outfile)

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
