from google.appengine.ext import db
"""Database models for the app.

Client: stores extra information about the client, including their key, billing details, etc. 
Points: stores map locations.

"""
class Client(db.Model):
    timestamp = db.DateTimeProperty(auto_now_add = True)
    user = db.UserProperty()
    name = db.StringProperty()

class Point(db.Model):
    lat = db.FloatProperty()
    lon = db.FloatProperty()
    