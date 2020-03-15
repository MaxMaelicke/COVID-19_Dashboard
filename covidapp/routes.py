from covidapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.load_data import load_figures, load_last_date

@app.route('/')
@app.route('/index')
def index():

    figures = load_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    # Get last date
    asof = load_last_date()

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                           asof=asof)
