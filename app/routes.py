from app import app
from flask import render_template, request
from flask_mysqldb import MySQL

mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        input = request.form
        username = input['username']
        email = input['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Users(Username, Email) VALUES (%s, %s)", (username, email))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('login.html')