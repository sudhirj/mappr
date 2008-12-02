def make_geo_point(lat, lon):
    from google.appengine.ext import db
    return db.GeoPt(lat,lon)
    