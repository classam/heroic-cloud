import random_name
import uuid
import logging
import json
import webapp2

try:
    from google.appengine.ext import ndb
    from google.appengine.api import users
except ImportError:
    from stubs import ndb
    from stubs import users

class User(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    properties = ndb.JsonProperty(indexed=False)
    has_password = ndb.BoolProperty(indexed=True, default=False)
    has_googleuser = ndb.BoolProperty(indexed=True, default=False)

    # Google Login
    googleuser = ndb.UserProperty()

    # Noogle Login
    username = ndb.StringProperty()
    password = ndb.StringProperty(indexed=False)
    salt = ndb.StringProperty(indexed=False)

    @classmethod
    def by_username(cls, username):
        query = cls.query(cls.username == username)
        return query.get()
    
    @classmethod
    def unique_user(cls, tries=0):
        if tries < 3:
            candidates = [random_name.name() for x in range(0,5)]
        else:
            candidates = [uuid.uuid4().hex for x in range(0,5)]

        query = cls.query(cls.username.IN(candidates))
        hits = query.fetch(5)
        existing_usernames = [user.username for user in hits]
        for name in existing_usernames:
            candidates.remove(name)

        if len(candidates) == 0 and tries < 5:
            logging.warning("unique_user couldn't create a unique user: trying again")
            tries=tries+1
            return cls.unique_username(tries)
        if len(candidates) == 0 and tries >= 6:
            logging.critical("unique_user couldn't create a unique user at all")
            return None
        else:
            return cls(username=candidates[0])
        
    @staticmethod
    def salt():
        return uuid.uuid4().hex

    @staticmethod 
    def passhash(password, salt):
        import hashlib
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        return hashed_password



class Session(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    token = ndb.StringProperty()
    ip = ndb.StringProperty(indexed=False)

    @classmethod
    def create(cls, user, ip):
        return cls(token=user.username+"-"+uuid.uuid4().hex, ip=ip, parent=user.key)

    @classmethod
    def session(cls, token, ip):
        query = cls.query(cls.token==token)
        s = query.get()
        if s and s.ip == ip:
            return s
        else:
            return None


class CreateSessionHandler(webapp2.RequestHandler):
    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        googleuser = users.get_current_user()
        
        if username and password:
            u = User.authenticate(username, password)
        elif googleuser:
            u = User.googleuser(googleuser)
        else:
            u = User.unique_user()
            u.put()

        if not u:    #no u
            self.response.write("ERRAR")
        else:
            s = Session.create(u, self.request.remote_addr)
            s.put()
            self.response.write(s.token)


class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        s = Session.session(token, self.request.remote_addr)
        if s:
            user = s.key.parent().get()

            # TODO: LOGIC LOGIC LOGIC


        else:
            self.response.write("Nope")


class SessionCheckHandler(webapp2.RequestHandler):
    def get(self, token):
        s = Session.session(token, self.request.remote_addr)
        if s:
            self.response.write(s)
        else:
            self.response.write("Nope")


def urls(debug=True):
    urls = [
        (r'/session', CreateSessionHandler), 
        (r'/register', RegisterHandler
    ]
    if debug:
        urls.append( (r'/session/([\w-]+)', SessionCheckHandler) )
    return urls

