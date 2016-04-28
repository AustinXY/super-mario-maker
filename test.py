import psycopg2

# Adapted from with heavy modifications from CA optional lecture on databases

class Struct(object): pass

data = Struct()

def connect():
    # host = "dirtyding.us.to"
    # host = "104.33.219.122"
    host = "localhost"
    db = "15112TP"
    user = "postgres"
    pw = "postgres"

    data.conn = psycopg2.connect(host = host, database = db, user = user, password = pw)
    data.cur = data.conn.cursor()
    initdb(data)

def initdb(data):
    query = """DROP TABLE IF EXISTS user_levels"""
    data.cur.execute(query)
    query = """CREATE TABLE user_levels (level_name varchar, level varchar, creator varchar, plays int, passes int);"""
    data.cur.execute(query)

def getLevels(data):
    query = """SELECT * from user_levels;"""
    data.cur.execute(query)
    levels = data.cur.fetchall()
    return levels

def login(data, user, pw):
    query = """SELECT password from user_logins WHERE username = %s;""" % (user)
    data.cur.execute(query)
    results = data.cur.fetchall
    if(results = []):
        return "no user"
    elif(results [0] != pw):
        return "wrong pw"
    else:
        return True

def makeAccount(data, user, pw):
    query = """SELECT PASSWORD from user_logins WHERE username = %s;""" % (user)
    data.cur.execute(query)
    results = data.cur.fetchall
    if(results = []):
        query = """INSERT into user_logins (username, password) VALUES (%s, %s)""" % (user, pw)
    else:
        return False

def processLevel(level):
    for row in range(len(level)):
        for col in range(len(level[0])):
            pass

def postLevel(data, name, level, creator):
    # level = "\'" + str(level) + "\'"
    query = """INSERT into user_levels (level_name, level, creator) VALUES (%s, %s, %s)""" % (name, level, creator)
    data.cur.execute(query)

def downloadLevel(data, name):
    query = """SELECT level from user_levels WHERE level_name = %s;""" % (name)
    data.cur.execute(query)
    level = data.cur.fetchall()
    if(level != ""):
        levelMap = eval(level)
        
        query = """SELECT creator from user_levels WHERE level_name = %s;""" % (name)
        data.cur.execute(query)
        name = data.cur.fetchall()
        creator = name

        return levelMap, creator
    else:
        return None