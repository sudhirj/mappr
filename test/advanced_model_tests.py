from google.appengine.ext import db
import unittest, logging, models, test.helpers, settings
from google.appengine.api import users


class AdvancedModelTests(test.helpers.TestFixture):
    
    def test_parentage(self):
        point = models.Point(point = db.GeoPt(34.66467,46.366), owner=self.sudhir,parent=self.sudhir)
        self.assertEqual(self.sudhir.key(),point.parent_key())
    
    def test_equality_overrides(self):
        sudhir2 = models.Customer(user=self.sudhir_gmail, url='sudhirurl')
        self.assertEqual(self.sudhir,sudhir2)
        self.assertFalse(sudhir2==self.home)
        self.assertFalse(self.sudhir == models.Customer(user=self.sudhir_gmail, url='url2'))
        
        home2 = models.Point(point = db.GeoPt(34.6467,46.36), owner=self.sudhir, title="sudhir_home")
        self.assertEqual(self.home,home2)
        self.assertFalse(home2 == self.office)

    def test_point_owner_counter(self):
        self.assertTrue(self.sudhir.points[0]==self.home)    
        self.assertEqual(self.sudhir.points[1],self.office)
        self.assertEqual(self.sudhir.point_count,2)
        self.office.delete()
        self.assertEqual(self.sudhir.point_count,1)
    
    def test_point_owner_counter_does_not_exceed_hard_ceiling(self):
        number_of_points_to_reach_ceiling = settings.hard_point_count_ceiling - self.sudhir.point_count - 1
        
        for i in xrange(number_of_points_to_reach_ceiling):
            models.Point(point = db.GeoPt(i,i),owner=self.sudhir).put()
        
        last_straw = models.Point(point = db.GeoPt(89,89),owner=self.sudhir)
        self.assertRaises(Exception,last_straw.put,None)
        
    
    def test_delete_override(self):
        startcount = models.Point.all().count()
        query  = models.Point.all().filter('point =',db.GeoPt(23.46,4.7))
        self.assertEqual(query.count(),1)
        self.office.delete()
        self.assertEqual(models.Point.all().count(),startcount-1)
        query  = models.Point.all().filter('lat =',23.46)
        self.assertEqual(query.count(),0)
     
    def test_delete_override_on_db_class(self):
        startcount = models.Point.all().count()
        query  = models.Point.all().filter('point =',db.GeoPt(23.46,4.7))
        self.assertEqual(query.count(),1)
        db.delete(self.office)
        self.assertEqual(models.Point.all().count(),startcount - 1)
        query  = models.Point.all().filter('lat =',23.46)
        self.assertEqual(query.count(),0)

