import wsgiref.handlers,logging, presenter, os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):

    def get(self,url=None):
        pointset = presenter.get_points_for(url)
        template_values = {'points':pointset}
        path = "templates/index.html"
        # path = os.path.join(os.path.dirname(__file__), '../mappr/templates/index.html')
        self.response.out.write(template.render(path,template_values ))

def main():
    wsgiref.handlers.CGIHandler().run(createMainApplication())

if __name__ == '__main__':
    main()

def createMainApplication():
    return webapp.WSGIApplication([(r'/(.*)', MainHandler)],
                                        debug=True)