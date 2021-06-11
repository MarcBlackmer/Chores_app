import os
from sqlalchemy importdb.Column, db.String, db.Integer
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD', '')
DB_NAME = os.getenv('DB_NAME', 'chores')
DB_PATH = 'postgresql://{}@{}/{}'.format(DB_HOST, DB_NAME, DB_USER, DB_PWD)

db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = app
        db.init_app(app)
        db.create_all()
    except Exception as e:
        print(e)
    return ('Database set up complete')


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(5), primary_key=True)
    cat_name = db.Column(db.String(20), unique=True, nullable=False)


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(3), primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)


class Chores(db.Model):
    __tablename__ = 'chores'

    id = db.Column(db.Integer(5), primary_key=True)
    chore_name = db.Column(db.String(150), unique=True, nullable=False)
    recurrence = db.Column(db.String(15), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    points = db.Column(db.Integer(3), nullable=False)
