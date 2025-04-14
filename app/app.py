# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flaskext.mysql import MySQL

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'app'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'appdb'
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("create table newtable (col int)")
    cursor.execute("insert into newtable (col) values (1)")
    cursor.execute("insert into newtable (col) values (1)")
    cursor.execute("select * from newtable")
    data = cursor.fetchone()
    return str(data)

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port='5000')

