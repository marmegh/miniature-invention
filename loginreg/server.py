from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
import md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "CakeByTheOcean"
mysql = MySQLConnector(app,'wall')
@app.route('/')
def index():
    if session.get('testy') is None:
        session['fname'] = 'First Name'
        session['lname'] = 'Last Name'
        session['email'] = 'Email'
        session['testy'] = False
    return render_template('index.html', fname = session['fname'], lname = session['lname'], email = session['email'], test = session['testy'], login = session['login'])
@app.route('/register', methods=['POST'])
def registration():
    session['password'] = request.form['password']
    session['confirmpw'] = request.form['confirmpw']
    session['testy'] = True
    session['verify'] = True
    if len(request.form['fname']) < 1:
        session['fname'] = request.form['fname']
        session['verify'] = False
        flash('First Name required')
    else:
        session['fname'] = request.form['fname']
    if len(request.form['lname']) < 1:
        session['verify'] = False
        flash('Last Name required')
    else:
        session['lname'] = request.form['lname']
    if len(request.form['email']) < 1:
        session['verify'] = False
        flash('Email required')
    else:
        session['email'] = request.form['email']
    if len(request.form['password']) < 4:
        session['verify'] = False
        flash('Password too short')
    if request.form['password'] != request.form['confirmpw']:
        session['verify'] = False
        flash('Password and confirmation must match')
    query1 = ("SELECT email FROM users")
    something = mysql.query_db(query1)
    for x in range(0,len(something)):
        print something[x]['email']
        if request.form['email'] == something[x]['email']:
            flash('Account already exists')
            session['verify'] = False
        else:
            print 'valid email'
    hashed_password = md5.new(request.form['password']).hexdigest()
    data = {
             'first': request.form['fname'],
             'last': request.form['lname'],
             'email': request.form['email'],
             'password': hashed_password
           }
    query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(:first, :last,:email, :password, NOW(), NOW())"
    print query
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    query1 = ("SELECT email, password, first_name, id FROM users")
    something = mysql.query_db(query1)
    for x in range(0,len(something)):
        print something[x]['email']
        if request.form['email'] == something[x]['email']:
            pw = md5.new(request.form['password']).hexdigest()
            if pw == something[x]['password']:
                session['login'] = True
                session['id'] = something[x]['id']
                session['fname']=something[x]['first_name']
                session['testy']=True
                print something[x]['first_name']
                print session['id']
                print 'match detected'
                return redirect('/success')
            else:
                flash('invalid login credentials')
                return redirect('/')
    flash('invalid email')
    return redirect('/')
@app.route('/logout')
def logout():
    session['login'] = False
    del session['testy']
    return redirect('/')
@app.route('/success')
def success():
    return render_template('success.html')
app.run(debug=True)
