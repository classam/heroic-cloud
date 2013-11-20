import json
import webapp2

import user
from utils import EchoHandler

#try:
#    from google.appengine.api import channel
#except ImportError: 
#    from stubs import channel
# The most basic WSGI application
#def application(environ, start_response):
#    start_response('200 OK', [('Content-Type', 'application/json')])
#    return [json.dumps(channel.create_channel("hobo-fight") )]

debug=True

class HelloWorldHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, world.")

routes = user.urls(debug) + [
            ('/', HelloWorldHandler),
        ]

if debug:
    routes.append( ('/echo', EchoHandler) )

application = webapp2.WSGIApplication(routes=routes, debug=debug, config={})
