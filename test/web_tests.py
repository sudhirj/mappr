import logging, unittest, main, test.helpers, settings, urllib
from BeautifulSoup import BeautifulSoup
from webtest import TestApp
from google.appengine.ext import webapp
from google.appengine.api import users
import BeautifulSoup

class MainPageTest(test.helpers.WebTestFixture):
    def test_basic_responses(self):
        app = self.app
        
        self.assertEqual('200 OK', app.get('/').status)
        self.assertEqual('200 OK', app.get('/sudhirurlcheck').status)
        self.assertEqual('200 OK', app.get('/sudhirurlcheck').status)
        self.assertEqual('200 OK', app.get('/thisoughttoworkforanyurl').status)
        
        
        sudhirpage = app.get('/sudhirurl')
        self.assertEqual('200 OK', sudhirpage.status)
        sudhirpage.mustcontain(self.homedict['title'], self.officedict['title'])
        sudhirpage.mustcontain(self.homedict['lat'], self.homedict['lon'])
        sudhirpage.mustcontain(self.officedict['lat'], self.officedict['lon'])
        
        
    def test_automatic_redirect_when_signed_in(self):
        app = self.app
        self.logout()
        app.get('/', status=200)
        self.login('sudhir.j@gmail.com')
        redirect = app.get('/', status=302)
        self.assertEqual(redirect.location, """http://localhost/sudhirurl""")

class ChecksWebTest(test.helpers.WebTestFixture):
    def test_url_presence_checks(self):
        app = self.app
        resp = app.get('/_check/url/abracadabra')
        resp.mustcontain('Y')
        resp = app.get('/_check/url/sudhirurl')
        resp.mustcontain('N')
        self.login('magician@gmail.com')
        app.post('/', {'url':'abracadabra'})
        resp = app.get('/_check/url/abracadabra')
        resp.mustcontain('N')

class PostMethodsSecurityTest(test.helpers.WebTestFixture):
    def test_security_of_post_handlers(self):
        app = self.app
        self.logout()
        app.post('/', status=403)
        app.post('/_points/', status=403)
        app.delete('/_points/', status=403)

class UserOperationsTest(test.helpers.WebTestFixture):
    def test_user_creation(self):
        app = self.app
        self.logout()
        
        before = app.get('/pagetotest').html
        self.assertTrue(before.find('div', id="create_user"))
        self.assertFalse(before.find('div', id="add_point"))
        
        self.login('testuser@testsite.com')
        
        intermediate = app.get('/pagetotest').html
        self.assertTrue(intermediate.find('div', id="create_user"))
        self.assertFalse(before.find('div', id="add_point"))
        
        app.post('/', {'url':'pagetotest'})
        after = app.get('/pagetotest').html
        self.assertTrue(after.find('div', id="add_point"))
        
        otherpage = app.get('/somebodyelsespage').html
        self.assertFalse(otherpage.find('div', id='add_point'))
        self.assertTrue(before.find('div', id="create_user"))
        
        self.login('guywhowantsform@gmail.com')
        app.post('/', {'url':'form'}, status=403)
    
    def test_homespot_link(self):
        app = self.app
        self.logout()
        soup = app.get('/sudhirurl').html
        self.assertFalse(soup.find('div', id="homespot_link"))
        self.login('sudhir.j@gmail.com')
        soup = app.get('/sudhirurl').html
        self.assertFalse(soup.find('div', id="homespot_link"))
        soup = app.get('/someotherurl').html
        self.assertTrue(soup.find('div', id="homespot_link"))
        
    def test_signin_signout_link(self):
        app = self.app
        self.logout()
        auth_link = app.get('/sudhirurl').html.find('div', id="auth").find('a').contents[0]
        self.assertEqual(auth_link, 'Sign In')
        self.login('sudhir.j@gmail.com')
        auth_link = app.get('/sudhirurl').html.find('div', id="auth").find('a').contents[0]
        self.assertEqual(auth_link, 'Sign Out')        
    
    def test_single_step_signon(self):
        app = self.app
        self.logout()
        resp = app.get('/_create/newurl', status=302)
        self.assertEqual(resp.location, """http://localhost/_ah/login?continue=http%3A//localhost/_create/newurl""")
        app.get('/_check/url/newurl').mustcontain('Y')
        
        self.login('newuser@gmail.com')
        new_spot = app.get('/_create/newurl', status=302).follow().html
        self.assertTrue(new_spot.find('div', id='add_point'))
        self.assertTrue(new_spot.find(text="Getting started."))
        
        self.login('somebodyelse@gmail.com')
        problem = app.get('/_create/newurl', status=302)
        self.assertEqual(problem.location, """http://localhost/""")       
           
class PointOperationsTest(test.helpers.WebTestFixture):    
    def points_in_partial(self, url):
        partial = self.app.get('/%s' % url).html
        return partial.findAll('div', 'point')
            
    def test_point_display(self):
        app = self.app
        self.logout()
        
        mainpage = app.get('/sudhirurl').html
        points = mainpage.findAll('div', "point")
        self.assertEqual(len(points), 2)
        
        self.login('sudhir.j@gmail.com')
        self.assertEqual(len(self.points_in_partial('sudhirurl')), 2)
    
    def test_point_creation(self):
        app = self.app
        self.login('sudhir.j@gmail.com')
        count = len(self.points_in_partial('sudhirurl'))
        app.post('/_points/', {'lat':54, 'lon':35, 'title':'new_point'})
        self.assertEqual(len(self.points_in_partial('sudhirurl')), count + 1)
        
        soup = app.get('/sudhirurl').html
        self.assertTrue(soup.find(text="new_point"))
        self.assertTrue(soup.find(text="54.0"))
        
        amrita_soup = app.get('/amritaurl').html
        self.assertFalse(amrita_soup.find(text='new_point'))
    
    def test_point_editing_and_deleting(self):
        app = self.app
        self.login('sudhir.j@gmail.com')
        response = app.post('/_points/', {'lat':12, 'lon':34, 'title':'point_to_be_changed'})
        returned_key = response.html
        soup = app.get('/sudhirurl').html
        self.assertTrue(soup.find(text="point_to_be_changed"))
        self.assertTrue(soup.find(text="12.0"))
        self.assertTrue(soup.find(text="34.0"))
        
        app.post('/_points/', {'key':returned_key, 'title':'point_that_was_changed', 'lat':21, 'lon':43})
        soup = app.get('/sudhirurl').html
        self.assertTrue(soup.find(text="point_that_was_changed"))
        self.assertTrue(soup.find(text="21.0"))
        self.assertTrue(soup.find(text="43.0"))
        
        app.delete('/_points/' + str(returned_key), {})
        soup = app.get('/sudhirurl').html
        self.assertFalse(soup.find(text="point_that_was_changed"))
        self.assertFalse(soup.find(text="21.0"))
        self.assertFalse(soup.find(text="43.0"))
        
    def test_protection_against_editing_other_peoples_points(self):
        app = self.app
        self.login('sudhir.j@gmail.com')
        sudhir_point_key = app.post('/_points/', {'lat':43, 'lon':23, 'title':'sudhir ka new point'}).html
        self.login('amrita@gmail.com')
        app.post('/_points/', {'key':sudhir_point_key, 'lat':34, 'lon':11, 'title':'hijack this'}, status=403)
    
    def test_protection_against_deleting_other_peoples_points(self):
        app = self.app
        self.login('sudhir.j@gmail.com')
        sudhir_point_key = app.post('/_points/', {'lat':43, 'lon':23, 'title':'sudhir ka new point'}).html
        self.login('amrita@gmail.com')
        app.delete('/_points/' + str(sudhir_point_key), status=403)
            
