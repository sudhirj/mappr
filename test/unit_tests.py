import unittest
import logging
import models
from google.appengine.ext import db
from google.appengine.api import users


class BasicModelTests(unittest.TestCase):
    def setUp(self):
        self.sudhir = users.User('sudhir.j@gmail.com')
        self.amrita = users.User('amrita@gmail.com')
        
            
    def test_point_creation(self):
        cl = memcache.Client()
        

# import model
# 
# class SuccessFailError(unittest.TestCase):
# 
#     def setUp(self):
#         logging.info('In setUp()')
#         
#     def tearDown(self):
#         logging.info('In tearDown()')
# 
#     def test_success(self):
#         logging.info('Running test_success()')
#         self.assertTrue(True)
# 
#     def test_failure(self):
#         logging.info('Running test_failure()')
#         self.assertTrue(True)
#         
#     def test_error(self):
#         logging.info('Running test_error()')
#         raise Exception('expected exception')


# class ModelTest(unittest.TestCase):
# 
#   def setUp(self):
#     # Populate test entities.
#     entity = model.MyEntity(name='Bar')
#     self.setup_key = entity.put()
# 
#   def tearDown(self):
#     # There is no need to delete test entities.
#     pass
# 
#   def test_new_entity(self):
#     entity = model.MyEntity(name='Foo')
#     self.assertEqual('Foo', entity.name)
# 
#   def test_saved_enitity(self):
#     entity = model.MyEntity(name='Foo')
#     key = entity.put()
#     self.assertEqual('Foo', db.get(key).name)
# 
#   def test_setup_entity(self):
#     entity = db.get(self.setup_key)
#     self.assertEqual('Bar', entity.name)
# 
# 
