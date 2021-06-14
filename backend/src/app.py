import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

from .database.models import setup_db, db, Categories, Users, Chores


def create_app(app):
    # Get the environment variables
    load_dotenv(find_dotenv())

    # Set up the app and create the database
    app = Flask(__name__)
    setup_db(app)

    migrate = Migrate(app, db)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'success': True,
            'message': 'Nothing to see here - yet'
        }), 200

    @app.route('/users', methods=['GET'])
    def get_users():
        error = False
        try:
            users = (
                Users.query
                .order_by(Users.id)
                .all()
            )

            user_list = {
                user.user_name: user.user_role for user in users
            }

            if len(users):
                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'users': user_list
                })
            else:
                abort(422)

        except Exception as e:
            print(e)
            error = True

    @app.route('/users', methods=['POST'])
    def add_user():
        error = False
        try:
            data = request.get_json()
            new_user = data['user_name'].strip()
            user_role = data['user_role'].strip()
            user_acct = Users(
                user_name=new_user,
                user_role=user_role
            )

            user_acct.insert()

            return jsonify({
                'status_code': 200,
                'success': True,
                'message': 'That may have worked. Who knows?'
            })

        except Exception as e:
            print(e)
            error = True

    return app
