from google.appengine.api import users
from google.appengine.ext import db
import logging
import models
import settings
import test.helpers
import unittest
from models import Point, Customer


class PointModelTests(test.helpers.TestFixture):
    
    def test_parentage(self):
        point = models.Point(title="parentage_test_point", point=db.GeoPt(34.66467, 46.366), owner=self.sudhir, parent=self.sudhir)
        self.assertEqual(self.sudhir.key(), point.parent_key())
    
    def test_equality_overrides(self):
        home2 = models.Point(point=db.GeoPt(34.6467, 46.36), owner=self.sudhir, title="sudhir_home")
        self.assertEqual(self.home, home2)
        self.assertFalse(home2 == self.office)

    def test_delete_override(self):
        startcount = models.Point.all().count()
        query = models.Point.all().filter('point =', db.GeoPt(23.46, 4.7))
        self.assertEqual(query.count(), 1)
        self.office.delete()
        self.assertEqual(models.Point.all().count(), startcount - 1)
        query = models.Point.all().filter('lat =', 23.46)
        self.assertEqual(query.count(), 0)
     
    def test_delete_override_on_db_class(self):
        startcount = models.Point.all().count()
        query = models.Point.all().filter('point =', db.GeoPt(23.46, 4.7))
        self.assertEqual(query.count(), 1)
        db.delete(self.office)
        self.assertEqual(models.Point.all().count(), startcount - 1)
        query = models.Point.all().filter('lat =', 23.46)
        self.assertEqual(query.count(), 0)

    def test_setting_points_for_user(self):
        mom = models.Customer(user=users.User('mom@gmail.com'), url='momurl')
        mom.put()
        confirmation = Point.create_point(mom, dict(lat=34.678, lon= -44.3456))
        self.assertTrue(confirmation)
        result = Customer.get_points_for('momurl')
        self.assertEqual(len(result), 1)
        self.assertEqual(result.count(dict(lat=34.678, lon= -44.3456, title='Untitled', key=str(confirmation.key()))), 1) 
