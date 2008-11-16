import wsgiref.handlers,logging, gateway, os, settings, cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from helpers import utils
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

class MainHandler(webapp.RequestHandler):
    def get(self,url=None):
        pointset = gateway.get_points_for(url)
        info = dict(current_url = url, user_url = gateway.get_current_user_url())
        template_values = { 'points':pointset,
                            'auth':utils.authdetails('/'+url), 
                            'info':info}
                            
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
        self.response.out.write('Y' if gateway.check_if_url_exists(url)[0] else 'N')


class PointHandler(webapp.RequestHandler):
    @utils.authorize('user')
    def post(self,url=None):
        user = users.get_current_user()
        lat = float(self.request.get('lat'))
        lon = float(self.request.get('lon'))
        title = str(cgi.escape(self.request.get('title')))
        key = self.request.get('key')
        
        point = dict(title=title, lat = lat, lon = lon)
        if not key:
            try:
                new_point = gateway.set_point(gateway.get_customer(user), point)
                self.response.out.write(new_point.key())
            except Exception, e:
                self.response.out.write(e)
                self.response.set_status(403)    
        else:
            try:
                gateway.edit_point(key, point)
                self.response.out.write('OK')
            except Exception, e:
                self.response.out.write(e)
                self.response.set_status(403)
    
    @utils.authorize('user')
    def get(self,url=None):
        pointset = gateway.get_points_for(url)
        self.response.out.write(template.render(utils.path('templates/pointlist.html'),{'points':pointset}))

class PointDeleteHandler(webapp.RequestHandler): 
    @utils.authorize('user')
    def post(self):
        key = self.request.get_all('key')
        try:
            gateway.delete_point(key)
        except Exception, e:
            self.response.out.write(e)
            self.response.out.write(403)    
    
ROUTES =[
            (r'/_points/delete.*', PointDeleteHandler),
            (r'/_points/(.*)', PointHandler),
            (r'/_check/url/(.*)', UrlCheckHandler),
            (r'/(.*)', MainHandler)
        ]

def createMainApplication():
    return webapp.WSGIApplication(ROUTES,debug=settings.debug)
                                        
def main():
    wsgiref.handlers.CGIHandler().run(createMainApplication())

if __name__ == '__main__':
    main()