import wsgiref.handlers,logging, gateway, os, settings, cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from helpers import utils
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

class CustomHandler(webapp.RequestHandler):
    def handle_exception(self,exception, debug_mode):
        self.response.out.write(exception)
        self.response.set_status(403)
    def respond(self,resp):
        self.response.out.write(resp)
    def respond_json(self, resp):
        import simplejson
        self.response.headers["Content-Type"] = "application/json"
        self.response.out.write(simplejson.dumps(resp))
    def render(self, template_path, data):
        self.respond(template.render(utils.path(template_path),data))
        

class MainHandler(CustomHandler):
    def get(self,url=None):
        user = users.get_current_user()
        if not url:
            logged_in_user_url = gateway.get_current_user_url(user)
            if logged_in_user_url: self.redirect('/'+logged_in_user_url)
        
        pointset = gateway.get_points_for(url)
        info = dict(current_url = url, 
                    user_url = gateway.get_current_user_url(user), 
                    user_nick = gateway.get_current_user_nick(url),
                    point_ceiling = settings.hard_point_count_ceiling,
                    empty_spot = True if pointset == None else False)
        template_values = { 'points':pointset if not pointset==None else [],
                            'auth':utils.authdetails('/'+url), 
                            'info':info}
                            
        self.respond(template.render(utils.path('templates/index.html'),template_values))
    
    @utils.authorize('user')
    def post(self,url=None):
        user = users.get_current_user()
        url = cgi.escape(self.request.get('url')).lower()

        if url == 'form': raise Exception, "You cannot use 'form'."
        new_customer = gateway.create_customer(url,user)
        self.respond(new_customer.url) 

        
class UrlCheckHandler(CustomHandler):
    def get(self,url=None):
        self.respond('N' if gateway.check_if_url_exists(url)[0] else 'Y')

class UrlCreateHandler(CustomHandler):
    @utils.authorize('user')
    def get(self,url=None):
        user = users.get_current_user()
        url = url.lower()
        try:
            if url == 'form': raise Exception, "You cannot use 'form'."
            new_customer = gateway.create_customer(url,user)
            self.redirect("/"+new_customer.url)            
        except Exception, e:
            self.redirect('/')
        
        
class PointHandler(CustomHandler):
    @utils.authorize('user')
    def post(self,url=None):
        user = users.get_current_user()
        lat = float(self.request.get('lat'))
        lon = float(self.request.get('lon'))
        title = str(cgi.escape(self.request.get('title')))
        key = self.request.get('key')
        
        point = dict(title=title, lat = lat, lon = lon)
        if not key:
            if title == '' or title==None: raise Exception, "You need to provide a title."
            new_point = gateway.set_point(gateway.get_customer(user), point)
            self.respond(new_point.key())
        else:
            gateway.edit_point(key, point, user)
            self.respond('OK')
    
    @utils.authorize('user')
    def get(self,url=None):
        pointset = gateway.get_points_for(url)
        self.render('templates/pointlist.html',{'points':pointset})
    
    @utils.authorize('user')
    def delete(self, key=None):
        gateway.delete_point(key,users.get_current_user())

class PointJsonHandler(CustomHandler):
    def get(self,url):
        pointset = gateway.get_points_for(url)
        self.respond_json(pointset)
        
        
ROUTES =[
            (r'/_json/points/(.*)', PointJsonHandler),
            (r'/_points/(.*)', PointHandler),
            (r'/_create/(.*)', UrlCreateHandler),
            (r'/_check/url/(.*)', UrlCheckHandler),
            (r'/(.*)', MainHandler)
        ]

def createMainApplication():
    return webapp.WSGIApplication(ROUTES,debug=settings.debug)
                                        
def main():
    wsgiref.handlers.CGIHandler().run(createMainApplication())

if __name__ == '__main__':
    main()