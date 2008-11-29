import unittest, logging, test.helpers, gateway, factory
from google.appengine.ext import db
from google.appengine.api import users
import simplejson as json

class FactoryTests (test.helpers.TestFixture):
    def test_point_factory(self):
        self.assertEqual(factory.make_geo_point(3.0,5.6),db.GeoPt(3.0,5.6))
    