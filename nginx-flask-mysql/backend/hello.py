import os
from flask import Flask
import mysql.connector
import psycopg2
from decouple import config




class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker-compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
        self.connection.commit()
    
    def query_titles(self):
        self.cursor.execute('SELECT firstname, lastname, total_quantity FROM   (SELECT buyerid, sum(qtysold) total_quantity FROM  sales GROUP BY buyerid ORDER BY total_quantity desc limit 10) Q, users WHERE Q.buyerid = userid ORDER BY Q.total_quantity desc;')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


server = Flask(__name__)


@server.route('/')
def listBlog():
    userID = config('userID')
    pw = config('pw')
    
    print(userID, pw)
    conn = psycopg2.connect(database="dev", user = userID, password = pw, host = "redshift-cluster-1.ccs6bshicmph.us-east-1.redshift.amazonaws.com", port = "5439")
    cursor = conn.cursor()
    cursor.execute('SELECT firstname, lastname, total_quantity FROM   (SELECT buyerid, sum(qtysold) total_quantity FROM  sales GROUP BY buyerid ORDER BY total_quantity desc limit 10) Q, users WHERE Q.buyerid = userid ORDER BY Q.total_quantity desc;')
    rec = []
    for row in cursor.fetchall():
        rec.append(row[0])
    response = ''
    response = response  + '<div>   Hello  ' + "".join([str(i) for i in rec]) + '</div>'
    return response


if __name__ == '__main__':
    server.run()
