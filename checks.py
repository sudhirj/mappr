import wsgiref.handlers,logging, gateway, os, settings
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from helpers import utils
from google.appengine.api import users

class UrlCheckHandler(webapp.RequestHandler):
    def get(self,url=None):
        if gateway.check_if_url_exists(url):
            self.response.out.write('Y')
        else:
            self.response.out.write('N')

        
    
ROUTES =[
            (r'/_check/url/(.*)', UrlCheckHandler)
        ]

def createMainApplication():
    return webapp.WSGIApplication(ROUTES,debug=settings.debug)
                                        
def main():
    wsgiref.handlers.CGIHandler().run(createMainApplication())

if __name__ == '__main__':
    main()