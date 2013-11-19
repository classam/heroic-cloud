try:
    from google.appengine.ext import ndb
except ImportError:
    from stubs import ndb

class User(ndb.entity):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    properties = ndb.JsonProperty(indexed=False)


class GoogleUser(ndb.entity):
    user = ndb.UserProperty(required=True)


class NonGoogleUser(ndb.entity):
    username = ndb.StringProperty()
    password = ndb.StringProperty(indexed=False)


def passhash(password):
    # TODO: consider passlib
    # TODO TODO: consider not storing passwords
    import hashlib, uuid
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password, salt


class Session(ndb.entity):
    created = ndb.DateTimeProperty(auto_now_add=True)
    token = ndb.StringProperty()
    user = ndb.KeyProperty(indexed=False, kind=User)

    @classmethod
    def create(cls, userkey):
        return cls(token=uuid.uuid4().hex, parent=userkey)

    @classmethod
    def user(cls, token):
        query = cls.query(cls.token==token)
        returned = query.get()
        if returned:
            return returned.#TODO PARENT CALL.get()
        else:
            return None


class CreateUser(webapp2.RequestHandler):
    def post(self):
        pass
        # create User
        # create Session


class UpgradeUser(webapp2.RequestHandler):
    def post(self):
        token = self.request.get('token')
        user = Session.user(token)

        username = self.request.get('username')
        password = self.request.get('password')
        user = users.get_current_user()

        if user:

        pass
        # if name/password OR google token with



def urls():
    urls = [
        (r'/user', CreateUserHandler)
    ]
    return urls

