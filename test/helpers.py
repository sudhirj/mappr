import models
from google.appengine.ext import db
def clearDatastore():
    for point in models.Point.all():
        db.delete(point)
    for customer in models.Customer.all():
        db.delete(customer)