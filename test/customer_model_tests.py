from google.appengine.api import users
from google.appengine.ext import db
import logging
import models, settings
import test.helpers
import unittest
from models import Customer

class CustomerModelTests(test.helpers.TestFixture):
        
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

    def test_equality_overrides(self):
        sudhir2 = models.Customer(user=self.sudhir_gmail, url='sudhirurl')
        self.assertEqual(self.sudhir, sudhir2)
        self.assertFalse(sudhir2 == self.home)
        self.assertFalse(self.sudhir == models.Customer(user=self.sudhir_gmail, url='url2'))
        
    def test_point_owner_counter(self):
        self.assertEqual(self.sudhir.points[0], self.home)  
        self.assertEqual(self.sudhir.points[1], self.office)
        self.assertEqual(self.sudhir.point_count, 2)
        self.office.delete()
        self.assertEqual(self.sudhir.point_count, 1)

    def test_point_owner_counter_does_not_exceed_hard_ceiling(self):
        number_of_points_to_reach_ceiling = settings.hard_point_count_ceiling - self.sudhir.point_count - 1

        for i in xrange(number_of_points_to_reach_ceiling):
            models.Point(title="point" + str(i), point=db.GeoPt(i, i), owner=self.sudhir).put()

        last_straw = models.Point(title="last_straw", point=db.GeoPt(89, 89), owner=self.sudhir)
        self.assertRaises(Exception, last_straw.put, None)

    def test_getting_points_for_user(self):
          valid_result = Customer.get_points_for('sudhirurl')
          self.assertEqual(len(valid_result), 2)

          valid_result = Customer.get_points_for('suDhirurl')
          self.assertEqual(len(valid_result), 2)

          valid_result = Customer.get_points_for('sudhirURl')
          self.assertEqual(len(valid_result), 2)

          non_existent_url = Customer.get_points_for('somerubbish')
          self.assertEqual(non_existent_url, None)

          new_guy = models.Customer(user=users.User('someguy@gmail.com'), url='someguyurl')
          new_guy.put()
          empty_result = Customer.get_points_for('someguyurl')
          self.assertEqual(empty_result, [])
          empty_result = Customer.get_points_for('SomEguyurl')
          self.assertEqual(empty_result, [])
