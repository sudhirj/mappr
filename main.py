import wsgiref.handlers,logging, gateway, os
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
    
    def post(self,url=None):
        user = users.get_current_user()
        if user == None:
            self.response.set_status(403)
            return
        else:
            url = self.request.get('url')
            try:
                new_customer = gateway.create_customer(url,user)
            except Exception, e:
                self.response.out.write(e)
                self.response.set_status(403)
            else:
                self.response.out.write(new_customer.url) 
                   
    
ROUTES =[
            (r'/(.*)', MainHandler)
        ]

def createMainApplication():
    return webapp.WSGIApplication(ROUTES,debug=True)
                                        
def main():
    wsgiref.handlers.CGIHandler().run(createMainApplication())

if __name__ == '__main__':
    main()