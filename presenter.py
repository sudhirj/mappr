import models,logging
from google.appengine.api import users

def get_points_for(url):
    query = models.Customer.all().filter('url =',url)
    if query.count() == 0:
        return None
    else:       
        pointset = []
      
        for point in query[0].points:
            sanitizedpoint = {}
            sanitizedpoint = dict(lat=point.lat,lon = point.lon,title = point.title)
            pointset.append(sanitizedpoint)
        
        return pointset

def set_point(customer, lat, lon):
    newpoint = models.Point(lat = lat, lon = lon, owner = customer, parent = customer)
    newpoint.put()
    return 'OK'


    
    