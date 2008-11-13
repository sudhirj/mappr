import models, unittest, main, logging, settings
from google.appengine.ext import db
from google.appengine.api import users
from webtest import TestApp
from google.appengine.ext import webapp

class TestFixture (unittest.TestCase):
    def setUp(self):
        
        self.sudhir_gmail = users.User('sudhir.j@gmail.com')
        self.amrita_gmail = users.User('amrita@gmail.com')
        
        self.sudhir = models.Customer(user=self.sudhir_gmail,url='sudhirurl')
        self.sudhir.put()
        self.amrita = models.Customer(user=self.amrita_gmail, url='amritaurl')
        self.amrita.put()
        
        self.homedict = dict(lat = 34.6467, lon = 46.36, owner = self.sudhir, title="sudhir_home")
        self.home = models.Point(point = db.GeoPt(34.6467, 46.36),owner=self.sudhir, title="sudhir_home")
        self.home.put()
       
        self.officedict = dict(lat=23.46,lon=4.7,owner=self.sudhir, title = "sudhir_office")
        self.office = models.Point(point = db.GeoPt(23.46,4.7),owner=self.sudhir, title = "sudhir_office")
        self.office.put()
        
        self.o2 = models.Point(title="O2",point = db.GeoPt(24.234456,-85.34556),owner = self.amrita,parent = self.amrita)
        self.o2.put()
        
            
    def tearDown(self):
        for point in models.Point.all():
            db.delete(point)
        for customer in models.Customer.all():
            db.delete(customer)
                    
                
class WebTestFixture(TestFixture):
    def setUp(self):
        TestFixture.setUp(self)
        self.app = TestApp(main.createMainApplication())
        self.logout()

    def login(self, user = "sudhir.j@gmail.com"):
        users.get_current_user = lambda user=user : users.User(user) if user else None
    def logout(self):
        self.login(None)
        
        
    