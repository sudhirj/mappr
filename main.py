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
        except Exception, e:
            self.response.out.write(e)
            self.response.set_status(403)
        else:
            self.response.out.write(new_customer.url) 

class UrlCheckHandler(webapp.RequestHandler):
    def get(self,url=None):
        if gateway.check_if_url_exists(url):
            self.response.out.write('Y')
        else:
            self.response.out.write('N')


class PointHandler(webapp.RequestHandler):
    @utils.authorize('user')
    def post(self):
        pass    
    
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