#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 17:13:46 2022

@author: aashvinoodle
"""

"""
Created on Sun May  1 10:14:19 2022

@author: aashvinoodle
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import dash_table as dt

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Pandas dataframe to HTML table
def generate_table(dataframe, max_rows = 10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets = stylesheet)
server = app.server


books = pd.read_csv('/Users/aashvinoodle/Desktop/books.csv', encoding = 'latin-1')

range_dropdown_options = [{'label' : pagerange, 'value' : pagerange} for pagerange in sorted(list(set(books.Range)))]

genre_dropdown_options = [{'label' : genre, 'value' : genre} for genre in sorted(list(set(books.Genre)))]

fig = px.histogram(books, x = 'Genre', color = 'Genre', title = 'Number of Books in Each Genre') 

app.layout = html.Div([
    html.H1('Book Repository Dashboard',
            style = {'textAlign' : 'center', 'backgroundColor': 'lavenderblush', 'font-family' : 'Georgia',
                     'font-style': 'italic', 'color': 'midnightblue'}),
    html.H5('by Aashvi Talati', 
            style = {'textAlign' : 'center', 'font-family' : 'Georgia', 'font-style': 'italic', 'color': 'midnightblue'}),
    dcc.Graph(figure = fig, id = 'plot'),
    html.Div([html.H6('Page Range', 
                      style = {'textAlign' : 'left', 'font-family' : 'Georgia', 'color': 'midnightblue'}),
             dcc.Dropdown(options = range_dropdown_options, 
                          value = '<201', 
                          multi = False, id = 'bookrange')],
             style = {'width' : '50%', 'float' : 'left'}),
    
    
    html.Div([html.H6('Genre', style = {'textAlign' : 'left'}),
             dcc.Dropdown(options = genre_dropdown_options, 
                          value = ['Classics', 'Literary Fiction', 'Philosophy'], 
                          multi = True, id = 'bookgenre')],
             style = {'width' : '50%', 'float' : 'right', 'font-family' : 'Georgia', 'color': 'midnightblue'}),
    html.H1('____________________________________________________________________________________________________________',
            style = {'color': 'lightgrey'}),
    html.H6('Data Table', style = {'font-family' : 'Georgia', 'color': 'midnightblue'}),
    html.Div(dt.DataTable(books.to_dict('records'),id = 'booktable',
                 page_size = 10, css = [{"selector": ".Select-menu-outer",
                                         "rule": 'display : block'}],
                 style_data={'whiteSpace': 'normal','height': 'auto','lineHeight': '15px',
                             'backgroundColor': 'lavenderblush','color': 'black'})),
    html.H6('References', style = {'textAlign' : 'left', 'font-family' : 'Georgia', 'color': 'midnightblue'}),
    html.Div([
    html.A('Dataset', style = {'font-family' : 'Georgia'},
           href = 'https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata'),
    html.Br(),
    html.A('CSS Font Styling', style = {'font-family' : 'Georgia'},
           href = 'https://www.w3schools.com/css/css_font.asp'),
    html.Br(),
    html.A('Dashboard Help and References', style = {'font-family' : 'Georgia'},
           href = 'https://dash.plotly.com'),

    html.H6("May 2022, Aashvi Talati", style = {'textAlign' : 'left', 'font-family' : 'Georgia', 'color': 'midnightblue'})
    ])
    ])


@app.callback(
    Output('booktable', 'data'),
    Input('bookrange', 'value'),
    Input('bookgenre', 'value')
)

def update_table_(book_range, book_genre):
    table = books[(books.Range == book_range) & (books.Genre.isin(book_genre))]
    return table.to_dict('records')

@app.callback(
   Output('plot', 'figure'),
   Input('bookrange', 'value'),
   Input('bookgenre', 'value')
)

def update_plot(book__range, book__genre):
    updated_plot = books[(books.Range == book__range) & (books.Genre.isin(book__genre))]
    fig = px.histogram(updated_plot, x = 'Genre', color = 'Genre') 
    return fig


if __name__ == '__main__':
    app.run_server(debug = True)