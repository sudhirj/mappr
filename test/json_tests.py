import logging,unittest,main,test.helpers,presenter,settings,urllib
from webtest import TestApp
from google.appengine.ext import webapp
from google.appengine.api import users
import simplejson as json

class JsonTests(test.helpers.WebTestFixture):
    def test_get_points(self):
        app=self.app
        self.logout()
        result = app.get('/_json/points/sudhirurl').body
        result = json.loads(result)
        self.assertTrue(self.find(result, self.homedict))
        self.assertTrue(self.find(result, self.officedict))
        self.assertEqual(len(result),2)
        
        