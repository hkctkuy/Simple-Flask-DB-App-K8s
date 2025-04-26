# Importing os module to be able to access environment variables
import os

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flaskext.mysql import MySQL

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('MYSQL_PORT'))
mysql.init_app(app)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("create table if not exists newtable (col char(15))")
    cursor.execute("insert into newtable (col) values ('Hello, World!')")
    cursor.execute("select * from newtable")
    data = cursor.fetchone()
    return str(data[0])


# Main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0', port=5000)
