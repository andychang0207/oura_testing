import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.express as px
from datetime import timedelta,datetime
import psycopg2
import pandas as pd
import json
from flask_login import current_user
from flask import session
with open("project/credentials/db_credentials.json") as db_file:
    data_base = json.load(db_file)
DB_HOST = data_base['DB_HOST']
DB_USER = data_base['DB_USER']
DB_PASS = data_base['DB_PASS']
DB_PORT = data_base['DB_PORT']
DB_NAME = data_base['DB_NAME']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def fetch_db(user_id):
    """目前還沒用到user_id"""
    con = psycopg2.connect(database=DB_NAME,user=DB_USER,host=DB_HOST,password=DB_PASS,port=DB_PORT)
    cur = con.cursor()
    cur.execute("""SELECT bedtime_start,bedtime_end,hr_5min,duration,summary_date FROM oura_sleep ORDER BY summary_date""")
    df = cur.fetchall()
    cur.close()
    con.close()
    data = []
    summary_date = []
    time_start = []
    time_end =[]
    duration = []
    time_step = []
    for row in df:
        l = []
        temp = row[2].replace('{','').replace('}','').split(',')
        for i in temp:
            l.append(int(i))
        data.append(l)
        time_start.append(row[0])
        time_end.append(row[1])
        duration.append(row[3])
        summary_date.append(row[4])
    j=0
    for row in duration:
        num = row//300
        tmp = [time_start[j] + timedelta(minutes=5*x) for x in range(0,num+1)]
        j = j + 1
        time_step.append(tmp)
    return time_start,time_step,data,summary_date

def init_dashboard(server):
    """製造一個plotly Dash dashboard. """
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=external_stylesheets
    )
    dash_app.index_string = """
    <link href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../static/style_user.css">
    <nav class="navbar navbar-inverse">
    <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <a class="navbar-brand" href="/">
                <img style="max-width:100px; margin-top: -10px;" alt="Loading" src="../static/icon/caticon.jpg" title = "omg-cat" width="40" height="40" >
            </a>
            <a class="navbar-brand" href="/" >
            Test-app
            </a>
        </div>
        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <form class="navbar-form navbar-right">
            <a class="btn btn-default" href="/logout" role="button">Log out</a>
            <a class="btn btn-default" href="/user_page" role="button">User Page</a>
            </form>
        </div><!-- /.navbar-collapse -->
    </div><!-- /.container-fluid -->
    </nav>
    <div id="intro" class="view">
    <div class="full-bg-img">
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
    </div>
    </div>
    """
    
    #製造 Dash layout  datetime.today().strftime("%Y-%m-%d")
    dash_app.layout = html.Div(
        children = [
            html.Div(
                dcc.DatePickerSingle(
                    id='date1',
                    date="2020-08-18"
                )
            ),
            html.Div(
                dcc.Graph(id='graph1',config={'displayModeBar':False})
            )
        ]
    )
    @dash_app.callback(
        Output('graph1','figure'),
        [Input('date1','date')])
    def update_graph(date):
        if current_user.is_authenticated:
            time_start,time_step,data,summary_date = fetch_db(current_user.user_id)
            dt = datetime.strptime(date,"%Y-%m-%d")
            if dt in summary_date:
                num = summary_date.index(dt)
                df = pd.DataFrame({
                    "time" : time_step[num],
                    "hr" : data[num]
                })
                fig = px.line(df,x='time',y='hr',range_y=[40,70])
                return fig
            else:
                df = pd.DataFrame({
                    "time" : [],
                    "hr" : []
                    })
                fig = px.line(df,x='time',y='hr',range_y=[40,70],template='plotly_dark')
                return fig
        else:
            return 'Please Login First !'
    return dash_app.server