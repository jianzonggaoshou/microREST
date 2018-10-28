from flask import Flask
from flask import jsonify
import pymysql
from lib.loggingConf import logging


app = Flask(__name__)


@app.route("/api/v1/info", methods=['GET'])
def home_index():
    db = pymysql.connect("localhost", "root", "123456", "mydb")
    cursor = db.cursor()
    logging.debug("connect mydb success!")

    sql = ''
    api_list = []
    try:
        sql = 'SELECT version, buildtime, methods, links from apirelease'
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
