import unittest
import logging
import models
from google.appengine.ext import db
from google.appengine.api import users
import test.helpers


class BasicModelTests(test.helpers.TestFixture):
        
    def test_customer_validations(self):
        self.assertRaises(ValueError,models.Customer,None)
        self.assertRaises(ValueError,models.Customer,user = self.sudhir_gmail)
        self.assertRaises(db.BadValueError,models.Customer,url='check')
        new_customer = models.Customer(url='check',user = self.sudhir_gmail)
        self.assertTrue(new_customer)
        self.assertTrue(new_customer.put())
        
        try:
            new_customer.url = None
        except ValueError,e:
            pass
        else:
            self.fail('Was supposed to stop the url being set to None')
        
        customer2 = models.Customer(user = self.sudhir_gmail,url='coffee')
        
        try:
            customer2.url=''
        except ValueError:
            pass
        else:
            self.fail('Was supposed to stop the url being set to blank')
        
        try:
            customer2.url='%^'
        except ValueError:
            pass
        else:
            self.fail('Was supposed to stop the url being not alphanumeric')
        
        customer2.url = 'the354'
        self.assertTrue(customer2.put())
    
    def test_point_validations(self):
        sudhir = models.Customer(user=self.sudhir_gmail,url='df').put()
        self.assertRaises(db.BadValueError,models.Point,None)
        self.assertRaises(db.BadValueError,models.Point,lat=34.445)
        self.assertRaises(db.BadValueError,models.Point,lon=36.345)
        self.assertRaises(db.BadValueError,models.Point,lat=34.45,lon=32.466)
        self.assertRaises(db.BadValueError,models.Point,lat=-34.45,lon=32.466)
        self.assertRaises(ValueError,models.Point,lat=float(3462.344),lon=float(45.67),owner=sudhir)
        self.assertRaises(ValueError,models.Point,lat=float(34.344),lon=float(-2345.67),owner=sudhir)
        
        point = models.Point(lat=34.5,lon=36.23,owner=sudhir)
        try:
            point.lat = 45666.456
        except ValueError:
            pass
        else:
            self.fail('Was supposed to prevent setting lat to invalid value')
        
        try:
            point.lon = -34667.34
        except ValueError:
            pass    
        else:
            self.fail('was supposed to prevent lon being set to an invalid value')
        
        try:
            point.owner = None
        except db.BadValueError:
            pass
        else:
            self.fail('was supposed to prevent owner being set to none')
        
