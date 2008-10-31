import wsgiref.handlers,logging, gateway, os, cgi, settings
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from helpers import utils
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

class MainHandler(webapp.RequestHandler):
    def get(self,url=None):
        pointset = gateway.get_points_for(url)
        template_values = {'points':pointset,'auth':utils.authdetails()}
        self.response.out.write(template.render(utils.path('templates/index.html'),template_values))
    
    @utils.authorize('user')
    def post(self,url=None):
        user = users.get_current_user()
        url = cgi.escape(self.request.get('url'))
        try:
            new_customer = gateway.create_customer(url,user)
            self.response.out.write(new_customer.url) 
        except Exception, e:
            self.response.out.write(e)
            self.response.set_status(403)
            

class UrlCheckHandler(webapp.RequestHandler):
    def get(self,url=None):
        self.response.out.write('Y' if gateway.check_if_url_exists(url) else 'N')


class PointHandler(webapp.RequestHandler):
    @utils.authorize('user')
    def post(self):
        user = users.get_current_user()
        lat = cgi.escape(self.request.get('lat'))
        lon = cgi.escape(self.request.get('lon'))
        try:
            new_point = gateway.set_point(customer = gateway.get_customer(user) , lat = lat, lon = lon)
            new_point.title = cgi.escape(self.request.get('title'))
            
            self.response.out.write('OK_%s',new_point.key())
        except Exception, e:
            self.response.out.write('ERROR_%s',e)
            self.response.set_status(403)    
    
ROUTES =[
            (r'/_points/', PointHandler),
            (r'/_check/url/(.*)', UrlCheckHandler),
            (r'/(.*)', MainHandler)
        ]

def createMainApplication():
    return webapp.WSGIApplication(ROUTES,debug=settings.debug)
                                        
def main():
    wsgiref.handlers.CGIHandler().run(createMainApplication())

if __name__ == '__main__':
    main()