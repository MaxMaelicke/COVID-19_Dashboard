# Flask App providing interactive Dashboard about COVID-19 cases

This project inhabitates the code for the flask app providing a dashboard with graphs about corona virus (COVID-19) cases:
* Confirmed Cases per Country (bar chart)
* Deaths per Country (bar chart)
* New Infections per Day per Country (line chart)
* Confirmed Cases & Deaths (scatterplot)
* Bubble Map with Confirmed Cases and Deaths per Location

The live dashboard can be found here: https://covid.maelicke.net/ 

The data is provided by Johns Hopkins University and updated once a day. It is collected from several sources (which do not always agree).


## Prerequisites

Python 3

Flask

Plotly

Gunicorn

Webserver (e. g. NGINX)


## Getting Started

For Flask beginners I would recommend following a tutorial (e.g. https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)

Download or clone this repository.

For reduced server load: setup a cron job for python script "wrangling_data/save_figures.sh"
If server load does not matter: change "covidapp/routes.py" to use libraries from "wrangle_data.py" directly

Setup Gunicorn/WSGI sock (e.g. systemd service).

Setup webserver and link to app location. 


## Used libraries

* numpy
* pandas

* flask
* plotly

* collections
* datetime


## Author

* **Max Maelicke** - (https://github.com/MaxMaelicke)


## Acknowledgments

Many thanks to **Johns Hopkins University** for collecting the data and making it accessable on Github (https://github.com/CSSEGISandData/COVID-19).

