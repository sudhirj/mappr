import models,logging
from google.appengine.api import users
from google.appengine.ext import db

def get_points_for(url):
    customer = get_customer_by_url(url)
    if not customer: return []
    return [dict(lat = point.point.lat,
                lon = point.point.lon,
                title = point.title,
                key=point.key()) for point in customer.points]

def set_point(customer, new_point):
    point = dict(title="Untitled",lat=0,lon=0)
    point.update(new_point)
    created_point = models.Point(point = db.GeoPt(point['lat'],point['lon']),
                                title=point['title'], 
                                owner = customer, 
                                parent = customer)
    created_point.put()
    return created_point

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

def edit_point(key, new_point):
    point = db.get(key)
    point.title = new_point['title']
    point.point = db.GeoPt(new_point['lat'],new_point['lon'])
    point.put()
    
def delete_point(key):
    point = db.get(key)
    logging.info(point)
    point.delete()

def get_current_user_url():
    user = users.get_current_user()
    if not user: return None
    customer = get_customer(user) if user else None
    if not customer: return None
    return customer.url
    
    
    