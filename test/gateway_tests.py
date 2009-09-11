from google.appengine.api import users
from google.appengine.ext import db
import gateway
import logging
import models
import simplejson as json
import test.helpers
import unittest

class GatewayTests (test.helpers.TestFixture):
    
     
    def test_user_creation_and_editing(self):
        test_user = users.User('test@gmail.com')
        new = gateway.create_customer(url='test', user=test_user)
        self.assertTrue(new)
        self.assertEqual(gateway.get_points_for('test').__len__(), 0)
        self.assertTrue(gateway.set_point(new, dict(lat=63.345, lon= -4.23)))
        self.assertEqual(gateway.get_points_for('test').__len__(), 1)
        
        self.assertRaises(Exception, gateway.create_customer, url='test', user=users.User('someone@gmail.com'))
        self.assertRaises(Exception, gateway.create_customer, url='TeSt', user=users.User('someoneelse@gmail.com'))
        self.assertRaises(Exception, gateway.create_customer, url='new_test', user=test_user)
        
        renew = gateway.create_customer(url='newtest', user=test_user)
        self.assertTrue(renew)
        self.assertEqual(gateway.get_points_for('newtest').__len__(), 1)
        self.assertTrue(gateway.set_point(renew, dict(lat=43.345, lon= -3.23)))
        self.assertEqual(gateway.get_points_for('newtest').__len__(), 2)
            
    def test_user_existence_check(self):
        self.assertFalse(gateway.check_if_user_exists(users.User('nonexistentemail@gmail.com')))
        self.assertTrue(gateway.check_if_user_exists(users.User('sudhir.j@gmail.com')))
    
    def test_url_existence_check(self):
        self.assertFalse(gateway.check_if_url_exists('nonexistenturl')[0])
        self.assertTrue(gateway.check_if_url_exists('sudhirurl')[0])
        self.assertTrue(gateway.check_if_url_exists('SuDhirurl')[0])
        self.assertTrue(gateway.check_if_url_exists('SuDhirUrl')[0])
        
    def test_point_editing(self):
        result = gateway.get_points_for('sudhirurl')
        start_count = len(result)
        new_point_dict = dict(lat=7.0, lon=7.0, title="seven")
        new_point_key = gateway.set_point(self.sudhir, new_point_dict).key().__str__()
        result = gateway.get_points_for('sudhirurl')
        
        self.assertEqual(len(result), start_count + 1)
        self.assertTrue(self.find(result, new_point_dict))
        
        new_point_dict = dict(lon=7.0, lat=8.0, title='seveneight')
        gateway.edit_point(new_point_key, new_point_dict, self.sudhir_gmail)
        new_results = gateway.get_points_for('sudhirurl')
        
        self.assertEqual(len(new_results), start_count + 1)
        self.assertTrue(self.find(new_results, new_point_dict))
        self.assertRaises(db.BadValueError, gateway.edit_point, new_point_key, dict(lon=2345, lat=3, title='invalid values'), self.sudhir_gmail)
  
    def test_point_deletion(self):
        result = gateway.get_points_for('sudhirurl')
        start_count = len(result)
        first_point = result[0]
        gateway.delete_point(first_point['key'], self.sudhir_gmail)
        new_result = gateway.get_points_for('sudhirurl')
        self.assertEqual(len(new_result), start_count - 1)
        self.assertFalse(self.find(new_result, first_point))
        
    def test_get_current_user_url(self):
        url = gateway.get_current_user_url(self.sudhir_gmail)
        self.assertEqual(url, 'sudhirurl')

        url = gateway.get_current_user_url(users.User('lskj@lsdfj.com'))
        self.assertFalse(url)
        
        url = gateway.get_current_user_url(None)
        self.assertFalse(url)
  
    def test_get_current_user_nickname(self):
        self.assertEqual(gateway.get_current_user_nick('nosuchurl'), None)
        self.assertEqual(gateway.get_current_user_nick('sudhirurl'), 'sudhir.j')
