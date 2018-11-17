import pymysql
import traceback
from lib.loggingConf import logging
from . import mysqlCon


def home_index_sql():
    db = pymysql.connect(mysqlCon.db_url, mysqlCon.db_username, mysqlCon.db_password, mysqlCon.db_name)
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
    return api_list


def list_users():
    db = pymysql.connect(mysqlCon.db_url, mysqlCon.db_username, mysqlCon.db_password, mysqlCon.db_name)
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
    return api_list


def list_user(user_id):
    db = pymysql.connect(mysqlCon.db_url, mysqlCon.db_username, mysqlCon.db_password, mysqlCon.db_name)
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
            pass
    except Exception as e:
        logging.debug("%s failed!" % sql)
        logging.debug(e)
        traceback.print_exc()

    db.close()
    return user


def add_user(new_user):
    db = pymysql.connect(mysqlCon.db_url, mysqlCon.db_username, mysqlCon.db_password, mysqlCon.db_name)
    cursor = db.cursor()
    logging.debug("connect mydb success!")

    sql = ''
    data = ()
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
    except Exception as e:
        db.rollback()
        logging.debug("%s failed!" % sql)
        logging.debug(e)
        traceback.print_exc()

    db.close()
    return True
