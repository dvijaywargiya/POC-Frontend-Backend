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
from backend.db.connection import database

SERVER_URL = "http://127.0.0.1:5000"

class TestCases(unittest.TestCase):
    def test_UsersPresent(self):
        try:
            container = database.get_container_client("Users")
            return True
        except:
            return False

    def test_UserMetricsPresent(self):
        try:
            container = database.get_container_client("UserMetrics")
            return True
        except:
            return False
    
    def test_RequestsPresent(self):
        try:
            container = database.get_container_client("Requests")
            return True
        except:
            return False
    def test_DatasetsPresent(self):
        try:
            container = database.get_container_client("Datasets")
            return True
        except:
            return False

if __name__ == '__main__':
    unittest.main()