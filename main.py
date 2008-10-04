import wsgiref.handlers,logging
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):

  def get(self,url=None):
    self.response.out.write('Hello world!')

def main():
  wsgiref.handlers.CGIHandler().run(createMainApplication())

if __name__ == '__main__':
  main()

def createMainApplication():
    return webapp.WSGIApplication([(r'/(.*)', MainHandler)],
                                        debug=True)