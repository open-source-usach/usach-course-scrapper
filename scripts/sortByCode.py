import json

byNone = open('data.json', 'r', encoding='utf-8')
byFaculty = open('data.json', encoding='utf-8')
byCareer = open('ramosCarrera.json', encoding='utf-8')
allCoursesFile = open('allCourses.json', 'w', encoding='utf-8')
allCoursesFacultyFile = open('allCoursesByFaculty.json', 'w', encoding='utf-8')
allCoursesCareerFile = open('allCoursesByCareer.json', 'w', encoding='utf-8')


def sortByCode(data: dict):
    
    myKeys = []
    for x in data:
        myKeys.append(int(x))
    myKeys.sort()
    sorted_dict = {str(i): data[str(i)] for i in myKeys}
    return sorted_dict


# SORT courses by career
data = json.load(byCareer)
data = sortByCode(data)
for faculty in data:
    data[faculty]['careers'] = sortByCode(data[faculty]['careers'])
    for career in data[faculty]['careers']:
        data[faculty]['careers'][career]['courses'] = sortByCode(data[faculty]['careers'][career]['courses']) 

json.dump(data, allCoursesCareerFile, ensure_ascii=False)

# SORT courses by faculty
data = json.load(byFaculty)
data = sortByCode(data)
for faculty in data:
    data[faculty]['courses'] = sortByCode(data[faculty]['courses'])

json.dump(data, allCoursesFacultyFile, ensure_ascii=False)

# SORT courses
data = json.load(byNone)
allCourses = {}
for faculty, facultyData in data.items():
    for course, courseData in facultyData['courses'].items():
        if course not in allCourses:
            allCourses[course] = courseData

data = sortByCode(allCourses)
json.dump(data, allCoursesFile, ensure_ascii=False)









