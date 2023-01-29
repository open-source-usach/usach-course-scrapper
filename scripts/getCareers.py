import json

def sortByCode(data: dict):
    
    myKeys = []
    for x in data:
        myKeys.append(int(x))
    myKeys.sort()
    sorted_dict = {str(i): data[str(i)] for i in myKeys}
    return sorted_dict


allCareers = open('ramosCarrera.json', 'r', encoding='utf-8')


allCareersFile = open('allCareers.json', 'w', encoding='utf-8')
allCareersFacultyFile = open('allCareersFaculty.json', 'w', encoding='utf-8')

data = json.load(allCareers)
# Get all careers faculty-independent
allDict = {}


for faculty in data:
    for career in data[faculty]['careers']:
        allDict[career] = data[faculty]['careers'][career]['name']

allDict = sortByCode(allDict)
json.dump(allDict, allCareersFile, ensure_ascii=False)

# Get all careers faculty-dependent

allDict = {}

for faculty in data:
    allDict[faculty] = {'name': data[faculty]['name'], 'careers': {}}
    for career in data[faculty]['careers']:
        allDict[faculty]['careers'][career] = data[faculty]['careers'][career]['name']

allDict = sortByCode(allDict)
for faculty in allDict:
    data[faculty]['careers'] = sortByCode(data[faculty]['careers'])
json.dump(allDict, allCareersFacultyFile, ensure_ascii=False)
#allCareersFacultyFile.write(str(allDict))


