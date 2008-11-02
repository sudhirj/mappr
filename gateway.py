import models,logging
from google.appengine.api import users
from google.appengine.ext import db

def get_points_for(url):
    customer = get_customer_by_url(url)
    pointset = []
    if not customer:
        return []
    for point in customer.points:
        pointset.append(dict(lat = point.point.lat,lon = point.point.lon,title = point.title,key=point.key()))
    return pointset

def set_point(customer, point_info):
    defaults = dict(title="Untitled",lat=0,lon=0)
    defaults.update(point_info)
    newpoint = models.Point(point = db.GeoPt(defaults['lat'],defaults['lon']),title=defaults['title'], owner = customer, parent = customer)
    newpoint.put()
    return newpoint

def create_customer(url, user):
    if get_customer_by_url(url):
        raise Exception, "This PinnSpot URL already exists."
    if get_customer(user):
        raise Exception, "You already have a PinnSpot URL."
    new_customer = models.Customer(url = url, user = user)
    new_customer.put()
    return new_customer

def check_if_user_exists(user):
    return True if get_customer(user) else False

def check_if_url_exists(url):
    customer = get_customer_by_url(url)
    return (True,customer.url) if customer else (False,None)

def get_customer(user):
     customer = models.Customer.all().filter('user =',user).fetch(1)
     return customer[0] if len(customer) else None 
     
def get_customer_by_url(url):
     customer = models.Customer.all().filter('url =',url.lower()).fetch(1)
     return customer[0] if len(customer) else None 
    
    