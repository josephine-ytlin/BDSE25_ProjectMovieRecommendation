from json import load
from flask import Flask, render_template, request, url_for,session,redirect,flash
from flask_moment import Moment
from datetime import datetime
from pathlib import Path
from flask_mysqldb import MySQL
import uuid
import MySQLdb.cursors
# import sqlalchemy as db
import math
import csv
import re
import pandas as pd
import recognition.loadModel as ml

#  取得啟動文件資料夾路徑
# pjdir = os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
# db_url:mysql://b9bd2e193517eb:507cc1f5@us-cdbr-east-06.cleardb.net/heroku_e40c35af84b7fd2?reconnect=true
#    username:b9bd2e193517eb
#    password:507cc1f5
#    db_host:us-cdbr-east-06.cleardb.net
#    db_name:heroku_e40c35af84b7fd2



# MySQL local 環境建置
app.secret_key = 'ispanbdse25'
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_USER'] = 'b9bd2e193517eb'
app.config['MYSQL_PASSWORD'] = '507cc1f5'
app.config['MYSQL_DB'] = 'heroku_e40c35af84b7fd2'

# app.secret_key = 'ispanbdse25'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
# app.config['MYSQL_DB'] = 'testlogin'

# Intialize MySQL
mysql = MySQL(app)


# model 頁面load load 進來的資料
models=[]
with open('model1.csv',"r",encoding="utf-8") as f:
     for modelppt in csv.DictReader(f):     
         models.append(modelppt)
 


pictures=[]  
# 首頁 （含登入視窗）
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def index():    
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # msg = 'Logged in successfully!'
            # return 'Logged in successfully'
            return render_template('cluster_ch.html')           
        else:
            msg = 'Incorrect username / password !'
    return render_template('index.html', msg = msg)
#註冊視窗

@app.route('/register', methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'    
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email))
            mysql.connection.commit()
            # flash("成功註冊了!")
            msg = 'You have successfully registered!'
            # return redirect(url_for('index'), msg = msg)
    elif request.method == 'POST':
         msg = 'Please fill out the form !'
    # return render_template('index.html', msg = msg)
    return render_template('index.html', msg = msg)
# 預測結果
@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == "GET":
        global pictures,pictures2
        data,data2=ml.predict()
        pictures=data
        pictures2=data2   
    return render_template('home.html',pictures=pictures[:10],pictures2=pictures2[:10])
@app.route('/home1', methods=['GET','POST'])
def home1():
    if request.method == "POST":
        global pictures
        cluster = request.values.get("genre")
        pictures=ml.predict2(cluster)
    return render_template('home1.html',pictures=pictures[:10])
# 使用者 "你可能喜歡"的詳細頁面   
@app.route('/detail1')
def user1_detail1():
    pictures
    return render_template('user1_detail1.html',pictures=pictures[:30])
# 使用者 "其他人也看...."的詳細頁面 
@app.route('/detail2')
def user1_detail2():
    pictures2
    return render_template('user1_detail2.html',pictures2=pictures2[:30])
# model 頁面
@app.route('/model')
def model():  
    modelppt=models
    return render_template('model.html',modelppt=modelppt)
# 簡介頁面
@app.route('/about')
def about():
    df = pd.read_csv('member.csv', encoding='UTF-8')
    member = []
    for i in range(len(df)):
        member_dict = {}
        for j in df.columns:
            member_dict[j] = df[j][i]
        member.append(member_dict)
    return render_template('about.html', member=member, len=len(member))

# @app.route('/cluster', methods=['GET','POST'])
# def cluster():  
#     cluster=request.form["genre"]
#     print(type(cluster))
#     data3=ml.predict2(cluster)
#     pictures=data3
#     return render_template('home.html',pictures=pictures)

@app.route('/map')
def map1():  
   
    return render_template('map1.html')
# @app.route('//ProcessClusterinfo/<string:clusterinfo>',methods=['POST'])
# def ProcessClusterinfo(clusterinfo):
#     clusterinfo=json.loads(clusterinfo)
#     cluster=clusterinfo
#     print()
#     print(cluster)
#     print()
#     return ('/')


# 讓flask app 跑起來    
if __name__=="__main__":
    app.run(debug=True)