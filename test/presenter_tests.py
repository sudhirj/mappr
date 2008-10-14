import unittest, logging, models, test.helpers, presenter
from google.appengine.ext import db
from google.appengine.api import users

class PresenterTests (test.helpers.TestFixture):
    def test_getting_points_for_user(self):
        result = presenter.get_points_for('sudhirurl')
        self.assertEqual(result.__len__(),2)
        result2 = presenter.get_points_for('somerubbish')
        self.assertEqual(result2.__len__(),0)
    
    def test_setting_points_for_user(self):
        mom = models.Customer(user=users.User('mom@gmail.com'),url='momurl')
        mom.put()
        confirmation = presenter.set_point(mom,lat=34.678,lon=-44.3456)
        self.assertEqual(confirmation,'OK')
        
        result = presenter.get_points_for('momurl')
        self.assertEqual(result.__len__(),1)
        self.assertEqual(result.count(dict(lat=34.678,lon=-44.3456,title=None)),1) 

        
