from google.appengine.api import users
from google.appengine.ext import webapp
from webtest import TestApp
import logging
import main
import settings
import test.helpers
import unittest
import urllib

class JsonTests(test.helpers.WebTestFixture):
    def test_get_points(self):
        app=self.app
        self.logout()
        result = app.get('/_json/points/sudhirurl').json
        self.assertTrue(self.find(result, self.homedict))
        self.assertTrue(self.find(result, self.officedict))
        self.assertEqual(len(result),2)
        
        