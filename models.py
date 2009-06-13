from google.appengine.ext import db
from helpers import validators
import logging
import settings

"""Database models for the app."""

class Base(db.Model):
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    
    def __eq__(self, other, attributes=[]):
        if not isinstance(other, self.__class__): return False
        if not len(attributes): return super(Base, self).__eq__(other)
        for attr in attributes:
            if getattr(self, attr) != getattr(other, attr): return False
        return True 
    
    def __ne__(self, other):
        return not self == other

class Customer(Base):
    """Stores info about the client like the ID, and the user object"""
    user = db.UserProperty(required=True)
    url = db.StringProperty(validator=validators.check_url)
    point_count = db.IntegerProperty(default=0)
    
    def __eq__(self, other):
        return super(Customer, self).__eq__(other, attributes=['user', 'url'])
        
    def get_point_by_key(self, key):
        return self.points.filter("__key__ =", db.Key(key)).fetch(1)[0]
    

class Point(Base):
    """Store the map points"""
    point = db.GeoPtProperty(required=True)
    title = db.StringProperty(required=True)
    owner = db.ReferenceProperty(Customer, collection_name='points', required=True)
    
    def __eq__(self, other):
        if not isinstance(other, Point): return False
        for attr in ['point', 'owner', 'title']:
            if getattr(self, attr) != getattr(other, attr): return False
        return True
    
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

        

