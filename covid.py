from covidapp import app

'''
from flask import Flask
app = Flask(__name__)

#@app.route("/")
#def hello():
#    return "<h1 style='color:blue'>Hello There!</h1>"

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')

#from covidapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.wrangle_data import return_figures

@app.route('/')
@app.route('/index')
def index():

    figures = return_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')    
