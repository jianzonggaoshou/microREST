from flask import Flask
from flask import jsonify
from flask import abort
from flask import request
import pymysql
import traceback
from lib.loggingConf import logging


app = Flask(__name__)

db_url = "114.116.74.221"
db_username = "root"
db_password = "Huawei12#$"
db_name = "mydb"


@app.route("/api/v1/info", methods=['GET'])
def home_index():
    db = pymysql.connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    logging.debug("connect mydb success!")

    sql = ''
    api_list = []
    try:
        sql = 'SELECT version, buildtime, methods, links FROM apirelease'
        logging.debug(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        logging.debug(results)

        for row in results:
            api = {}
            api['version'] = row[0]
            api['bulidtime'] = row[1]
            api['methods'] = row[2]
            api['links'] = row[3]
            api_list.append(api)
    except Exception as e:
        logging.debug("%s failed!" % sql)
        logging.debug(e)
        traceback.print_exc()

    db.close()
    return jsonify({'api_version': api_list}), 200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()


def list_users():
    db = pymysql.connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    logging.debug("connect mydb success!")

    sql = ''
    api_list = []
    try:
        sql = 'SELECT username, full_name, email, password, id FROM users'
        logging.debug(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        logging.debug(results)

        for row in results:
            a_dict = {}
            a_dict['username'] = row[0]
            a_dict['full_name'] = row[1]
            a_dict['email'] = row[2]
            a_dict['password'] = row[3]
            a_dict['id'] = row[4]
            api_list.append(a_dict)
    except Exception as e:
        logging.debug("%s failed!" % sql)
        logging.debug(e)
        traceback.print_exc()

    db.close()
    return jsonify({'user_list': api_list}), 200


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


def list_user(user_id):
    db = pymysql.connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    logging.debug("connect mydb success!")

    sql = ''
    user = {}
    try:
        sql = 'SELECT id, username, email, password, full_name FROM users WHERE id="%s"' % user_id
        logging.debug(sql)
        cursor.execute(sql)
        results = cursor.fetchone()
        logging.debug(results)
        if results:
            user['id'] = results[0]
            user['username'] = results[1]
            user['email'] = results[2]
            user['password'] = results[3]
            user['full_name'] = results[4]
            logging.debug(user)
        else:
            abort(404)
    except Exception as e:
        logging.debug("%s failed!" % sql)
        logging.debug(e)
        traceback.print_exc()

    db.close()
    return jsonify(user), 200


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

    return add_user(user)


def add_user(new_user):
    db = pymysql.connect(db_url, db_username, db_password, db_name)
    cursor = db.cursor()
    logging.debug("connect mydb success!")

    sql = ''
    try:
        sql = 'SELECT * FROM users WHERE username="%s" or email="%s"' % (new_user['username'], new_user['email'])
        logging.debug(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        logging.debug(data)
    except Exception as e:
        logging.debug("%s failed!" % sql)
        logging.debug(e)
        traceback.print_exc()

    try:
        if not data:
            sql = 'INSERT INTO users(username, email, password, full_name) VALUES ("%s", "%s", "%s", "%s")' \
                  % (new_user['username'], new_user['email'], new_user['password'], new_user['full_name'])
            logging.debug(sql)
            cursor.execute(sql)
            db.commit()

        else:
            abort(400)
    except Exception as e:
        db.rollback()
        logging.debug("%s failed!" % sql)
        logging.debug(e)
        traceback.print_exc()

    db.close()
    result = 'success add!'
    return jsonify({'status': result}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
