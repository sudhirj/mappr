import logging,unittest,main,test.helpers,presenter,settings,urllib
from  webtest import TestApp
from google.appengine.ext import webapp
from google.appengine.api import users

class MainPageTest(test.helpers.WebTestFixture):
    def test_basic_responses(self):
        app = self.app
        
        self.assertEqual('200 OK', app.get('/').status)
        self.assertEqual('200 OK', app.get('/sudhirurlcheck').status)
        self.assertEqual('200 OK', app.get('/sudhirurlcheck').status)
        self.assertEqual('200 OK', app.get('/thisoughttoworkforanyurl').status)
        
        
        sudhirpage = app.get('/sudhirurl')
        self.assertEqual('200 OK',sudhirpage.status)
        sudhirpage.mustcontain(self.homedict['title'],self.officedict['title'])
        sudhirpage.mustcontain(self.homedict['lat'],self.homedict['lon'])
        sudhirpage.mustcontain(self.officedict['lat'],self.officedict['lon'])

class ChecksWebTest(test.helpers.WebTestFixture):
    def test_url_presence_checks(self):
        app = self.app
        
        resp_good_choice = app.get('/_check/url/abracadabra')
        resp_good_choice.mustcontain('N')
        self.assertEqual('200 OK',resp_good_choice.status)
        
        resp_url_already_present = app.get('/_check/url/sudhirurl')
        resp_url_already_present.mustcontain('Y')
        self.assertEqual('200 OK',resp_url_already_present.status)

class PostMethodsSecurityTest(test.helpers.WebTestFixture):
    def test_security_of_post_handlers(self):
        app = self.app
        
        # Testing main user creation 
        app.post('/',status=403)
        
        # Testing point creation
        app.post('/_points/',status=403)
