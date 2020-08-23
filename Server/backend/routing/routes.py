from backend import app
from backend.db.connection import *
from flask import Flask, redirect, abort, request, jsonify, url_for
import json, random
from backend.routing.supportFunctions import *
from werkzeug.security import generate_password_hash, check_password_hash
from backend.ADL.model import Regressor
from sklearn.preprocessing import MinMaxScaler
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

def retrain():
    Regressor.reTrain()
    return json.dumps("Success")

sched = BackgroundScheduler(daemon=True)
sched.add_job(retrain, 'interval', minutes=24*60)
sched.start()

@app.route('/', methods = ['GET'])
def get():
    return redirect('/swagger')

@app.route('/predictCost', methods = ['POST'])
def predictCost():
    Lt = predictParameteres(request)
    val = Regressor.predict(Lt)
    return json.dumps(val)

@app.route('/addUser', methods=['POST'])
def newUser():
    toBeAdded = addNewUser(request, container_users, container_userMetrics)
    container_users.create_item(body=toBeAdded)
    return jsonify(dict({'userid':toBeAdded['id']}))

@app.route('/signin', methods=['POST'])
def signIn():
    username = request.json.get('username')
    password = request.json.get('password')
    try:
        item_response = container_users.read_item(item=username, partition_key=username)
        if check_password_hash(item_response['password'], password):
            return jsonify({'userid':item_response['id']})
        else: abort(400)      
    except:
        abort(400)        
  
@app.route('/getUserMetrics', methods=['POST'])
def getUserMetrics():
    try:
        userid = request.json.get('userid')
        item_response = container_userMetrics.read_item(item=userid, partition_key=userid)
        return json.dumps(item_response)
    except:
        abort(400)

@app.route('/addJobs', methods=['POST'])
def addJobs():
    body = returnJobs()
    for ele in body:    
        container_jobs.create_item(body=ele)
    return jsonify(dict({'cr':body[0]['id']}))


@app.route('/addDatasets', methods=['POST'])
def addDatasets():
    body = returnDatasets()
    for ele in body:    
        container_datasets.create_item(body=ele)
    return jsonify(dict({'cr':body[0]['id']}))

@app.route('/getDatasets', methods=['GET'])
def getDatasets():
    item_list = list(container_datasets.read_all_items())
    return json.dumps(item_list)

@app.route('/newRequest', methods=['POST'])
def newRequest():
    toBeAdded = createNewRequest(request)
    container_requests.create_item(body=toBeAdded)
    updateUserMetricsTE(container_userMetrics, toBeAdded['userId'], toBeAdded['datasetName'])
    updateDatasetExtractionCount(container_datasets, toBeAdded['datasetId'])
    val = bool(random.getrandbits(1))
    updateOnExtractionUserMetrics(container_userMetrics, toBeAdded['userId'], val)
    updateOnExtractionDatasetMetrics(container_datasets, toBeAdded['datasetId'], val)
    updateOnExtractionRequestStatus(container_requests, toBeAdded['id'], val)
    return jsonify(dict({'requestid':toBeAdded['id']}))

if __name__ == '__main__':
    app.run(debug=True)