

from mysql.connector import connect as mysql_connect
LANG = "GNU C++11"
# LANG = "GNU C"
EXTENSION = ".cpp"
MIN_TEST_CASES = 20

db_conf = {
    "host": "127.0.0.1",
    "port": "3306",
    "user": "root",
    "password": "password",
    "database": "code4bench",
}


def connect(conf=None):
    if conf is None:
        conf = db_conf
    db = mysql_connect(**conf)
    db.ping()
    cur = db.cursor(prepared=True)
    return db, cur
