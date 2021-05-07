import unittest
from apiV2 import *

class Test(unittest.TestCase): 

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def testRoute24hV2(self):
        response = self.app.get('/api/v2/24horas')
        self.assertEqual(response.status_code, 200)

    def testRoute48hV2(self):
        response = self.app.get('/api/v2/48horas')
        self.assertEqual(response.status_code, 200)

    def testRoute72hV2(self):
        response = self.app.get('/api/v2/72horas')
        self.assertEqual(response.status_code, 200)