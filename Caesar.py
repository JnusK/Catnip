import requests
from datetime import datetime
from Keys import caesarKey

classSch = []

'''
def f(x):
    return {
        'EECS' or 'eecs': 1,
        'DSGN' or 'dsgn': 2,
        'ENTREP' or 'entrep': 3,
        'd': 4
    }.get(x, 9)
'''

courses = {
    'key' : caesarKey['key'],
    #'class_num' : '31902',
    #'term' : '4660',
    #'subject' : 'EECS'
}

#response = requests.get('http://api.asg.northwestern.edu/courses/', params=courses)
# calling response.json() returns the response as a Python dictionary or list

def inputChoice():
    print 'Type a to add new course\r\nType d to display class schedule\r\nType q to quit'
    choice = raw_input('Choice : ')
    return choice

response = requests.get('http://api.asg.northwestern.edu/terms/', params=caesarKey)
#response = requests.get('http://api.asg.northwestern.edu/terms/', params=courses['key'])
print response.url
curDate = datetime.now()
print curDate
mth = curDate.month
day = curDate.day
terms = response.json()
print terms
termStart = terms[0][u'start_date']
y, m, d = termStart.split('-')
print y, m, d
if day >= d and mth >= m :
    curTerm = terms[0][u'id']
else:
    curTerm = terms[1][u'id']
print curTerm

choice = inputChoice()
while choice != 'q' or choice != 'Q':
    if choice == 'a' or choice == 'A':
        if day >= d and mth >= m:
            curTerm = terms[0][u'id']
            print("Only quarter available is " + terms[0][u'id'])
            courses['term'] = curTerm
        else:
            print("which quarter is it for : \r\na) " + terms[0][u'id'] + "\r\nb) " + terms[1][u'id'])
            term = raw_input('Enter letter : ')
            if term =='a' or 'A':
                courses['term'] = terms[0][u'id']
            else:
                courses['term'] = terms[1][u'id']
        sub = raw_input('Enter subject : ')
        sub = sub.upper()
        catNum = raw_input('Enter catalog number : ')
        courses['subject'] = sub
        response = requests.get('http://api.asg.northwestern.edu/courses/', params=courses)
        print response.json()

        for i in response.json():
            if i[u'catalog_num'].find(catNum) != -1:
                tempClass = i
                print i[u'subject'] + ' ' + i[u'catalog_num'] + ' ' + i[u'section'] + ' : ' + i[u'meeting_days'] + ' at ' + i[u'room'] + ' from ' + i[u'start_time'] + ' to ' + i[u'end_time']
                a = raw_input('Is this the correct class?\r\nIf yes, enter y : ')
                if a == 'y':
                    classSch.append(i)
                    break
    if choice == 'd' or choice == 'D':
        if len(classSch) == 0:
            print 'No classes'
        for cls in classSch:
            print cls[u'subject'] + ' ' + cls[u'catalog_num'] + ' : ' + cls[u'meeting_days'] + ' at ' + cls[u'room'] + ' from ' + cls[u'start_time'] + ' to ' + cls[u'end_time']

    choice = inputChoice()
