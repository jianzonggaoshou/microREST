from flask import Flask
from flask import jsonify
import pymysql
from lib.loggingConf import logging


app = Flask(__name__)


@app.route("/api/v1/info", methods=['GET'])
def home_index():
    db = pymysql.connect("114.116.74.221", "root", "Huawei12#$", "mydb")
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
    except:
        logging.debug("%s failed!" % sql)

    db.close()
    return jsonify({'api_version': api_list}), 200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()


def list_users():
    db = pymysql.connect("114.116.74.221", "root", "Huawei12#$", "mydb")
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
    except:
        logging.debug("%s failed!" % sql)

    db.close()
    return jsonify({'user_list': api_list}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
