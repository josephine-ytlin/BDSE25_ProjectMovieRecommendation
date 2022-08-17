import re
from flask import Flask, render_template, request
import csv
import pandas as pd

app = Flask(__name__)



# 電影資訊清單(dict型態)
results=[]
with open('lates_movie_html.csv',"r",encoding="utf8") as f:
    for line in csv.DictReader(f):
        results.append(line)
# model 頁面load load 進來的資料
models=[]
with open('model1.csv',encoding="utf8") as f:
    for modelppt in csv.DictReader(f):     
        models.append(modelppt)



# 首頁,一鍵成影
@app.route('/')
def index():    
     return render_template('index.html')

# 預測結果
@app.route('/home')
def home():    
    pictures = results[:30]
    return render_template('home.html',pictures=pictures[:10])
# 使用者 "你可能喜歡"的詳細頁面   
@app.route('/detail1')
def user1_detail1():
    pictures = results[:30]
    return render_template('user1_detail1.html', pictures=pictures)
# 使用者 "其他人也看...."的詳細頁面 
@app.route('/detail2')
def user1_detail2():
    pictures = results[:30]
    return render_template('user1_detail2.html', pictures=pictures)
# model 頁面
@app.route('/model')
def model():  
    modelppt=models
    return render_template('model.html',modelppt=modelppt)
# 簡介頁面
@app.route('/about')
def about():
    df = pd.read_csv('member.csv', encoding='UTF-8')
    member = [{key: df[key][value] for key in [key for key in df]} for value in range(len(df))]
    return render_template('about.html', member=member, len=len(member))

@app.route('/map')
def map1():  
   
    return render_template('map1.html')
# 讓flask app 跑起來    
if __name__=="__main__":
    app.run(debug=True)