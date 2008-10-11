import models,logging
from google.appengine.api import users
from google.appengine.ext import db

def get_points_for(url):
    customer = models.Customer.all().filter('url =',url).get()
    pointset = []
    if customer == None:
        return pointset
        
    for point in customer.points:
        stripped_point = {}
        stripped_point = dict(lat = point.point.lat,lon = point.point.lon,title = point.title)
        pointset.append(stripped_point)
        
    return pointset

def set_point(customer, lat, lon):
    newpoint = models.Point(point = db.GeoPt(lat,lon), owner = customer, parent = customer)
    newpoint.put()
    return 'OK'


    
    