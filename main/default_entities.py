try:
    from google.appengine.ext import ndb
except ImportError:
    from stubs import ndb


class Workspace(ndb.entity):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    owners = ndb.KeyProperty(repeated=True, kind=DefaultEntities.User)
    channel = ndb.StringProperty(indexed=False)


class User(ndb.entity):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    properties = ndb.JsonProperty(indexed=False)


class GoogleUser(ndb.entity):
    user = UserProperty(required=True)


class Event(ndb.entity):
    """
        'create' 'deck/9283/cards/2931'  {...}
        'update' 'deck/9283/cards/2931'  {...}
        'delete' 'deck/9283/cards/2931'  {...}
    """
    action = StringProperty(indexed=True, choices=EVENT_CHOICES)
    entity = KeyProperty(indexed=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    values = JsonProperty(indexed=False)
