import logging,unittest,main,test.helpers,settings,urllib
from webtest import TestApp
from google.appengine.ext import webapp
from google.appengine.api import users

class JsonTests(test.helpers.WebTestFixture):
    def test_get_points(self):
        app=self.app
        self.logout()
        result = app.get('/_json/points/sudhirurl').json
        self.assertTrue(self.find(result, self.homedict))
        self.assertTrue(self.find(result, self.officedict))
        self.assertEqual(len(result),2)
        
        