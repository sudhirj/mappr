from google.appengine.ext import db
from helpers import validators
import logging
import settings

"""Database models for the app."""

class Base(db.Model):
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__): return False
        if not self.equality_attributes or not len(self.equality_attributes): return super(Base, self).__eq__(other)
        for attr in self.equality_attributes:
            if getattr(self, attr) != getattr(other, attr): return False
        return True 
    
    def __ne__(self, other):
        return not self == other

class Customer(Base):
    """Stores info about the client like the ID, and the user object"""
    user = db.UserProperty(required=True)
    url = db.StringProperty(validator=validators.check_url)
    point_count = db.IntegerProperty(default=0)
    
    equality_attributes = ['user', 'url']
        
    def get_point_by_key(self, key):
        return self.points.filter("__key__ =", db.Key(key)).fetch(1)[0]
    
    def inc_point_count(self):
        self.point_count += 1
        if self.point_count > settings.hard_point_count_ceiling: raise Exception, "Hard ceiling reached."
        self.put()
    
    def dec_point_count(self):
        self.point_count -= 1
        self.put()

    @classmethod
    def get_by_url(cls, url):
        matches = cls.all().filter('url =', url.lower()).fetch(1)
        return matches[0] if len(matches) else None
    
    @classmethod
    def get_by_user(cls, user):
        matches = cls.all().filter('user =', user).fetch(1)
        return matches[0] if len(matches) else None 

class Point(Base):
    """Store the map points"""
    point = db.GeoPtProperty(required=True)
    title = db.StringProperty(required=True)
    owner = db.ReferenceProperty(Customer, collection_name='points', required=True)
    
    equality_attributes = ['point','owner','title']
    
    def delete(self):
        self.owner.dec_point_count()
        return super(Point, self).delete()
    
    def put(self):
        if self.is_saved(): return db.Model.put(self)
        self.parent = self.owner
        self.owner.inc_point_count()
        return super(Point, self).put()

        

