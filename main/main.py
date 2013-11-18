import json

try:
    from google.appengine.api import channel
except ImportError: 
    from stubs import channel


# The most basic WSGI application
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [json.dumps(channel.create_channel("hobo-fight") )]
