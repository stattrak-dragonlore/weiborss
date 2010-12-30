from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from rss163 import Rss163


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, weiborss!!!')

class NotFound(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('404 Not found!')


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/163/.*', Rss163),
                                      ('/.*', NotFound)],
                                     debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
