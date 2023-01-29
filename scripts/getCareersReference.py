import json

def sortByCode(data: dict):
    
    myKeys = []
    for x in data:
        myKeys.append(int(x))
    myKeys.sort()
    sorted_dict = {str(i): data[str(i)] for i in myKeys}
    return sorted_dict

allCareers = open('ramosCarrera.json', 'r', encoding='utf-8')
allCareersFile = open('allCoursesCareer.txt', 'w', encoding='utf-8')

allDict = {}
data = json.load(allCareers)

for faculty in data:
    for career in data[faculty]['careers']:
        if career not in allDict:
            allDict[career] = {'careerName' :data[faculty]['careers'][career]['name'],
                               'facultyName': data[faculty]['name'],
                               'facultyId': faculty,
                            }

allDict = sortByCode(allDict)
allCareersFile.write(str(allDict))
