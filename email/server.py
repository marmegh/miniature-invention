from flask import Flask, request, redirect, render_template, session, flash
import datetime
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "CakeByTheOcean"
mysql = MySQLConnector(app,'friends')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    temp = request.form['email']
    query1 = ("SELECT email FROM accounts")
    something = mysql.query_db(query1)
    for x in range(0,len(something)):
        print something[x]['email']
        if temp == something[x]['email']:
            flash('Invalid entry! Try again!')
            return redirect('/')
    data = {
            'email' : temp
            }
    query2 = ("INSERT INTO accounts (email, created_at) VALUES(:email, NOW())")
    mysql.query_db(query2, data)
    print "SUCCESS!!!!"
    return redirect('/success')
@app.route('/success')
def success():
    query = ("SELECT email, DATE_FORMAT(created_at, '%c/%d/%y %l:%m %p') AS day FROM accounts")
    emails = mysql.query_db(query)
    print query
    return render_template('/success.html', all_emails = emails)
app.run(debug=True)
