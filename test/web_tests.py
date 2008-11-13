import logging,unittest,main,test.helpers,presenter,settings,urllib
from BeautifulSoup import BeautifulSoup
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
        self.logout()
        app.post('/',status=403)
        app.post('/_points/',status=403)
        app.post('/_points/delete',status=403)

class UserOperationsTest(test.helpers.WebTestFixture):
    def test_user_creation(self):
        app = self.app
        self.logout()
        
        before = app.get('/pagetotest').html
        self.assertFalse(before.find('div',id="create-user"))
        self.assertFalse(before.find('div',id="add-point"))
        
        self.login('testuser@testsite.com')
        
        intermediate = app.get('/pagetotest').html
        self.assertTrue(intermediate.find('div',id="create-user"))
        self.assertFalse(before.find('div',id="add-point"))
        
        app.post('/',{'url':'pagetotest'})
        after = app.get('/pagetotest').html
        self.assertTrue(after.find('div',id="add-point"))
        
        otherpage = app.get('/somebodyelsespage').html
        self.assertFalse(otherpage.find('div',id='add-point'))
        self.assertFalse(before.find('div',id="create-user"))

class PointOperationsTest(test.helpers.WebTestFixture):    
    def points_in_partial(self,url):
        partial = self.app.get('/%s' % url).html
        return partial.findAll('div','point')
            
    def test_point_display(self):
        app = self.app
        self.logout()
        
        mainpage = app.get('/sudhirurl').html
        points = mainpage.findAll('div', "point")
        logging.info(len(points))
        self.assertEqual(len(points),2)
        
        self.login('sudhir.j@gmail.com')
        self.assertEqual(len(self.points_in_partial('sudhirurl')),2)
    
    def test_point_creation(self):
        app = self.app
        self.login('sudhir.j@gmail.com')
        count = len(self.points_in_partial('sudhirurl'))
        app.post('/_points/',{'lat':54,'lon':35,'title':'new_point'})
        self.assertEqual(len(self.points_in_partial('sudhirurl')),count+1)
        
        soup = app.get('/sudhirurl').html
        self.assertTrue(soup.find(text="new_point"))
        self.assertTrue(soup.find(text="54.0"))
        
        amrita_soup = app.get('/amritaurl').html
        self.assertFalse(amrita_soup.find(text='new_point'))
    
    def test_point_editing_and_deleting(self):
        app = self.app
        self.login('sudhir.j@gmail.com')
        response = app.post('/_points/',{'lat':12,'lon':34,'title':'point_to_be_changed'})
        returned_key = response.html
        soup = app.get('/sudhirurl').html
        self.assertTrue(soup.find(text="point_to_be_changed"))
        self.assertTrue(soup.find(text="12.0"))
        self.assertTrue(soup.find(text="34.0"))
        
        app.post('/_points/',{'key':returned_key, 'title':'point_that_was_changed', 'lat':21, 'lon':43})
        soup = app.get('/sudhirurl').html
        self.assertTrue(soup.find(text="point_that_was_changed"))
        self.assertTrue(soup.find(text="21.0"))
        self.assertTrue(soup.find(text="43.0"))
        
        app.post('/_points/delete',{'key':returned_key})
        soup = app.get('/sudhirurl').html
        self.assertFalse(soup.find(text="point_that_was_changed"))
        self.assertFalse(soup.find(text="21.0"))
        self.assertFalse(soup.find(text="43.0"))

            
        
        
        
        
        