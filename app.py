from flask import Flask
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response
from lib import sqlLib
from lib.loggingConf import logging


app = Flask(__name__)


@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)


@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)


@app.route("/api/v1/info", methods=['GET'])
def home_index():
    result_list = sqlLib.home_index_sql()
    logging.debug(result_list)
    return jsonify({'api_version': result_list}), 200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    result_list = sqlLib.list_users()
    logging.debug(result_list)
    return jsonify({'user_list': result_list}), 200


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    result_dict = sqlLib.list_user(user_id)
    logging.debug(result_dict)
    if result_dict:
        return jsonify(result_dict), 200
    else:
        abort(404)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not ('username' in request.json) or not ('email' in request.json) or \
       not ('password' in request.json):
        abort(400)

    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'full_name': request.json.get('full_name', ''),
        'password': request.json['password'],
    }

    logging.debug(user)

    result_bool = sqlLib.add_user(user)
    logging.debug(result_bool)
    if result_bool:
        content = 'success add!'
        return jsonify({'status': content}), 201
    else:
        abort(409)


@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not ('username' in request.json):
        abort(400)

    user = request.json['username']
    logging.debug(user)
    result_bool = sqlLib.del_user(user)
    logging.debug(result_bool)
    if result_bool:
        content = 'success delete!'
        return jsonify({'status': content}), 200
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
