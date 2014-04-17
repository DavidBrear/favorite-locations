from app import db
from hashlib import md5
import random
import string

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    locations = db.relationship('Location', backref = 'creator', lazy = 'dynamic')

    password_salt = db.Column(db.String(16))
    password_digest = db.Column(db.String(128))

    last_login = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def authenticate(self, password):
        if self.password_digest == md5(password + self.password_salt).hexdigest():
            return True
        return False


    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1

        return new_nickname

    @staticmethod
    def generate_password_salt():
        salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        return salt
    @staticmethod
    def generate_password_digest(password, salt):
        return md5(password + salt).hexdigest()


class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), index = True)
    address = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return '<Location %r>' % (self.name)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'name': self.name,
           'address': self.address,
           'latitude': self.latitude,
           'longitude': self.longitude
       }

