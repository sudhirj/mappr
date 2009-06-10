from google.appengine.ext import db
from helpers import validators
import logging
import settings

"""Database models for the app."""

class Customer(db.Model):
    """Stores info about the client like the ID, and the user object"""
    timestamp = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty(required=True)
    url = db.StringProperty(validator=validators.check_url)
    point_count = db.IntegerProperty(default=0)
    
    def __eq__(self, other):
        if not isinstance(other,Customer): return False
        for attr in ['user','url']:
            if getattr(self, attr) != getattr(other,attr): return False
        return True
    def __ne__(self,other):
        return not self == other
    
    def get_point_by_key(self, key):
        return self.points.filter("__key__ =", db.Key(key)).fetch(1)[0]
    

class Point(db.Model):
    """Store the map points"""
    point = db.GeoPtProperty(required=True)
    title = db.StringProperty(required=True)
    owner = db.ReferenceProperty(Customer, collection_name='points', required=True)
    
    def __eq__(self, other):
        if not isinstance(other,Point): return False
        for attr in ['point','owner', 'title']:
            if getattr(self, attr) != getattr(other,attr): return False
        return True
    def __ne__(self, other):
        return not self == other
    
    def delete(self):
        self.owner.point_count -= 1
        self.owner.put()
        return super(Point, self).delete()
    
    def put(self):
        if self.is_saved(): return db.Model.put(self)
        self.parent = self.owner
        self.owner.point_count += 1
        if self.owner.point_count > settings.hard_point_count_ceiling: raise Exception, "Hard ceiling reached."
        self.owner.put()
        return super(Point, self).put()

        

