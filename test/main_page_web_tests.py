import logging,unittest,main,test.helpers,presenter
from  webtest import TestApp
from google.appengine.ext import webapp



class MainPageTest(test.helpers.WebTestFixture):
    def test_basic_responses(self):
        app = TestApp(self.application)
        self.assertEqual('200 OK', app.get('/').status)
        self.assertEqual('200 OK', app.get('/sudhirurlcheck').status)
        self.assertEqual('200 OK', app.get('/thisoughttoworkforanyurl').status)

        sudhirpage = app.get('/sudhirurl')

     
