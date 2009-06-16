import factory
import logging
import models
from models import Customer

def get_points_for(url):
    customer = get_customer_by_url(url)
    if not customer: return None
    return [dict(lat=point.point.lat,
                lon=point.point.lon,
                title=point.title,
                key=str(point.key())) for point in customer.points]

def set_point(customer, new_point):
    point = dict(title="Untitled", lat=0, lon=0)
    point.update(new_point)
    created_point = models.Point(point=factory.make_geo_point(point['lat'], point['lon']),
                                    title=point['title'],
                                    owner=customer,
                                    parent=customer)
    created_point.put()
    return created_point

def create_customer(url, user):
    if get_customer_by_url(url):
        raise Exception, "This PinnSpot URL already exists."
    existing_customer = get_customer(user)
    if existing_customer:
        existing_customer.url = url
        existing_customer.put()
        return existing_customer
    else:
        new_customer = models.Customer(url=url, user=user)
        new_customer.put()
        return new_customer

def check_if_user_exists(user):
    return True if get_customer(user) else False

def check_if_url_exists(url):
    customer = get_customer_by_url(url)
    return (True, customer.url) if customer else (False, None)

def get_customer(user):
    return Customer.get_by_user(user)
     
def get_customer_by_url(url):
    return Customer.get_by_url(url)

def edit_point(key, new_point, user):
    customer = get_customer(user)
    if not customer: raise Exception, "Customer does not exist."
    point = customer.get_point_by_key(key)
    if not point: raise Exception, "Point does not exist."
    point.title = new_point['title']
    point.point = factory.make_geo_point(new_point['lat'], new_point['lon'])
    point.put()
    
def delete_point(key, user):
    customer = get_customer(user)
    if not customer: raise Exception, "No spot for this user."
    point = customer.get_point_by_key(key)
    if not point: raise Exception, "That isn't your pin."
    point.delete()

def get_current_user_url(user):
    if not user: return None
    customer = get_customer(user) if user else None
    return None if not customer else customer.url

def get_current_user_nick(url):
    customer = get_customer_by_url(url)
    return None if not customer else customer.user.nickname()
    
    
