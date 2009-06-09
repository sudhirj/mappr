from google.appengine.api import users
from google.appengine.ext import db
import logging
import models
import test.helpers
import unittest

class ModelQueryTests(test.helpers.TestFixture):
        
    def test_basic_association(self):
        self.assertEqual(self.sudhir.points.count(),2)
        query = models.Point.all()
        query.filter('owner =',self.amrita)
        
        self.assertEqual(query.count(),1)
        self.assertEqual(query[0],self.o2)
        
        
    
    