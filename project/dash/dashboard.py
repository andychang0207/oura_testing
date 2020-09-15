import dash
import dash_core_components as dcc
import dash_html_components as html

def init_dashboard(server):
    """製造一個plotly Dash dashboard. """
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/'
    )

    #製造 Dash layout
    dash_app.layout = html.Div(id='dash-container')

    return dash_app.server