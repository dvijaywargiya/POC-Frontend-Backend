import json

f = open('datasets.json')

data = json.load(f)
temp = []
num = 1
for ele in data:
    t = dict()
    t['id'] = num
    num += 1
    t['entityName'] = ele['entityName']
    t['datasetName'] = ele['datasetName']
    t['datasetUserScope'] = {}
    avl = 0
    for p in ele['availableScopes']:
        t['datasetUserScope'][p['datasetUserScope']] = 1
        avl = p['datasetAvailability']
    val = avl.split('.')
    val = int(val[0])
    t['datasetAvailability'] = val
    t['datasetSize'] = val*100
    t['numberOfRequests'] = 0
    t['numberOfSuccessfulExtractions'] = 0
    t['userCompleteness'] = 0
    temp.append(t)

tt = json.dumps(temp)
with open("toBeUploaded.json", "w") as outfile: 
    outfile.write(tt) 