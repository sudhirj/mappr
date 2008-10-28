from google.appengine.ext import db
from helpers import validators
import logging, settings


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
    point = db.GeoPtProperty(required = True)
    title = db.StringProperty(required = False)
    owner = db.ReferenceProperty(Customer,collection_name='points',required=True)
    
    def __eq__(self, other):
        if isinstance(other,Point):
            if self.point == other.point and self.owner == other.owner and self.title == other.title:
                return True
            else:
                return False
            return False
    
    def delete(self):
        self.owner.point_count -=1
        self.owner.put()
        return db.Model.delete(self)
    
    def put(self):
        if self.is_saved():
            return db.Model.put(self)
        else:
            self.parent = self.owner
            self.owner.point_count +=1
            if self.owner.point_count > settings.hard_point_count_ceiling:
                raise Exception, "Maximum possible number of points reached."
            self.owner.put()
            return db.Model.put(self)

