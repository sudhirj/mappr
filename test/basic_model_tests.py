from google.appengine.api import users
from google.appengine.ext import db
import logging
import models
import test.helpers
import unittest

class BasicModelTests(test.helpers.TestFixture):
        
    def test_customer_validations(self):
        self.assertRaises(ValueError, models.Customer, None)
        self.assertRaises(ValueError, models.Customer, user=self.sudhir_gmail)
        self.assertRaises(db.BadValueError, models.Customer, url='check')
        new_customer = models.Customer(url='check', user=self.sudhir_gmail)
        self.assertTrue(new_customer)
        self.assertTrue(new_customer.put())
        
        self.assertRaises(ValueError, setattr, new_customer, 'url', None)
        
        customer2 = models.Customer(user=self.sudhir_gmail, url='coffee')
        
        self.assertRaises(ValueError, setattr, customer2, 'url', '')
        self.assertRaises(ValueError, setattr, customer2, 'url', '%$')
        
        customer2.url = 'the354'
        self.assertTrue(customer2.put())
    
    def test_point_validations(self):
        sudhir = models.Customer(user=self.sudhir_gmail, url='df').put()
        self.assertRaises(db.BadValueError, models.Point, None)
        
        point = models.Point(point=db.GeoPt(34.5, 36.23), owner=sudhir, title="testpoint")
        self.assertRaises(db.BadValueError, setattr, point, 'owner', None)

