from google.appengine.ext import db
import unittest
import logging
import models
from google.appengine.api import users
import test.helpers

class ModelQueryTests(unittest.TestCase):
    def setUp(self):
        self.sudhir_gmail = users.User('sudhir.j@gmail.com')
        self.amrita_gmail = users.User('amrita@gmail.com')
        self.sudhir = models.Customer(user=self.sudhir_gmail,url='someshit')
        self.sudhir.put()
        self.amrita = models.Customer(user=self.amrita_gmail, url='iloveo2')
        self.amrita.put()
        self.home = models.Point(lat = 34.6467,lon = 46.36,owner=self.sudhir)
        self.home.put()
        self.office = models.Point(lat = 23.46,lon = 4.7,owner=self.sudhir)
        self.office.put()
        self.o2 = models.Point(lat=24.234456,lon=-85.34556,owner = self.amrita)
    
    def tearDown(self):
        test.helpers.clearDatastore()