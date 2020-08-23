from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from backend.services.services import *
import uuid
import datetime
import json
import random
import csv
from datetime import date, datetime
import calendar
from backend.ADL.model import categoryMap, datasetMap

def addNewUser(request, container_users, container_userMetrics):
    username = request.json.get('username')
    password = generate_password_hash(request.json.get('password'))
    if username is None or password is None:
        abort(400)
    addNewFileInUserMetrics(container_userMetrics, username)
    toBeAdded = {
        'id': username,
        'password': password
    }
    return toBeAdded

def createNewRequest(request):
    requestName = request.json.get('requestName')
    userId = request.json.get('userId')
    requestIdTobeAdded = userId + str(uuid.uuid4())
    datasetName = request.json.get('datasetName')
    datasetId = request.json.get('datasetId')
    datasetScope = request.json.get('datasetScope')
    numberOfDays =  request.json.get('daysSelected')
    isSuccessful = False
    if requestName is None \
        or userId is None \
        or datasetName is None \
        or datasetScope is None:
        abort(400)
    toBeAdded = {
        'id': requestIdTobeAdded,
        'requestName': requestName,
        'userId': userId,
        'datasetId': datasetId,
        'datasetName': datasetName,
        'datasetScope': datasetScope,
        'numberOfDays': numberOfDays,
        'successful': isSuccessful,
    }
    return toBeAdded

def returnDatasets():
    f = open('/home/devesh/Devesh/MSFT/flaskCosmosAzure/server/backend/ADL/datasets.json')
    data = json.load(f)
    temp = []
    for ele in data:
        avl = 0
        per = 0
        pub = 0
        for p in ele['availableScopes']:
            if p['datasetUserScope'] == "personal":
                per = 1
            if p['datasetUserScope'] == "publicGroup":
                pub = 1
            avl = p['datasetAvailability']
        val = avl.split('.')
        val = int(val[0])
        toBeAdded = {
            'id' : str(uuid.uuid4()),
            'description': ele['description'],
            'entityName' : ele['entityName'],
            'datasetName' : ele['datasetName'],
            'datasetUserScope' : {
                'personal': str(per),
                'publicGroup': str(pub)
            },
            'datasetAvailability' : str(val),
            'datasetSize' : str(val*100),
            'numberOfRequests' : 0,
            'successfulExtractions' : 0,
            'userCompleteness' : random.randint(91, 100)
        }
        temp.append(toBeAdded)
    return temp

def returnJobs():
    temp = []
    ct = 1
    with open('/home/devesh/Devesh/MSFT/flaskCosmosAzure/server/backend/static/dataset.csv', 'r') as fl:
        reader = csv.reader(fl)
        for line in reader:
            arr = line
            toBeAdded = {
                'id' : str(ct),
                'category': str(arr[0]),
                'entityName': str(arr[1]),
                'day': float(arr[3]),
                'time': float(arr[4]),
                'days': float(arr[5]),
                'timeTaken': float(arr[6])
            }
            ct = ct + 1
            temp.append(toBeAdded)
    return temp

def predictParameteres(request):
    # print(request.json)
    UserScope = request.json.get('userscope')
    EntityName = request.json.get('entityName')
    Days = request.json.get('daysSelected')
    if UserScope is None\
        or EntityName is None\
        or Days is None:
        abort(400)
    Days = int(Days)
    today = date.today()
    dt = today.strftime("%d/%m/%Y")
    dt = dt.split('/')
    day = calendar.weekday(int(dt[2]), int(dt[1]), int(dt[0]))
    now = datetime.now()
    tm = now.strftime("%H:%M")
    tm = tm.split(':')
    tm = int(tm[0]+tm[1])
    Lt =  [[UserScope, EntityName, day, tm, Days]]
    Lt[0][0] = categoryMap[Lt[0][0]]
    try:
        Lt[0][1] = datasetMap[Lt[0][1]]
    except:
        Lt[0][1] = 27
    # print(Lt)
    return Lt