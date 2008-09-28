from google.appengine.ext import db


"""Database models for the app."""

class Client(db.Model):
    """Stores info about the client like the ID, and the user object"""
    timestamp = db.DateTimeProperty(auto_now_add = True)
    user = db.UserProperty()
    tiny = db.StringProperty()

class Point(db.Model):
    """Store the map points"""
    lat = db.FloatProperty()
    lon = db.FloatProperty()
    title = db.StringProperty()
    text = db.TextProperty()
    