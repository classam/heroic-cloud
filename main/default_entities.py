from user import User
from uuid import uuid4

try:
    from google.appengine.ext import ndb
    from google.appengine.api import users
except ImportError:
    from stubs import ndb, users

EVENT_CHOICES = ['create', 'update', 'delete']



class Workspace(ndb.entity):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    owners = ndb.KeyProperty(repeated=True, kind=User)


class Channel(ndb.entity):
    channel = ndb.StringProperty()


class Event(ndb.entity):
    """
        'create' 'deck/9283/cards/2931'  {...}
        'update' 'deck/9283/cards/2931'  {...}
        'delete' 'deck/9283/cards/2931'  {...}
    """
    action = ndb.StringProperty(indexed=True, choices=EVENT_CHOICES)
    entity = ndb.KeyProperty(indexed=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    values = ndb.JsonProperty(indexed=False)
    initiated_by = ndb.KeyProperty(indexed=False, kind=User)



class CreateWorkspaceHandler(webapp2.RequestHandler):
    def post(self):
        token = self.request.get('token')
        if token != '':
            session = Session.find(token)
            if session:
                user = session.user
            else:
                user = None
        else:
            user = None

        if not user:
            # throw an error: you must have a valid token to
            #   create a workspace

        if user:
            pass

