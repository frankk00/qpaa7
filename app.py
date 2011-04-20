# watch a TPB user for new uploads

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.urlfetch import fetch
from google.appengine.ext import db
from google.appengine.api import memcache

from BeautifulSoup import BeautifulSoup
import cgi
import re
import qpaa7

class MainPage(webapp.RequestHandler):
    def get(self):
        cache_key = 'html'

        self.response.headers['Content-Type'] = 'text/html'
        html = memcache.get(cache_key)
        #html = None
        if html is None:
            # cache expired, time to update the db
            try:
                fetch_ob = fetch('http://www.blasldkjasds.com/qpfc/')
                html = fetch_ob.content
            except:
                pass

            code = fetch_ob.status_code
            if code != 200:
                html = 'Failed to fetch url: %d' % code
                self.response.out.write('Oops, broken. :(<br>Failed to fetch url, code %d' % code)
                return

            memcache.add(cache_key, html, 300)

        out_html = qpaa7.get_html(html)
        self.response.out.write(out_html)


application = webapp.WSGIApplication(
    [('/', MainPage)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
