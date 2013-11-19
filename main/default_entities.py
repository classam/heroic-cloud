try:
    from google.appengine.ext import ndb
except ImportError:
    from stubs import ndb

EVENT_CHOICES = ['create', 'update', 'delete']


class User(ndb.entity):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    properties = ndb.JsonProperty(indexed=False)


class Workspace(ndb.entity):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    owners = ndb.KeyProperty(repeated=True, kind=User)
    channel = ndb.StringProperty(indexed=False)


class GoogleUser(ndb.entity):
    user = ndb.UserProperty(required=True)


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
