import pymysql

db = pymysql.connect("localhost", "root", "123456", "mydb")

cursor = db.cursor()

sql = ''
#sql = 'INSERT INTO apirelease (version, buildtime, links, methods) VALUES ' \
#      '("v1", "2017-01-01 10:00:00", "/api/v1/users", "get, post, put, delete"); '
sql = 'INSERT INTO users (username, email, password, full_name) VALUES ' \
      '("manish123", "manishest@gmail.com", "manish123", "Manish"); '

try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

db.close()
