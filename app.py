import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

from models import setup_db, db, Categories, Users, Chores
from auth import AuthError, requires_auth


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
        return render_template('pages/home.html')

    '''
    User-related endpoints
        '''

    @app.route('/users', methods=['GET'])
    @requires_auth('get:users')
    def get_users(f):
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
                abort(404)

        except Exception as e:
            print(e)
            abort(404)

    @app.route('/users', methods=['POST'])
    @requires_auth('post:users')
    def add_user(f):
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
                'message': 'User created'
            })

        except Exception as e:
            error = True
            print(e)
            abort(422)

    @app.route('/users/<id>', methods=['PATCH'])
    @requires_auth('patch:users')
    def update_user(f, id):
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

        except Exception as e:
            error = True
            print(e)
            abort(404)

    @app.route('/users/<id>', methods=['DELETE'])
    @requires_auth('delete:users')
    def delete_user(f, id):
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
            error = True
            print(e)
            abort(404)

    '''
    Category-related endpoints
        '''

    @app.route('/categories', methods=['GET'])
    @requires_auth('get:categories')
    def get_categories(f):
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
                    'categories': [category.cat_name for
                                   category in categories]
                })
            else:
                abort(404)

        except TypeError as e:
            error = True
            print(e)
            abort(404)

    @app.route('/categories', methods=['POST'])
    @requires_auth('post:categories')
    def add_category(f):
        error = False
        try:
            data = request.get_json()
            cat_name = data['cat_name'].strip()
            new_cat = Categories(
                cat_name=cat_name
            )

            new_cat.insert()

            return jsonify({
                'status_code': 201,
                'success': True,
                'message': 'Created new category'
            })

        except Exception as e:
            error = True
            print(e)
            abort(422)

    @app.route('/categories/<id>', methods=['PATCH'])
    @requires_auth('patch:categories')
    def update_category(f, id):
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

        except Exception as e:
            error = True
            print(e)
            abort(404)

    @app.route('/categories/<id>', methods=['DELETE'])
    @requires_auth('delete:categories')
    def delete_category(f, id):
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
            error = True
            print(e)
            abort(404)

    '''
    Chore-related endpoints
        '''

    @app.route('/chores', methods=['GET'])
    @requires_auth('get:chores')
    def get_chores(f):
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

        except TypeError as e:
            error = True
            print(e)
            abort(404)

    @app.route('/chores', methods=['POST'])
    @requires_auth('post:chores')
    def add_chore(f):
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
                'status_code': 201,
                'success': True,
                'message': 'Created new chore'
            })

        except Exception as e:
            error = True
            print(e)
            abort(422)

    @app.route('/chores/<id>', methods=['PATCH'])
    @requires_auth('patch:chores')
    def update_chore(f, id):
        error = False
        try:
            data = request.get_json()
            chore = Chores.query.get(id)

            if chore:
                chore.chore_name = data.get('chore_name').strip()
                chore.recurrence = data.get('recurrence').strip()
                chore.category_id = data.get('category_id')
                chore.user_id = data.get('user_id')
                chore.status = data.get('status').strip()
                chore.points = data.get('points')

                chore.update()

                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'message': 'Chore updated'
                })

        except Exception as e:
            error = True
            print(e)
            abort(404)

    @app.route('/chores/<id>', methods=['DELETE'])
    @requires_auth('delete:chores')
    def delete_chore(f, id):
        error = False
        try:
            data = request.get_json()
            chore = Chores.query.get(id)

            if chore:
                chore.delete()

                return jsonify({
                    'status_code': 200,
                    'success': True,
                    'message': 'Chore deleted'
                })
            else:
                abort(404)

        except Exception as e:
            error = True
            print(e)
            abort(404)

    '''
    Erorr handlers
        '''

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'status_code': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def not_processed_error(error):
        return jsonify({
            'success': False,
            'status_code': 422,
            'message': 'Your request could not be processed'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'status_code': 500,
            'message': 'The server did not understand your request'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5150, debug=True)
