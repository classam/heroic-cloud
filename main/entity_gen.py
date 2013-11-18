from property_gen import generate_property, CantParse

try:
    from google.appengine.ext import ndb
except ImportError:
    from stubs import ndb


EVENT_CHOICES = ['create', 'update', 'delete']


def generate_entity(name, properties):
    """
        Documentation!
    """
    fields = {
        'title': ndb.StringProperty(indexed=False),
        'slug': ndb.StringProperty(required=True, indexed=True),
        'created': ndb.DateTimeProperty(auto_now_add=True, indexed=False),
        'last_update': ndb.DateTimeProperty(auto_now=True, indexed=True),
    }

    for typename, typestring in properties.iteritems():
        if type(typestring) != str:
            continue
        ndb_prop = generate_property(typestring)
        if ndb_prop:
            fields[typename] = ndb_prop

    cls = type(name,
               (ndb.entity, object),
               fields)

    return cls
