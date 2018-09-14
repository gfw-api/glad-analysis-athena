import unittest
import json
# from gladAnalysis import app
import requests
from httmock import all_requests, response, HTTMock


@all_requests
def response_content(url, request):
    headers = {'content-type': 'application/json'}
    content = {'data': 'any value'}
    return response(200, content, headers, None, 5, request)

class BasicTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def deserialize(self, response):
        return json.loads(response.data).get('data', None)
