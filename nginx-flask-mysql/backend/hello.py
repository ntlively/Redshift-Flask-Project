import os
from flask import Flask
import mysql.connector
import psycopg2
from decouple import config
import mpld3
import matplotlib.pyplot as plt



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
    hostname = config('hostname')

    conn = psycopg2.connect(database="dev", user = userID, password = pw, host = hostname, port = "5439")
    cursor = conn.cursor()
    cursor.execute('SELECT qtysold FROM sales;')


    fig = plt.figure()
    y_coords = []
    x_coords = []
    for index, row in enumerate(cursor.fetchall()):
        y_coords.append(row[0])
        x_coords.append(index)
        #print("\nData:"+ str(row[0]))
    

    plt.plot(x_coords,y_coords, marker = 'o', color='darkcyan', linestyle='none')

    response = str(mpld3.fig_to_html(fig, template_type='simple'))
    return response


if __name__ == '__main__':
    server.run()
