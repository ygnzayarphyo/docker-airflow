import MySQLdb

database = {
    "host": "mysql",
    "port": 3306,
    "user": "root",
    "password": "root",
    "db": "db_user"
}

def get_connection():
	return MySQLdb.connect(
        host = database["host"],
        user = database["user"],
        password = database["password"],
        db = database["db"],
        charset = 'utf8')