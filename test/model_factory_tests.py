from google.appengine.api import users
from google.appengine.ext import db
import factory
import gateway
import logging
import simplejson as json
import test.helpers
import unittest

class FactoryTests (test.helpers.TestFixture):
    def test_point_factory(self):
        self.assertEqual(factory.make_geo_point(3.0,5.6),db.GeoPt(3.0,5.6))
    