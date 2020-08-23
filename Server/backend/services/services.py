import json

def addNewFileInUserMetrics(container, userId):
    tempDict = dict()
    toBeAdded = {
        'id': userId,
        'totalExtractions': 0,
        'datasetExtracted': json.dumps(tempDict),
        'successfulExtractions': 0
    }
    container.create_item(body=toBeAdded)

def checkUserExistsInUsers(container, userId, userName):
    item_response = container.read_item(item=userId, partition_key=userName)
    print(item_response)     

def checkUserExistsInUserMetrics(container, userId):
    item_response = container.read_item(item=userId, partition_key=userId)
    if item_response: return True
    else: return False     

def updateOnExtractionRequestStatus(container, id, val):
    if val == False: return 
    item_response = container.read_item(item=id, partition_key=id)
    item_response['successful'] = True
    response = container.upsert_item(body=item_response)    

def updateUserMetricsTE(container, userId, datasetName):
    item_response = container.read_item(item=userId, partition_key=userId)
    item_response['totalExtractions'] += 1
    tempDict = json.loads(item_response['datasetExtracted'])
    try:
        tempDict[datasetName] += 1
    except: 
        tempDict[datasetName] = 1
    item_response['datasetExtracted'] = json.dumps(tempDict)
    response = container.upsert_item(body=item_response)

def updateDatasetExtractionCount(container, datasetId):
    item_response = container.read_item(item=datasetId, partition_key=datasetId)
    item_response['numberOfRequests'] = item_response['numberOfRequests'] + 1
    response = container.upsert_item(body=item_response)

def updateOnExtractionUserMetrics(container, id, wasSuccessful):
    if wasSuccessful == False: return
    item_response = container.read_item(item=id, partition_key=id)    
    item_response['successfulExtractions'] += 1
    response = container.upsert_item(body=item_response) 

def updateOnExtractionDatasetMetrics(container, id, wasSuccessful):
    item_response = container.read_item(item=id, partition_key=id)    
    if wasSuccessful == True:
        item_response['successfulExtractions'] += 1
    item_response['userCompleteness'] = (item_response['successfulExtractions']/item_response['numberOfRequests']) * 100    
    response = container.upsert_item(body=item_response) 