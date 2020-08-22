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
    def test_RUN(self):
        def start_and_init_server(app):
            app.run(threaded=True)

        server_process = Process(target=start_and_init_server, args=(app, ))
        server_process.start()
        noOfNewUsers = 10
        request_threads = []
        responseCode = 0
        try:
            def post_data():
                usr = "tempUser"+str(uuid.uuid4())
                response = app.test_client().post('/addUser', data=json.dumps(dict(
                username = usr,
                password = 'password'
                )), content_type='application/json')
                if response.status_code != 200:
                    responseCode = 1

            for i in range(noOfNewUsers):
                t = threading.Thread(target=post_data)
                request_threads.append(t)
                t.start()

            all_done = False
            while not all_done:
                all_done = True
                for t in request_threads:
                    if t.is_alive():
                        all_done = False
                        time.sleep(1)

            assert responseCode == 0
        except Exception as ex:
            print('Something went wrong!', ex.message)
        finally:
            server_process.terminate()
            server_process.join()

if __name__ == '__main__':
    unittest.main()