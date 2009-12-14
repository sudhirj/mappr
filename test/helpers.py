from google.appengine.api import users
from google.appengine.ext import db, webapp
from webtest import TestApp

import logging
import main
import models
import settings
import unittest, os

class TestFixture (unittest.TestCase):
    def setUp(self):
        os.environ['SERVER_NAME'] = 'test'
        os.environ['SERVER_PORT'] = '9001'
        self.sudhir_gmail = users.User('sudhir.j@gmail.com')
        self.amrita_gmail = users.User('amrita@gmail.com')
        
        self.sudhir = models.Customer(user=self.sudhir_gmail, url='sudhirurl')
        self.sudhir.put()
        self.amrita = models.Customer(user=self.amrita_gmail, url='amritaurl')
        self.amrita.put()
        
        self.homedict = dict(lat=34.6467, lon=46.36, owner=self.sudhir, title="sudhir_home")
        self.home = models.Point(point=db.GeoPt(34.6467, 46.36), owner=self.sudhir, title="sudhir_home")
        self.home.put()
       
        self.officedict = dict(lat=23.46, lon=4.7, owner=self.sudhir, title="sudhir_office")
        self.office = models.Point(point=db.GeoPt(23.46, 4.7), owner=self.sudhir, title="sudhir_office")
        self.office.put()
        
        self.o2dict = dict(title='O2', lat=24.234456, lon= -85.34556)
        self.o2 = models.Point(title="O2", point=db.GeoPt(24.234456, -85.34556), owner=self.amrita, parent=self.amrita)
        self.o2.put()
        
        self.temp_gcu = users.get_current_user
        
        
            
    def tearDown(self):
        for point in models.Point.all():
            point.delete() 
        for customer in models.Customer.all():
            customer.delete()
        users.get_current_user = self.temp_gcu
            
    
    def login(self, user="sudhir.j@gmail.com"):
        users.get_current_user = lambda user = user : users.User(user) if user else None
    def logout(self):
        self.login(None)
    
    def find(self, search_in, search_for, equalizers=['title', 'lat', 'lon']):
        for item in search_in:
            found = True
            for key in equalizers:
                if not item.has_key(key) or not item[key] == search_for[key]: found = False
            if found: return True
        return False
            
                
class WebTestFixture(TestFixture):
    def setUp(self):
        TestFixture.setUp(self)
        self.app = TestApp(main.createMainApplication())
        self.logout()

        
        
    
