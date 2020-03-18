from covidapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.load_data import load_figures, load_last_date            # Load figures etc. from pickles which are created every 4 hours (reduced server load)
#from wrangling_scripts.wrangle_data import return_figures, return_last_date    # Load and create figures etc. from raw data (higher server load)
import pandas as pd
import pickle

@app.route('/')
@app.route('/index')
def index():

    figures = load_figures()       # Load figure data from saved pickle
    #figures = return_figures()    # Load and create figures from raw data

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    # Get last date
    asof = load_last_date()       # Load last date from saved pickle
    #asof = return_last_date()    # Load and create last date from raw data

    # Get table
    table = pd.read_pickle('covidapp/data/df_cases_deaths.pkl')
    formatters = [lambda x: str(x),
            lambda x: '{:,}'.format(x).replace(',','.'),
            lambda x: '{:,}'.format(x).replace(',','.'),
            lambda x: str('{:,.2f}'.format(x) + ' %').replace(',','.'),
            lambda x: str('{:,.3f}'.format(x) + ' %').replace(',','.')
            ]
    table = table.to_html(classes = 'table table-striped', header = True, index = False, index_names = False, border = 0, justify = 'center', formatters = formatters)

    return render_template('index.html',
                           ids = ids,
                           figuresJSON = figuresJSON,
                           asof = asof,
                           table = table
                           )
