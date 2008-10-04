import models
from google.appengine.ext import db
from google.appengine.api import users
import unittest
from  webtest import TestApp
from google.appengine.ext import webapp
import main

class TestFixture (unittest.TestCase):
    def setUp(self):
        self.sudhir_gmail = users.User('sudhir.j@gmail.com')
        self.amrita_gmail = users.User('amrita@gmail.com')
        
        self.sudhir = models.Customer(user=self.sudhir_gmail,url='sudhirurl')
        self.sudhir.put()
        self.amrita = models.Customer(user=self.amrita_gmail, url='amritaurl')
        self.amrita.put()
        
        self.homedict = dict(lat = 34.6467,lon = 46.36,title=None)
        self.home = models.Point(lat = 34.6467,lon = 46.36,owner=self.sudhir)
        self.home.put()
       
        self.office = models.Point(lat = 23.46,lon = 4.7,owner=self.sudhir)
        self.office.put()
        self.officedict = dict(lat = 34.6467,lon = 46.36,title=None)
        self.o2 = models.Point(lat=24.234456,lon=-85.34556,owner = self.amrita,parent = self.sudhir)
        self.o2.put()
            
    def tearDown(self):
        for point in models.Point.all():
            db.delete(point)
        for customer in models.Customer.all():
            db.delete(customer)
    
class WebTestFixture(TestFixture):
    def setUp(self):
        TestFixture.setUp(self)
        self.application = main.createMainApplication()
    