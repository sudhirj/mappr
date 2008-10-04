import logging,unittest,main,test.helpers,presenter
from  webtest import TestApp
from google.appengine.ext import webapp


class IndexTest(test.helpers.WebTestFixture):

  def test_basic_responses(self):
      app = TestApp(self.application)
      self.assertEqual('200 OK', app.get('/').status)
      self.assertEqual('200 OK', app.get('/sudhirurl').status)
      self.assertEqual('200 OK', app.get('/thisoughttoworkforanyurl').status)
      self.assertTrue('Hello' in app.get('/something'))
