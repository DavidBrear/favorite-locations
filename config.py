import os

# CSRF STUFF
CSRF_ENABLED = True
SECRET_KEY = 'This-is-a-VERY-long-String-with-many different possible WAYS of typing thiNGS!!1! Please dont guess me! :( <3'

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
#
#MAIL_SERVER = 'localhost'
#MAIL_PORT = 25
#MAIL_USERNAME = None
#MAIL_PASSWORD = None

# administrator list
ADMINS = ['davidbrear04@gmail.com']
