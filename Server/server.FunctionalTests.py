import unittest
from backend import app
import json
import threading
import requests
import time
from backend.services.services import *
from backend.routing.routes import *
import sys
from multiprocessing import Process

SERVER_URL = "http://127.0.0.1:5000"

class TestCases(unittest.TestCase):
    def test_AddUser(self):
        tester = app.test_client(self)
        usr = "tempUser"+str(uuid.uuid4())
        response = tester.post('/addUser', data=json.dumps(dict(
        username = usr,
        password = 'password'
        )), content_type='application/json')
        assert response.status_code == 200

    def test_signInFalse(self):
        tester = app.test_client(self)
        usr = "tempUser"+str(uuid.uuid4())
        response = tester.post('/signin', data=json.dumps(dict(
        username = usr,
        password = 'password'
        )), content_type='application/json')
        assert response.status_code == 400

    def test_signInTrue(self):
        tester = app.test_client(self)
        response = tester.post('/signin', data=json.dumps(dict(
        username = 'devesh',
        password = 'password123'
        )), content_type='application/json')
        assert response.status_code == 200
    
    def test_getUserMetricsFalse(self):
        tester = app.test_client(self)
        usr = "tempUser"+str(uuid.uuid4())
        response = tester.post('/getUserMetrics', data=json.dumps(dict(
        userid = usr,
        )), content_type='application/json')  
        assert response.status_code == 400
    
    def test_getUserMetricsTrue(self):
        tester = app.test_client(self)
        response = tester.post('/getUserMetrics', data=json.dumps(dict(
        userid = "devesh",
        )), content_type='application/json')  
        assert response.status_code == 200

    def test_getDatasets(self):
        tester = app.test_client(self)
        response = tester.get('/getDatasets', content_type='html/text')
        assert response.status_code == 200

    def test_newRequestFalse(self):
        tester = app.test_client(self)
        response = tester.post('/signin', data=json.dumps(dict(
        )), content_type='application/json')
        assert response.status_code == 400

    def test_AddUserMetricCreation(self):
        tester = app.test_client(self)
        usr = "tempUser"+str(uuid.uuid4())
        response = tester.post('/addUser', data=json.dumps(dict(
        username = usr,
        password = 'password'
        )), content_type='application/json')
        assert checkUserExistsInUserMetrics(container_userMetrics, response.json.get('userid')) == True

if __name__ == '__main__':
    unittest.main()