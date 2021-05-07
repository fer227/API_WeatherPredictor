import unittest
from apiV1 import *

class Test(unittest.TestCase): 

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def testRoute24hV1(self):
        response = self.app.get('/api/v1/24horas')
        self.assertEqual(response.status_code, 200)

    def testRoute48hV1(self):
        response = self.app.get('/api/v1/48horas')
        self.assertEqual(response.status_code, 200)

    def testRoute72hV1(self):
        response = self.app.get('/api/v1/72horas')
        self.assertEqual(response.status_code, 200)