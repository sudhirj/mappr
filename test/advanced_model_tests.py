from google.appengine.ext import db
import unittest
import logging
import models
from google.appengine.api import users
import test.helpers


class AdvancedModelTests(unittest.TestCase):
    def setUp(self):
        self.sudhir_gmail = users.User('sudhir.j@gmail.com')
        self.sudhir = models.Customer(user=self.sudhir_gmail,url='someshit')
        self.sudhir.put()
        self.home = models.Point(lat = 34.6467,lon = 46.36,owner=self.sudhir,parent=self.sudhir)
        self.home.put()
        self.office = models.Point(lat = 23.46,lon = 4.7,owner=self.sudhir)
        self.office.put()
    
    def tearDown(self):
        test.helpers.clearDatastore()
    
    def test_parentage(self):
        self.assertEqual(self.sudhir.key(),self.office.parent_key())
    
    def test_equality_overrides(self):
        sudhir2 = models.Customer(user=self.sudhir_gmail, url='someshit')
        self.assertEqual(self.sudhir,sudhir2)
        self.assertFalse(sudhir2==self.home)
        self.assertFalse(self.sudhir == models.Customer(user=self.sudhir_gmail, url='bedf'))
        
        home2 = models.Point(lat = 34.6467, lon = 46.36, owner=self.sudhir)
        self.assertEqual(self.home,home2)
        self.assertFalse(home2 == self.office)

    def test_point_owner_counter(self):
        self.assertTrue(self.sudhir.points[0]==self.home)    
        self.assertEqual(self.sudhir.points[1],self.office)
        self.assertEqual(self.sudhir.point_count,2)
        
        self.office.delete()
        
        self.assertEqual(self.sudhir.point_count,1)
    
    def test_delete_override(self):        
        self.assertEqual(models.Point.all().count(),2)
        query  = models.Point.all().filter('lat =',23.46)
        self.assertEqual(query.count(),1)
        self.office.delete()
        self.assertEqual(models.Point.all().count(),1)
        query  = models.Point.all().filter('lat =',23.46)
        self.assertEqual(query.count(),0)
     
    def test_delete_override_on_db_class(self):
        self.assertEqual(models.Point.all().count(),2)
        query  = models.Point.all().filter('lat =',23.46)
        self.assertEqual(query.count(),1)
        db.delete(self.office)
        self.assertEqual(models.Point.all().count(),1)
        query  = models.Point.all().filter('lat =',23.46)
        self.assertEqual(query.count(),0)

