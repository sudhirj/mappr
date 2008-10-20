import logging,unittest,main,test.helpers,presenter
from  webtest import TestApp
from google.appengine.ext import webapp
from google.appengine.api import users

class MainPageTest(test.helpers.WebTestFixture):
    def test_basic_responses(self):
        app = self.app
        
        self.assertEqual('200 OK', app.get('/').status)
        self.assertEqual('200 OK', app.get('/sudhirurlcheck').status)
        self.assertEqual('200 OK', app.get('/thisoughttoworkforanyurl').status)
        
        sudhirpage = app.get('/sudhirurl')
        self.assertEqual('200 OK',sudhirpage.status)
        sudhirpage.mustcontain(self.homedict['title'],self.officedict['title'])
        sudhirpage.mustcontain(self.homedict['lat'],self.homedict['lon'])
        sudhirpage.mustcontain(self.officedict['lat'],self.officedict['lon'])
        
    def test_setting_points(self):
        pass
        

     
