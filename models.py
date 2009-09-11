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
        if not self.equality_attributes or not len(self.equality_attributes): 
            return super(Base, self).__eq__(other)
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
        if self.point_count > settings.hard_point_count_ceiling: 
            raise Exception, "Hard ceiling reached."
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
    
    @classmethod
    def get_points_for(cls, url):
        customer = cls.get_by_url(url)
        if not customer: return None
        return [dict(lat=point.point.lat,
                    lon=point.point.lon,
                    title=point.title,
                    key=str(point.key())) for point in customer.points]
    
    @classmethod
    def create(cls, url, user):
        if cls.get_by_url(url):
            raise Exception, "URL already exists"
        customer = cls.get_by_user(user) or Customer(url=url, user=user)
        customer.url = url
        customer.put()
        return customer

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
    
    @classmethod
    def create_point(cls, customer, new_point):
        point = dict(title="Untitled", lat=0, lon=0)
        point.update(new_point)
        created_point = cls(point=db.GeoPt(point['lat'], point['lon']),
                            title=point['title'], 
                            owner=customer, 
                            parent=customer)
        created_point.put()
        return created_point
        
    @classmethod
    def edit(cls, key, new_point, user):
        customer = Customer.get_by_user(user)
        if not customer: raise Exception, "Customer does not exist."
        point = customer.get_point_by_key(key)
        if not point: raise Exception, "Point does not exist."
        point.title = new_point['title']
        point.point = db.GeoPt(new_point['lat'], new_point['lon'])
        point.put()
    
    @classmethod
    def delete_point(cls, key, user):
        customer = Customer.get_by_user(user)
        if not customer: raise Exception, "No spot for this user."
        point = customer.get_point_by_key(key)
        if not point: raise Exception, "That isn't your pin."
        point.delete()
            
        

