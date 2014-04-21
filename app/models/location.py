from app import db
from hashlib import md5
import random
import string

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


