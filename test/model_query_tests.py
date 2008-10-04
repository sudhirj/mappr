from google.appengine.ext import db
import unittest
import logging
import models
from google.appengine.api import users
import test.helpers

class ModelQueryTests(test.helpers.TestFixture):
        
    def test_basic_association(self):
        self.assertEqual(self.sudhir.points.count(),2)
        query = models.Point.all()
        query.filter('owner =',self.amrita)
        
        self.assertEqual(query.count(),1)
        self.assertEqual(query[0],self.o2)
        
        
    
    