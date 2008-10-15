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
        
        self.homedict = dict(lat = 34.6467, lon = 46.36, owner = self.sudhir)
        self.home = models.Point(point = db.GeoPt(34.6467, 46.36),owner=self.sudhir)
        self.home.put()
       
        self.office = models.Point(point = db.GeoPt(23.46,4.7),owner=self.sudhir)
        self.office.put()
        self.o2 = models.Point(point = db.GeoPt(24.234456,-85.34556),owner = self.amrita,parent = self.sudhir)
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
    