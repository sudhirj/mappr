import logging
import models
from models import Customer, Point

def get_points_for(url):
    return Customer.get_points_for(url)

def set_point(customer, new_point):
    return Point.create_point(customer, new_point)
   
def create_customer(url, user):
    return Customer.create(url, user)

def check_if_user_exists(user):
    return not not get_customer(user) 

def check_if_url_exists(url):
    customer = get_customer_by_url(url)
    return (True, customer.url) if customer else (False, None)

def get_customer(user):
    return Customer.get_by_user(user)
     
def get_customer_by_url(url):
    return Customer.get_by_url(url)

def edit_point(key, new_point, user):
    return Point.edit(key, new_point, user)
    
def delete_point(key, user):
    return Point.delete_point(key, user)

def get_current_user_url(user):
    return Customer.get_url_by_user(user)

def get_current_user_nick(url):
    return Customer.get_nick_by_url(url)
    
    
