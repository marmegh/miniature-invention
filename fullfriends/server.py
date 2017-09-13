from flask import Flask, request, redirect, render_template, session, flash
import datetime
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friends')
@app.route('/')
def index():
    query = ("SELECT name, age, DATE_FORMAT(created_at, '%M %D') AS day, DATE_FORMAT(created_at, '%Y') AS year FROM friends")
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends = friends)
@app.route('/friends', methods=['POST'])
def create():
    name = request.form['name']
    age = request.form['age']
    #insert new friends into mySQL
    # query = "INSERT INTO friends (name, age, created_at, updated_at) VALUES (:name, :age, NOW(), NOW())"
    data = {
             'name': request.form['name'],
             'age': request.form['age']
           }
    query = 'INSERT INTO friends (name, age, created_at, updated_at) VALUES (:name, :age, NOW(), NOW())'
    print query
    mysql.query_db(query, data)
    return redirect('/')
app.run(debug=True)