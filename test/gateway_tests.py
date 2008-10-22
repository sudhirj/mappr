import unittest, logging, models, test.helpers, gateway
from google.appengine.ext import db
from google.appengine.api import users

class GatewayTests (test.helpers.TestFixture):
    def test_getting_points_for_user(self):
        result = gateway.get_points_for('sudhirurl')
        self.assertEqual(len(result),2)
        result2 = gateway.get_points_for('somerubbish')
        self.assertEqual(len(result2),0)
    
    def test_setting_points_for_user(self):
        mom = models.Customer(user=users.User('mom@gmail.com'),url='momurl')
        mom.put()
        confirmation = gateway.set_point(mom,lat=34.678,lon=-44.3456)
        self.assertTrue(confirmation)
        result = gateway.get_points_for('momurl')
        self.assertEqual(len(result),1)
        self.assertEqual(result.count(dict(lat=34.678,lon=-44.3456,title=None)),1) 
    
    def test_user_creation(self):
        new = gateway.create_customer(url = 'test', user=users.User('test@gmail.com'))
        self.assertTrue(new)
        self.assertEqual(gateway.get_points_for('test').__len__(),0)
        self.assertTrue(gateway.set_point(new,lat = 63.345, lon = -4.23))
        self.assertEqual(gateway.get_points_for('test').__len__(),1)
        
        self.assertRaises(Exception,gateway.create_customer,url='test',user=users.User('someone@gmail.com'))
        self.assertRaises(Exception,gateway.create_customer,url='somethingelse',user=users.User('test@gmail.com'))
        self.assertRaises(Exception,gateway.create_customer,url='TeSt',user=users.User('someoneelse@gmail.com'))
    