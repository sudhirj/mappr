from google.appengine.ext import db
from helpers import validators
import logging


"""Database models for the app."""

class Customer(db.Model):
    """Stores info about the client like the ID, and the user object"""
    timestamp = db.DateTimeProperty(auto_now_add = True)
    user = db.UserProperty(required=True)
    url = db.StringProperty(validator=validators.check_url)
    point_count = db.IntegerProperty(default=0)
    
    def __eq__(self, other):
        if isinstance(other,Customer):
            if self.user == other.user and self.url == other.url:
                return True 
        else:
            return False
        return False

class Point(db.Model):
    """Store the map points"""
    lat = db.FloatProperty(required=True,validator=validators.check_point)
    lon = db.FloatProperty(required=True,validator=validators.check_point)
    title = db.StringProperty()
    owner = db.ReferenceProperty(Customer,collection_name='points',required=True)
    


        
        
    def __eq__(self, other):
        if isinstance(other,Point):
            if self.lat == other.lat and self.lon == other.lon and self.owner == other.owner:
                return True
            else:
                return False
            return False
            
    def put(self):
        self.owner.point_count += 1
        self.owner.put()
        return db.Model.put(self)
        
    def delete(self):
        self.owner.point_count -= 1
        self.owner.put()
        return db.Model.delete(self)
        
        
    