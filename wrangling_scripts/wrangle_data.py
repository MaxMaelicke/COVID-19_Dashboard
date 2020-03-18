# Import libraries
import pandas as pd
import plotly.graph_objs as go
from collections import Counter
from collections import defaultdict
import datetime
import numpy as np
from pycountry import countries
import pickle


def return_figures():
    ''' Fuction to create plotly visualizations
    Input:    None
    Output:   list (dict): list containing the plotly visualizations
    '''
    # Load Johns Hopkins University Data
    url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
    
    df_confirmed = pd.read_csv(url_confirmed, error_bad_lines=False)
    df_death = pd.read_csv(url_death, error_bad_lines=False)
    df_recovered = pd.read_csv(url_recovered, error_bad_lines=False)

    # Load population data from the World Bank
    df_pop_2018 = pd.read_pickle('covidapp/data/df_pop_2018.pkl')
    df_pop_2018 = df_pop_2018.drop(['Country Name'], axis = 1)
    
    #df_confirmed.to_pickle('data/covid-19_confirmed.pkl')
    #df_death.to_pickle('data/covid-19_death.pkl')
    #df_recovered.to_pickle('data/covid-19_recovered.pkl')
    
    last_col_confirmed = df_confirmed.columns[-1]

    cases = defaultdict(int)
    for i in range(len(df_confirmed)):
        cases[df_confirmed['Country/Region'][i]] += df_confirmed[last_col_confirmed][i]
    
    last_col_death = df_death.columns[-1]
    
    deaths = defaultdict(int)
    for i in range(len(df_death)):
        deaths[df_death['Country/Region'][i]] += df_death[last_col_death][i]
    
    
    '''
    # Gruppiertes Balkendiagramm
    graph_one = []
    x = []
    y = []
    for key, value in sorted(cases.items(), key=lambda item: item[1], reverse=True):
        x.append(key)
        y.append(value)
    
    z = []
    for key, value in sorted(deaths.items(), key=lambda item: item[1], reverse=True):
        z.append(value)

    x = x[0:15]
    y = y[0:15]
    z = z[0:15]


    graph_one.append(
            go.Bar(x = x,
                   y = y,
                   name = 'cases',)
            )
    graph_one.append(
            go.Bar(x = x,
                   y = z,
                   name = 'deaths',
                   marker_color = 'grey',)
            )

    layout_one = dict(title = 'Confirmed Cases | Top 15 Countries',
                      xaxis = dict(title = 'Country',),
                      yaxis = dict(title = 'Cases'),
                      barmode = 'group',
                      )
    '''

    # 1. Graph: Bar chart of confirmed cases per top country
    graph_one = []
    x = []
    y = []
    for key, value in sorted(cases.items(), key=lambda item: item[1], reverse=True):
        x.append(key)
        y.append(value)

    # Create dataframe for later
    df_country_cases = {'Country/Region': x, 'Cases': y}
    df_country_cases = pd.DataFrame(df_country_cases)

    x = x[0:15]
    y = y[0:15]
    
    graph_one.append(
            go.Bar(x = x,
                   y = y,)
            )
    
    layout_one = dict(title = 'Confirmed Cases | Top 15 Countries',
                      #xaxis = dict(title = 'Country',),
                      yaxis = dict(title = 'Cases'),
                      separators = ',.',
                      )


    # 2. Graph: Bar chart of deaths per top country
    graph_two = []
    x = []
    y = []
    for key, value in sorted(deaths.items(), key=lambda item: item[1], reverse=True):
        x.append(key)
        y.append(value)

    # Create dataframe for later
    df_country_deaths = {'Country/Region': x, 'Deaths': y}
    df_country_deaths = pd.DataFrame(df_country_deaths)

    x = x[0:15]
    y = y[0:15]
    
    graph_two.append(
            go.Bar(x = x,
                   y = y,
                   marker_color = 'grey',)
            )
    
    layout_two = dict(title = 'Fatal Cases | Top 15 Countries',
                      #xaxis = dict(title = 'Country',),
                      yaxis = dict(title = 'Deaths'),
                      separators = ',.',
                      )


    # 3. Graph: Line chart of new infections per day for top countries
    graph_three = []
    x = []
    y = []

    # Create DataFrame with new cases
    arr_confirmed = df_confirmed.iloc[:,4:].to_numpy()
    arr_confirmed_sub = np.append(arr = np.zeros((len(arr_confirmed), 1)).astype(int), values = arr_confirmed, axis = 1)
    arr_confirmed_sub = arr_confirmed_sub[:,:-1]
    
    arr_new = arr_confirmed - arr_confirmed_sub
    df_new_values = pd.DataFrame(arr_new)
    df_new_values.reset_index(inplace = True)

    df_new = df_confirmed.iloc[:,:4]
    df_new.reset_index(inplace = True)
    df_new = df_new.merge(df_new_values, on = 'index')
    df_new = df_new.iloc[:,1:]
    df_new.columns = df_confirmed.columns.tolist()

    # Create dictionary with new cases of the last 7 days
    countrylist = []
    new_last7 = defaultdict(int)
    for i in range(len(df_new)):
        new_last7[df_new['Country/Region'][i]] += df_new.iloc[:,-7:].sum(axis = 1)[i]
    
    # Create countrylist with top 15 countries
    countrylist = []
    for key, value in sorted(new_last7.items(), key=lambda item: item[1], reverse=True):
        countrylist.append(key)
    countrylist = countrylist[:12]

    datelist = df_new.columns[-28:].tolist()    # last 28 days

    # Create graph
    for country in countrylist:
        x = datelist
        y = []
        for date in datelist:
            y.append(df_new[date][df_new['Country/Region'] == country].sum())

        graph_three.append(
                go.Scatter(
                    x = x,
                    y = y,
                    mode = 'lines',
                    name = country)
                )

    layout_three = dict(title = 'Infections per Day <br>Top 12 Countries by most infections in last 7 days',
                xaxis = dict(#title = 'Date',
                    autotick=True),
                yaxis = dict(title = 'Cases'),
                separators = ',.',
                )


    # 4. Graph: Scatter confirmed cases vs. deaths
    graph_four = []
    
    # Create countrylist with top countries by total cases
    countrylist = []
    count = 0
    for key, value in sorted(cases.items(), key=lambda item: item[1], reverse=True):
        if count < 12:
            countrylist.append(key)
            count += 1
        else:
            break

    for country in countrylist:
        x = [deaths[country]]
        y = [cases[country]]
        #text = str(country) + ' ' + str(x) + '/' + str(y)
        graph_four.append(
                go.Scatter(
                    x = x,
                    y = y,
                    mode = 'markers',
                    #text = text,
                    name = country,
                    textposition = 'top center'
                    )
                )

    layout_four = dict(title = 'Confirmed Cases & Deaths <br>Top 12 Countries by total cases',
                xaxis = dict(title = 'Deaths'),
                yaxis = dict(title = 'Cases'),
                separators = ',.',
                )


    # 5. Graph: Bubble map with confirmed cases per country
    graph_five = []

    #cases_deaths = []
    for latitude in df_confirmed['Lat']:
        df_lat = df_confirmed[df_confirmed['Lat'] == latitude]
        df_death_lat = df_death[df_death['Lat'] == latitude]
        for longitude in df_lat['Long']:
            cases = df_lat[last_col_confirmed][df_lat['Long'] == longitude].sum()
            deaths = df_death[last_col_death][df_death['Long'] == longitude].sum() 
            country_name = str(df_lat['Country/Region'][df_lat['Long'] == longitude].unique().tolist()[0])
            #cases_deaths.append([country, cases, deaths])
            if cases > 0:
                if str(df_lat['Province/State'][df_lat['Long'] == longitude].unique().tolist()[0]) == 'nan':
                    bubble_text = (
                            country_name 
                            + '<br>Cases:  ' + str(cases)
                            + '<br>Deaths: ' + str(deaths)
                            )
                else:
                    bubble_text = (
                            country_name + ', '
                            + str(df_lat['Province/State'][df_lat['Long'] == longitude].unique().tolist()[0])
                            + '<br>Cases:  ' + str(cases)
                            + '<br>Deaths: ' + str(deaths)
                            )
                graph_five.append(
                        go.Scattergeo(
                            locationmode = 'country names', #USA-states',
                            lat = [latitude],
                            lon = [longitude],
                            text = bubble_text,
                            marker = dict(
                                size = cases/1000,
                                #color = ,
                                line_color = 'rgb(40, 40, 40)',
                                line_width = 0.5,
                                sizemode = 'area'
                                )
                            #, name = 
                            )
                        )
            else:
                break
    
    layout_five = dict(title = 'Confirmed Cases & Deaths | Bubble Map (all cases)',
                      showlegend = False,
                      geo = dict(
                          projection = dict(type = 'natural earth'),
                          showland = True,
                          landcolor = 'rgb(217, 217, 217)',
                          #showocean = True,
                          #oceancolor = 'rgb(204,229,255)',
                          showcountries = True
                          )
                      )


    # 6. Graph: Colored Map (Chroropleth Map) with Cases / Population
    # Create dataframe with population, cases and death columns

    # Match Country Names with Pycountry library
    no_pycountry = []
    matched_country_dict = defaultdict(str)

    manual_country_dict = {
            'Brunei' : 'BRN',
            'Congo (Brazzaville)' : 'COG',
            'Congo (Kinshasa)' : 'COD',
            "Cote d'Ivoire" : 'CIV',
            'Holy See' : 'VAT',
            'Iran' : 'IRN',
            'Korea, South' : 'KOR',
            'Kosovo' : 'UNK',
            'Reunion' : 'REU',
            'Russia' : 'RUS',
            'Taiwan*' : 'TWN',
            'The Bahamas' : 'BHS',
            'occupied Palestinian territory' : 'PSE'
            }


    for country in df_confirmed['Country/Region'].drop_duplicates().sort_values():
        try:
            matched_country_dict[country] = countries.lookup(country).alpha_3
        except:
            try:
                matched_country_dict[country] = manual_country_dict[country]
            except:
                #print(country, ' not found')
                no_pycountry.append(country)
    
    # Create Dataframe with cases, deaths and population
    df_cases_deaths = df_country_cases.copy()
    df_cases_deaths = df_cases_deaths.merge(df_country_deaths, on = 'Country/Region')
    df_cases_deaths['Country Code'] = df_cases_deaths['Country/Region'].apply(lambda x: matched_country_dict[x])
    df_cases_deaths = df_cases_deaths.merge(df_pop_2018, on = 'Country Code')
    df_cases_deaths.columns = ['Country/Region',  'Cases',  'Deaths', 'Country Code', 'Population']

    # Calculate ratios
    df_cases_deaths['Mortality Rate'] = df_cases_deaths['Deaths'] / df_cases_deaths['Cases'] * 100
    df_cases_deaths['Cases / Population'] = df_cases_deaths['Cases'] / df_cases_deaths['Population'] * 100

    # Drop unneeded columns & save to pickle
    df_cases_deaths.drop(['Country Code', 'Population'], axis = 1).to_pickle('covidapp/data/df_cases_deaths.pkl')


    # Append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures


def return_last_date():
    '''
    Returns the last date of the confirmed, death and recovered data respectively by comparing the title of the last column
    '''

    url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
    url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'

    df_confirmed = pd.read_csv(url_confirmed, error_bad_lines=False)
    df_death = pd.read_csv(url_death, error_bad_lines=False)
    df_recovered = pd.read_csv(url_recovered, error_bad_lines=False)

    date_cases = datetime.datetime.strptime(df_confirmed.columns[-1], '%m/%d/%y').date()
    date_recovered = datetime.datetime.strptime(df_recovered.columns[-1], '%m/%d/%y').date()
    date_deaths = datetime.datetime.strptime(df_death.columns[-1], '%m/%d/%y').date()

    last_date = max(date_cases, date_recovered, date_deaths)

    return last_date


def return_table():
    '''
    Returns a table in HTML format with ratios and figures per country.
    '''
    
    html_table = None

    return html_table
