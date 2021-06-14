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

    '''
    User-related endpoints
        '''

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

    @app.route('/users/<id>', methods=['PATCH'])
    def update_user(id):
        error = False
        try:
            data = request.get_json()
            user = Users.query.get(id)

            if user:
                user.user_name = data.get('user_name').strip()
                user.user_role = data.get('user_role').strip()

                user.update()

                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'message': 'User updated'
                })
            else:
                abort(404)

        except Exception as e:
            print(e)
            error = True

    @app.route('/users/<id>', methods=['DELETE'])
    def delete_user(id):
        error = False
        try:
            data = request.get_json()
            user = Users.query.get(id)

            if user:
                user.delete()

                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'message': 'User deleted'
                })
            else:
                abort(404)

        except Exception as e:
            print(e)
            error = True

    '''
    Category-related endpoints
        '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        error = False
        try:
            categories = (
                Categories.query
                .order_by(Categories.id)
                .all()
            )

            if len(categories):
                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'categories': [category.cat_name for category in categories]
                })
            else:
                abort(404)

        except Exception as e:
            print(e)
            error = True

    @app.route('/categories', methods=['POST'])
    def add_category():
        error = False
        try:
            data = request.get_json()
            cat_name = data['cat_name'].strip()
            new_cat = Categories(
                cat_name=cat_name
            )

            new_cat.insert()

            return jsonify({
                'status_code': 200,
                'success': True,
                'message': 'Created new category'
            })

        except Exception as e:
            print(e)
            error = True

    @app.route('/categories/<id>', methods=['PATCH'])
    def update_category(id):
        error = False
        try:
            data = request.get_json()
            category = Categories.query.get(id)

            if category:
                category.cat_name = data.get('cat_name').strip()
                category.update()

                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'message': 'Category updated'
                })
            else:
                abort(404)

        except Exception as e:
            print(e)
            error = True

    @app.route('/categories/<id>', methods=['DELETE'])
    def delete_category(id):
        error = False
        try:
            data = request.get_json()
            category = Categories.query.get(id)

            if category:
                category.delete()

                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'message': 'Category deleted'
                })
            else:
                abort(404)

        except Exception as e:
            print(e)
            error = True

    '''
    Chore-related endpoints
        '''

    @app.route('/chores', methods=['GET'])
    def get_chores():
        error = False
        try:
            chores = (
                Chores.query
                .order_by(Chores.id)
                .all()
            )

            chore_list = {
                chore.chore_name: chore.status for chore in chores
            }

            if len(chores):
                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'chores': chore_list
                })
            else:
                abort(404)

        except Exception as e:
            print(e)
            error = True

    @app.route('/chores', methods=['POST'])
    def add_chore():
        error = False
        try:
            data = request.get_json()
            chore_name = data['chore_name'].strip()
            recurrence = data['recurrence'].strip()
            category_id = data['category_id']
            user_id = data['user_id']
            status = data['status'].strip()
            points = data['points']

            new_chore = Chores(
                chore_name=chore_name,
                recurrence=recurrence,
                category_id=category_id,
                user_id=user_id,
                status=status,
                points=points
            )

            new_chore.insert()

            return jsonify({
                'status_code': 200,
                'success': True,
                'message': 'Created new chore'
            })

        except Exception as e:
            print(e)
            error = True

    return app
