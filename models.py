import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

'''
    App_state looks for "dev" to run locally, otherwise we will assume the app
    is running in production on Heroku

    '''

APP_STATE = os.getenv('APP_STATE')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD')
DB_NAME = os.getenv('DB_NAME')
# DB_PATH refers to a local installation
DB_PATH = 'postgresql://{}@{}/{}'.format(DB_USER, DB_HOST, DB_NAME, DB_PWD)

# Check to see if we'll use a local DB connection or Heroku
if APP_STATE == 'local':
    database_path = DB_PATH
else:
    # DATABASE_URL is the required variable name used by Heroku
    database_path = os.getenv('DATABASE_URL')

'''
    Heroku still uses 'postgres' in its connection strings, which has been
    deprecated by SQLAlchemy and is no longer supported. This check will
    correct the string as it is not editable within Heroku

    '''

if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)


db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = app
        db.init_app(app)
        db.create_all()
    except Exception as e:
        print(e)
    return ('Database set up complete')


def insert_record(self):
    db.session.add(self)
    db.session.commit()


def update_record(self):
    db.session.commit()


def delete_record(self):
    db.session.delete(self)
    db.session.commit()


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, cat_name):
        self.cat_name = cat_name

    def insert(self):
        insert_record(self)

    def update(self):
        update_record(self)

    def delete(self):
        delete_record(self)

    def __repr__(self):
        return f'<ID: { self.id }, Category: { self.cat_name }>'


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_role = db.Column(db.String(10), nullable=False)

    def __init__(self, user_name, user_role):
        self.user_name = user_name
        self.user_role = user_role

    def insert(self):
        insert_record(self)

    def update(self):
        update_record(self)

    def delete(self):
        delete_record(self)

    def __repr__(self):
        return f'<ID: { self.id }, Name: { self.user_name }, \
        Role: { self.user_role }>'


class Chores(db.Model):
    __tablename__ = 'chores'

    id = db.Column(db.Integer, primary_key=True)
    chore_name = db.Column(db.String(150), unique=True, nullable=False)
    recurrence = db.Column(db.String(15), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __init__(self, chore_name, recurrence, category_id, user_id,
                 status, points):
        self.chore_name = chore_name
        self.recurrence = recurrence
        self.category_id = category_id
        self.user_id = user_id
        self.status = status
        self.points = points

    def insert(self):
        insert_record(self)

    def update(self):
        update_record(self)

    def delete(self):
        delete_record(self)

    def __repr__(self):
        return f'<ID: { self.id }, Name: { self.chore_name }, \
        Schedule: { self.recurrence }, Status { self.status } \
        Points: { self.points }>'
