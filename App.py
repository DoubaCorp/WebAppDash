"""Importing the required libraries"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

# import plotly.offline as pyo
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

"""Building the functions required to scrape the website"""

# ---------------------------------------------------------------------------
from Imdb import df

data= df.copy()


"""Building the plotting functions"""

# ---------------------------------------------------------------------------
def top_rated_movies(data, num_movies=10):
    top_rated_movies = data.sort_values('rating', ascending=False).head(num_movies)

    fig = go.Figure(data=go.Bar(x=top_rated_movies['rating'], y=top_rated_movies['name'], orientation='h',
                               marker=dict(color='lightblue')))

    fig.update_layout(title='Top ten films in terms of ratings',
                      xaxis_title='Rating', yaxis_title='Movies', title_x=0.5, 
                      yaxis=dict(title='Movies', titlefont=dict(family='Arial', size=14)))

    return fig

def year_histogram(data):
    fig = go.Figure(data=go.Histogram(x=data['year'], marker=dict(color='tomato')))

    fig.update_layout(title='Histogram of film release years', title_x=0.5,
                      xaxis_title='Years', yaxis_title='Number of films')

    return fig

def top_voted_movies(data, num_movies=5):
        top_movies = data.sort_values(['votes', 'rating'], ascending=False).head(num_movies)


        labels = top_movies['name']
        values_votes = top_movies['votes']
        values_rating = top_movies['rating']

        fig = go.Figure()
        fig.add_trace(go.Funnel(
            name='Votes',
            y=labels,
            x=values_votes,
            textinfo="value+percent initial",
            textposition="inside",
            marker=dict(color='lightsalmon')
        ))
        fig.add_trace(go.Funnel(
            name='Rating',
            y=labels,
            x=values_rating,
            textinfo="value+percent previous",
            textposition="outside",
            marker=dict(color='mediumslateblue')
        ))

        fig.update_layout(title='Top 5 Movies: In term of Votes and Ratings',
                        title_x=0.5)

        return fig



def init_figure():
    "This function initiate all the needed figure to start the app."
    return top_rated_movies(data),year_histogram(data),top_voted_movies(data)



"""Initiale Figures"""
# ---------------------------------------------------------------------------



init_bar_fig,init_hist_fig, init_fun_fig = init_figure()



"""Building the app"""
# ---------------------------------------------------------------------------

# Initializing the app
app = dash.Dash(__name__)
server = app.server

# Building the app layout
app.layout = html.Div([
    
    html.H1("Imdb DashBoard", style={"text-align": "center"}),
    html.Br(),

    html.Div([
    dcc.Graph(id="graph_grp",figure=init_fun_fig)
    ]),
    
    html.Div([
     dcc.Graph(id ="graph",figure=init_bar_fig)
    ]),

    html.Div([
    dcc.Graph(id="graph_hist",figure=init_hist_fig)
    ])

  
])




# Defining the application callbacks

@app.callback(
    Output("graph", "figure"),
)
def update_bar_plot(value):
    return top_rated_movies(data, keyword=value)

@app.callback(
    Output("graph_hist", "figure"),
)
def update_hist_plot(value):
    return year_histogram(data, keyword=value)

@app.callback(
    Output("graph_grp", "figure"),
)
def update_grp_plot(value):
    return top_voted_movies(data, keyword=value)

if __name__ == "__main__":
    app.run_server()
