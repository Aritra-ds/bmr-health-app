import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: Flask-Login settings
    LOGIN_VIEW = 'login'
