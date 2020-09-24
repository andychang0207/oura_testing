from flask import request,redirect,session,url_for,render_template
from flask import current_app as app
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json
import psycopg2
import pandas as pd
from urllib.parse import urlparse,urlencode
import requests
import os
from requests_oauthlib import OAuth2Session
import ast
from datetime import datetime,timedelta
from project.Register import LoginForm,RegisterForm
from project.model import User
from project.token_saver import token_saver
from project.update_to_db import to_db
from . import login,db


with open('project/credentials/db_credentials.json') as db_file:
    data_base = json.load(db_file)
DB_HOST = data_base['DB_HOST']
DB_USER = data_base['DB_USER']
DB_PASS = data_base['DB_PASS']
DB_PORT = data_base['DB_PORT']
DB_NAME = data_base['DB_NAME']

with open('project/credentials/oura_app_credentials.json') as json_file:
    credentials = json.load(json_file)


def update_db(data_name,df,user_id):
    con = psycopg2.connect(database = DB_NAME,host = DB_HOST,user = DB_USER,password = DB_PASS,port = DB_PORT)
    cur = con.cursor()
    df['user_id']=user_id
    output = StringIO()
    df.to_csv(output,sep='\t',index=False,header=False)
    output1 = output.getvalue()
    col = tuple(df.columns.values.tolist())
    cur.copy_from(StringIO(output1),"oura_" + data_name,columns = col,null="")
    con.commit()
    cur.close()
    con.close()
    return True

#app端ID
CLIENT_ID = credentials['CLIENT_ID']
#app端Secretkey
CLIENT_SECRET = credentials['CLIENT_SECRET']
#認證網址
AUTH_URL = 'https://cloud.ouraring.com/oauth/authorize'
#獲取token網址
TOKEN_URL = 'https://api.ouraring.com/oauth/token'
#獲取從何時開始的資料
START_DATE = "?start=2020-07-10"
#儲存路徑
OUTPUT_PATH = 'static/output/'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#起始畫面
@app.route("/")
def home():
    """Welcome page of the oura ring.
    """
    return render_template('index.html')
@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        session['username'] = current_user.username
        redirect(url_for('user_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user_object = User.query.filter_by(username=form.username.data).first()
        login_user(user_object)
        return redirect(url_for('user_page'))
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('user_info',None)
    session.pop('oauth',None)
    session.pop('username',None)
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup',methods=["POST","GET"])
def sign():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('signup.html',form = form)
@app.route('/user_page')
@login_required
def user_page():
    form = {
        'age':'NULL',
        'weight':'NULL',
        'height':'NULL',
        'email':'NULL',
        'user_id':'NULL',
        'gender':'NULL'
    }
    if current_user.user_id:
        token = {
            'refresh_token' : current_user.refresh_token,
            'token_type':'bearer',
            'access_token':current_user.access_token,
            'expires_in':current_user.expires_in
        }
        extra = {
            'client_id':CLIENT_ID,
            'client_secret':CLIENT_SECRET,
        }
        summaries = ['sleep','activity','readiness']
        con = psycopg2.connect(database = DB_NAME,host = DB_HOST,user = DB_USER,password = DB_PASS,port = DB_PORT)
        cur = con.cursor()
        cur.execute('''SELECT last_visit FROM oura_user_profile
        WHERE user_id = %s''',(current_user.user_id,))
        rows = cur.fetchall()
        cur.close()
        con.close()
        flag = True
        for summary in summaries:
            if rows[0][0] is None:
                url = 'https://api.ouraring.com/v1/' + summary
            else:
                START_DATE = rows[0][0].strftime("%Y-%m-%d")
                url = 'https://api.ouraring.com/v1/'+ summary +'?start=' + START_DATE
            client = OAuth2Session(CLIENT_ID,token=token)
            result = client.get(url)
            try:
                df = result.json()[summary]
                #df.to_csv('static/output/'+summary+'4.csv')
                flag = flag and to_db(summary,df,current_user.user_id)
            except:
                token = client.refresh_token(TOKEN_URL,**extra)
                print(token)
                token_saver(token)
                client = OAuth2Session(CLIENT_ID,token=token)
                result = client.get(url)
                df = result.json()[summary]
                flag = flag and to_db(summary,df,current_user.user_id)
        VISIT_DATE = datetime.strftime(datetime.now()-timedelta(days=2),"%Y/%m/%d")
        con = psycopg2.connect(database = DB_NAME,host = DB_HOST,user = DB_USER,password = DB_PASS,port = DB_PORT)
        cur = con.cursor()
        cur.execute('''UPDATE oura_user_profile
                SET last_visit = %s
                WHERE user_id = %s''',(VISIT_DATE,current_user.user_id))
        con.commit()
        cur.close()
        con.close()
        client = OAuth2Session(CLIENT_ID,token=token)
        result = client.get('https://api.ouraring.com/v1/userinfo')
        try:
            test = result.json()['age']
            print('age is',test)
        except:
            token = client.refresh_token(TOKEN_URL,**extra)
            print(token)
            token_saver(token)
            client = OAuth2Session(CLIENT_ID,token=token)
            result = client.get('https://api.ouraring.com/v1/userinfo')
        form = result.json()
    return render_template('user_page.html',**form)



#重新導向至oura的授權畫面 user所輸入的密碼操作都在oura server端 app端看不到
@app.route("/oura_login",methods=['POST','GET'])
@login_required
def oura_login():
    """Redirect to the OAuth provider login page.
    """
    #只給client id 因為scope=None 表示全部資訊都要
    oura_session = OAuth2Session(CLIENT_ID)

    #將 client id 、default auth url 、state 拼出我們的 authorization url 
    #其中此 authorization url 有我們的訊息
    authorization_url , state = oura_session.authorization_url(AUTH_URL)

    #---------------第一種打法-----------------------------#
    #將隨機創出的 state 放進物件session中 (session以cookie實踐)
    #session['oauth_state'] = state
    #----------------------------------------------------#

    #重新導向至authorization server端 (oura server)
    return redirect(authorization_url)

#從授權端重新導向回來 (申請 client id 時填的 callback url)
@app.route("/callback")
def callback():
    """Retrieve access_token from Oura response URL. Redirect to profile page.
    """
    
    #------------------------第一種打法(利用session cookie 傳遞訊息)--------------#
    #if else 是為了檢查 session (cookie實作) 的 oauth_session 有沒有東西
    #若沒有則再回去 /oura_login 重跑一次
    #若host name改成 localhost 就不會有這個問題
    #在此def也需要一個Oauth2session物件 並需放入state 
    #利用 fetch_token function 到 token 的 url 取得 token
    #需要 client secret 、 authorization response (我們的url) 來換取 token

    #if 'oauth_state' in session:
        #oura_session = OAuth2Session(CLIENT_ID,state = session['oauth_state'])
        #session['oauth'] = oura_session.fetch_token(TOKEN_URL,
        #client_secret=CLIENT_SECRET,
        #authorization_url = request.url)
        #return redirect(url_for('.profile'))
    #else:
        #return redirect(url_for('.oura_login'))
    #----------------------------------------------------------------------------#


    #--------------------第二種打法(從 url 中傳遞訊息)-----------------------------#    
    #利用 python 的 urlparse 分解 request.url 從中獲得 code 及 state
    temp_list = urlparse(request.url).query.replace("=","&").split("&")
    temp_dict = {temp_list[0]:temp_list[1],temp_list[2]:temp_list[3],temp_list[4]:temp_list[5]}
    if temp_list[0] == "error":
        return """<h2>You have denied authorization. Please go back to home page.</h2>
                    <a href="/">home</a>"""
    oura_session = OAuth2Session(CLIENT_ID,state = temp_dict['state'])

    #利用 code (authorization code) 和 client secret 向 authorization server 要求 token
    #而且此 session 有 我們之前授權時傳出的 state 以增加安全性 
    #將 token 存到 session 中
    session['oauth'] = oura_session.fetch_token(TOKEN_URL,
        client_secret=CLIENT_SECRET,
        code = temp_dict['code'])

    #重新導向至 /profile
    return redirect(url_for('first'))
    
    
@app.route('/first')
@login_required
def first():
    access_token = session['oauth']['access_token']
    token_type = session['oauth']['token_type']
    expires_in = session['oauth']['expires_in']
    refresh_token = session['oauth']['refresh_token']
    result = requests.get('https://api.ouraring.com/v1/userinfo?access_token=' + access_token)
    user_profile = result.json()
    session['user_info'] = user_profile
    user = db.session.query(User).filter_by(username=current_user.username).first()
    user.access_token = access_token
    user.token_type = token_type
    user.expires_in = expires_in
    user.refresh_token = refresh_token
    user.user_id = session['user_info']['user_id']
    db.session.commit()
    buffer = StringIO()
    df_user = pd.DataFrame(user_profile,index=[0])
    df_user.to_csv(buffer,sep = '\t',index=False,header=False)
    data = buffer.getvalue()
    try:
        con = psycopg2.connect(database = DB_NAME,host = DB_HOST,user = DB_USER,password = DB_PASS,port = DB_PORT)
        cur = con.cursor()
    except:
        print("can't connect to database.")
    cur.execute('''SELECT user_id FROM oura_user_profile
    WHERE user_id = %s''',(df_user.loc[0,'user_id'],))
    x = cur.fetchall()
    if not x: 
        cur.copy_from(StringIO(data),' "oura_user_profile" ',columns =('age','weight','height','gender','email','user_id')  )
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('user_page'))

#個人檔案介面
@app.route("/profile")
@login_required
def profile():
    """User profile.
    """
    #用取得的 token 換取 resource (user informations)
    oauth_token = session['oauth']['access_token']
    result = requests.get('https://api.ouraring.com/v1/userinfo?access_token=' + oauth_token)
    user_profile = result.json()
    buffer = StringIO()
    df_user = pd.DataFrame(user_profile,index=[0])
    session['user_info'] = user_profile
    df_user.to_csv(buffer,sep = '\t',index=False,header=False)
    data = buffer.getvalue()
    try:
        con = psycopg2.connect(database = DB_NAME,host = DB_HOST,user = DB_USER,password = DB_PASS,port = DB_PORT)
        cur = con.cursor()
    except:
        print("can't connect to database.")
    cur.execute('''SELECT user_id FROM oura_user_profile
    WHERE user_id = %s''',(df_user.loc[0,'user_id'],))
    x = cur.fetchall()
    if not x: 
        cur.copy_from(StringIO(data),' "oura_user_profile" ',columns =('age','weight','height','gender','email','user_id')  )
    con.commit()
    cur.close()
    con.close()
    
    
    test = ast.literal_eval(str(user_profile))
    return render_template("profile_page.html" ,**test)
