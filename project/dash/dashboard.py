import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.express as px
import plotly.graph_objs as go
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
def time_change(num):
    num = num//60
    minute = num % 60
    hour = num // 60
    return hour , minute
def time_change_min(num):
    hour = num // 60
    minute = num % 60
    return hour , minute
def fetch_db_sleep(summary,user_id):
    con = psycopg2.connect(database=DB_NAME,user=DB_USER,host=DB_HOST,password=DB_PASS,port=DB_PORT)
    cur = con.cursor()
    cur.execute("""SELECT bedtime_start,bedtime_end,hr_5min,duration,summary_date,hypnogram_5min,efficiency,score,total,hr_lowest,rem,awake,deep,light,onset_latency,hr_average,breath_average,rmssd,rmssd_5min,temperature_delta FROM oura_sleep WHERE user_id = %s ORDER BY summary_date """,(user_id,))
    df = cur.fetchall()
    cur.close()
    con.close()
    data = []
    temperature_delta = []
    breath_average = []
    hr_average = []
    summary_date = []
    time_start = []
    time_end =[]
    duration = []
    rem=[]
    awake=[]
    deep=[]
    light=[]
    total = []
    hr_low = []
    time_step = []
    hyp = []
    score = []
    latency = []
    rmssd = []
    rmssd_5min = []
    efficiency = []
    for row in df:
        l = []
        l2 = []
        l3 = []
        temp = row[2].replace('{','').replace('}','').split(',')
        temp2 = list(row[5])
        temp3 = row[18].replace('{','').replace('}','').split(',')
        for i in temp2:
            l2.append(int(i))
        for i in temp:
            l.append(int(i))
        for i in temp3:
            l3.append(int(i))
        data.append(l)
        time_start.append(row[0])
        time_end.append(row[1])
        duration.append(row[3])
        summary_date.append(row[4])
        hyp.append(l2)
        efficiency.append(row[6])
        score.append(row[7])
        total.append(row[8])
        hr_low.append(row[9])
        rem.append(row[10])
        awake.append(row[11])
        deep.append(row[12])
        light.append(row[13])
        latency.append(row[14])
        hr_average.append(row[15])
        breath_average.append(row[16])
        rmssd.append(row[17])
        rmssd_5min.append(l3)
        temperature_delta.append(row[19])
    j=0
    for row in duration:
        num = row//300
        tmp = [time_start[j] + timedelta(minutes=5*x) for x in range(0,num+1)]
        j = j + 1
        time_step.append(tmp)
    return time_start,time_step,data,summary_date,hyp,score,efficiency,total,hr_low,duration,rem,awake,deep,light,latency,hr_average,breath_average,rmssd,rmssd_5min,temperature_delta

def fetch_db_readiness(summary,user_id):
    con = psycopg2.connect(database=DB_NAME,user=DB_USER,host=DB_HOST,password=DB_PASS,port=DB_PORT)
    cur = con.cursor()
    cur.execute("""SELECT score,summary_date,score_previous_night,score_activity_balance,score_resting_hr,score_hrv_balance,score_previous_day,score_sleep_balance,score_recovery_index,score_temperature FROM oura_readiness WHERE user_id = %s ORDER BY summary_date """,(user_id,))
    df = cur.fetchall()
    cur.close()
    con.close()
    data = []
    summary_date = []
    score_previous_night = []
    score_activity_balance=[]
    score_resting_hr = []
    score_hrv_balance = []
    score_previous_day = []
    score_sleep_balance = []
    score_recovery_index = []
    score_temperature = []
    for row in df:
        data.append(row[0])
        summary_date.append(row[1])
        score_previous_night.append(row[2])
        score_activity_balance.append(row[3])
        score_resting_hr.append(row[4])
        score_hrv_balance.append(row[5])
        score_previous_day.append(row[6])
        score_sleep_balance.append(row[7])
        score_recovery_index.append(row[8])
        score_temperature.append(row[9])
    return data,summary_date,score_previous_night,score_activity_balance,score_resting_hr,score_hrv_balance,score_previous_day,score_sleep_balance,score_recovery_index,score_temperature

def fetch_db_activity(summary,user_id):
    con = psycopg2.connect(database=DB_NAME,user=DB_USER,host=DB_HOST,password=DB_PASS,port=DB_PORT)
    cur = con.cursor()
    cur.execute("""SELECT summary_date,day_start,day_end,score,score_stay_active,score_move_every_hour,score_meet_daily_targets,score_training_frequency,score_training_volume,score_recovery_time,daily_movement,non_wear,rest,inactive,inactivity_alerts,low,medium,high,steps,cal_total,cal_active,met_min_inactive,met_min_low,met_min_medium_plus,met_min_medium,met_min_high,average_met,class_5min,met_1min,target_calories,target_km,to_target_km,total FROM oura_activity WHERE user_id = %s ORDER BY summary_date """,(user_id,))
    df = cur.fetchall()
    cur.close()
    con.close()
    summary_date = []
    day_start = []
    day_end = []
    score = []
    score_stay_active = []
    score_move_every_hour = []
    score_meet_daily_targets = []
    score_training_frequency = []
    score_training_volume = []
    score_recovery_time = []
    daily_movement = []
    non_wear = []
    rest = []
    inactive = [] 
    inactivity_alerts = []
    low = []
    medium = []
    high = []
    steps = []
    cal_total = []
    cal_active = []
    met_min_inactive = []
    met_min_low = []
    met_min_medium_plus = []
    met_min_medium = []
    met_min_high = []
    average_met = []
    class_5min = []
    met_1min = []
    target_calories = []
    target_km = []
    to_target_km = []
    total = []
    for row in df:
        l = []
        l2 = []
        tmp = row[28].replace('{','').replace('}','').split(',')
        tmp2 = list(row[27])
        for i in tmp:
            l.append(float(i))
        for i in tmp2:
            l2.append(int(i))
        summary_date.append(row[0])
        day_start.append(row[1])
        day_end.append(row[2])
        score.append(row[3])
        score_stay_active.append(row[4])
        score_move_every_hour.append(row[5])
        score_meet_daily_targets.append(row[6])
        score_training_frequency.append(row[7])
        score_training_volume.append(row[8])
        score_recovery_time.append(row[9])
        daily_movement.append(row[10])
        non_wear.append(row[11])
        rest.append(row[12])
        inactive.append(row[13])
        inactivity_alerts.append(row[14])
        low.append(row[15])
        medium.append(row[16])
        high.append(row[17])
        steps.append(row[18])
        cal_total.append(row[19])
        cal_active.append(row[20])
        met_min_inactive.append(row[21])
        met_min_low.append(row[22])
        met_min_medium_plus.append(row[23])#空的
        met_min_medium.append(row[24])
        met_min_high.append(row[25])
        average_met.append(row[26])
        target_calories.append(row[29])
        target_km.append(row[30])
        to_target_km.append(row[31])
        total.append(row[32])
        class_5min.append(l2)
        met_1min.append(l)
    return summary_date,day_start,day_end,score,score_stay_active,score_move_every_hour,score_meet_daily_targets,score_training_frequency,score_training_volume,score_recovery_time,daily_movement,non_wear,rest,inactive,inactivity_alerts,low,medium,high,steps,cal_total,cal_active,met_min_inactive,met_min_low,met_min_medium_plus,met_min_medium,met_min_high,average_met,class_5min,met_1min,target_calories,target_km,to_target_km,total



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
    <link rel="stylesheet" href="../static/style_dash.css">
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
                className='drop-container',
                children=[   
                    dcc.Dropdown(
                        id='drop1',
                        options=[
                            {'label': 'Sleep', 'value': 'oura_sleep'},
                            {'label': 'Readiness', 'value': 'oura_readiness'},
                            {'label': 'Activity', 'value': 'oura_activity'}
                        ],
                        value='oura_sleep',
                        style={'float':'left','width':'15vw'}
                    ),
                    dcc.DatePickerSingle(
                        id='date1',
                        date=datetime.today().strftime("%Y-%m-%d"),
                        style={'background-color':'#1f2630','margin-left':'20px'}
                    ),
                ]
            ),
            html.Div(
                className='graph-container',
                children=[
                    html.Div(id='out'),
                ]
            )
        ]
    )
    @dash_app.callback(
        Output('out','children'),
        [Input('drop1','value'),Input('date1','date')])
    def update_graph(select,date):
        if current_user.is_authenticated:
            dt = datetime.strptime(date,"%Y-%m-%d")
            
            if select == 'oura_sleep':
                
                time_start,time_step,data,summary_date,hyp,score,eff,total,hr_low,duration,rem,awake,deep,light,latency,hr_average,breath_average,rmssd,rmssd_5min,temperature_delta = fetch_db_sleep(select,current_user.user_id)
                if dt - timedelta(days=1)  in summary_date:
                    num = summary_date.index(dt- timedelta(days=1))
                    fig_data_hr = go.Scatter(
                        y = data[num],
                        x = time_step[num],
                        name = 'Scatter',
                        mode = 'lines+markers'
                    )
                    hr_g = dcc.Graph(id='graph1',config={'displayModeBar':False},style={'width':'35vw','height':'20vw','margin':'10px'},figure={
                        'data':[fig_data_hr],
                        'layout':go.Layout(yaxis = dict(range=[40,70]),title = 'Resting heart rate',paper_bgcolor="#1f2630",plot_bgcolor="#1f2630",font=dict(color="#2cfec1"))
                    })
                    fig_data_hyp = go.Scatter(
                        y = hyp[num],
                        x = time_step[num],
                        name = 'Scatter',
                        mode = 'lines+markers'
                    )
                    hyp_g = dcc.Graph(id='graph2',config={'displayModeBar':False},style={'width':'35vw','height':'20vw','margin':'10px'},figure={
                        'data':[fig_data_hyp],
                        'layout':go.Layout(yaxis = dict(range=[1,4],tickvals=[1,2,3,4],ticktext=['deep','light','rem','awake']),title = 'Sleep stages',paper_bgcolor="#1f2630",plot_bgcolor="#1f2630",font=dict(color="#2cfec1"))
                    })
                    fig_data_rmssd = go.Scatter(
                        y = rmssd_5min[num],
                        x = time_step[num],
                        name='Scatter',
                        mode='lines+markers'
                    )
                    rmssd_g = dcc.Graph(id='graph3',config={'displayModeBar':False},style={'width':'35vw','height':'20vw','margin':'10px'},figure={
                        'data':[fig_data_rmssd],
                        'layout':go.Layout(yaxis = dict(range=[0,300]),title = 'Heart Rate Variability',paper_bgcolor="#1f2630",plot_bgcolor="#1f2630",font=dict(color="#2cfec1"))
                    })
                    dura_hr , dura_min = time_change(duration[num])
                    slp_hr , slp_min = time_change(total[num])
                    labels = ['deep','light','rem','awake',]
                    values = [deep[num],light[num],rem[num],awake[num]]
                    lat = latency[num]//60

                    return html.Div(
                        className='graph_output',
                        children=[
                            html.Div(
                                className='leftcol',
                                children=[
                                    html.Div(
                                        [html.H1(str(score[num])), html.P("Score")],
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H1(str(eff[num])+'%'), html.P("Efficiency")],
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H1(str(dura_hr)+'h'+str(dura_min)+'m'), html.P("Time in bed")],
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H1(str(slp_hr)+'h'+str(slp_min)+'m'), html.P("Total sleep time")],
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H1(str(lat)+'m'), html.P("Latency")],
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H1(str(breath_average[num])+' / min'), html.P("Respiratory rate")],
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H1(str(temperature_delta[num])+' '+'\u2103'), html.P("Body temperature deviation")],
                                        className="mini_container",
                                    ),
                                    
                                ]
                            ),
                            html.Div(
                                className='hr_g',
                                children = [
                                    hr_g,
                                    html.Div(
                                        [html.H1(str(hr_average[num])+' bpm'), html.P("average")],
                                        className="mini_container_g",
                                    ),
                                    html.Div(
                                        [html.H1(str(hr_low[num])+' bpm'), html.P("lowest")],
                                        className="mini_container_g",
                                    ),
                                ]
                            ),
                            html.Div(
                                className='hyp_g',
                                children=[
                                    hyp_g,
                                    dcc.Graph(
                                        style={'width':'35vw','height':'20vw','margin':'10px'},
                                        figure={
                                            'data':[go.Pie(labels=labels, values=values,marker={'colors': ['#aecaf5','#fff','#063a8a','#516f9c']},hole=.3)],
                                            'layout':go.Layout(paper_bgcolor="#1f2630",font=dict(color="#fff")),
                                            })
                            ]),
                            html.Div(
                                className='rmssd_g',
                                children=[
                                    rmssd_g,
                                    html.Div(
                                        [html.H1(str(rmssd[num])+' ms'), html.P("average")],
                                        className="mini_container_g",
                                    ),
                                    html.Div(
                                        [html.H1(str(max(rmssd_5min[num]))+' ms'), html.P("max")],
                                        className="mini_container_g",
                                    ),
                                ]
                            )
                        ])
            
                else:
                    return
            elif select == 'oura_readiness':
                data,summary_date,score_previous_night,score_activity_balance,score_resting_hr,score_hrv_balance,score_previous_day,score_sleep_balance,score_recovery_index,score_temperature = fetch_db_readiness(select,current_user.user_id)
                if dt - timedelta(days=1) in summary_date:
                    num = summary_date.index(dt- timedelta(days=1))
                    return html.Div(
                        className='graph_container',
                        children=[
                            html.Div(
                                [html.H1(str(data[num])), html.P("Readiness")],
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H1(str(score_previous_night[num])), html.P("Score previous night")],
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H1(str(score_activity_balance[num])), html.P("Score activity balance")],
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H1(str(score_resting_hr[num])), html.P("Score resting hr")],
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H1(str(score_hrv_balance[num])), html.P("Score hrv balance")],
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H1(str(score_previous_day[num])), html.P("Score previous day")],
                                className="mini_container",
                            ),
                            html.Div(
                                [html.H1(str(score_sleep_balance[num])), html.P("Score sleep balance")],
                                className="mini_container",
                            ),
                             html.Div(
                                [html.H1(str(score_recovery_index[num])), html.P("Score recovery index")],
                                className="mini_container",
                            ),
                             html.Div(
                                [html.H1(str(score_temperature[num])), html.P("Score temperature")],
                                className="mini_container",
                            ),
                        ]
                    )
            elif select == 'oura_activity':
                summary_date,day_start,day_end,score,score_stay_active,score_move_every_hour,score_meet_daily_targets,score_training_frequency,score_training_volume,score_recovery_time,daily_movement,non_wear,rest,inactive,inactivity_alerts,low,medium,high,steps,cal_total,cal_active,met_min_inactive,met_min_low,met_min_medium_plus,met_min_medium,met_min_high,average_met,class_5min,met_1min,target_calories,target_km,to_target_km,total = fetch_db_activity(select,current_user.user_id)
                if dt in summary_date:
                    num = summary_date.index(dt)
                    inactive_hr,inactive_min = time_change_min(inactive[num])
                    time_step = [day_start[num]+timedelta(minutes=i) for i in range(0,len(met_1min[num]))]
                    fig_data_met = go.Bar(
                        x = time_step,
                        y = met_1min[num]
                    )
                    met_g = dcc.Graph(id='graph_met',config={'displayModeBar':False},style={'width':'35vw','height':'20vw','margin':'10px'},figure={
                        'data':[fig_data_met],
                        'layout':go.Layout(yaxis = dict(tickvals=[1.05,2,3,7],ticktext=['inactive','low','medium','high'],gridcolor='#5b5b5b'),title = 'Daily Movement',paper_bgcolor="#1f2630",plot_bgcolor="#1f2630",font=dict(color="#2cfec1"))
                    })
                    return html.Div(
                                className='graph_output',
                                children=[
                                    html.Div(
                                        className='leftcol',
                                        children=[
                                            html.Div(
                                                [html.H1(str(score[num])), html.P("Score")],
                                                className="mini_container",
                                            ),
                                            html.Div(
                                                [html.H1(str(cal_active[num])+' / '+str(target_calories[num])+' Cal'), html.P("Goal Progress")],
                                                className="mini_container",
                                            ),
                                            html.Div(
                                                [html.H1(str(cal_total[num])+' Cal'), html.P("Total Burn")],
                                                className="mini_container",
                                            ),
                                            html.Div(
                                                [html.H1(str(steps[num])), html.P("Steps")],
                                                className="mini_container",
                                            ),
                                            html.Div(
                                                [html.H1(str(inactive_hr)+'h'+str(inactive_min)+'m'), html.P("Inactive")],
                                                className="mini_container",
                                            ),
                                            
                                        ]
                                    ),
                                    html.Div(
                                        className='met_g',
                                        children = [
                                            met_g
                                        ]
                                    ),
                                    html.Div(
                                        className='hyp_g',
                                        children=[
                                            
                                    ]),
                                    html.Div(
                                        className='rmssd_g',
                                        children=[
                                            
                                        ]
                                    )
                                ])
            else:
                return
        else:
            return 'Please Login First !'
    return dash_app.server