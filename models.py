from google.appengine.ext import db
from helpers import validators


"""Database models for the app."""

class Customer(db.Model):
    """Stores info about the client like the ID, and the user object"""
    timestamp = db.DateTimeProperty(auto_now_add = True)
    user = db.UserProperty(required=True)
    url = db.StringProperty(validator=validators.check_url)

class Point(db.Model):
    """Store the map points"""
    lat = db.FloatProperty(required=True)
    lon = db.FloatProperty(required=True)
    title = db.StringProperty()
    text = db.TextProperty()
    