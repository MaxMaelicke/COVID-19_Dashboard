## Script to match country population with covid data (via ISO-alpha-3 codes)

# Import the libraries
import pandas as pd
import pickle
from collections import defaultdict
from pycountry import countries

# Get the COVID data
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    
df_confirmed = pd.read_csv(url_confirmed, error_bad_lines=False)

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
            print(country, ' not found')
            no_pycountry.append(country)


'''
## Load the World Development Indicators by the World Bank and create data pickle for population data
# Comment: I created the pickle file only once to reduce server load

df_wdi = pd.read_csv('../covidapp/data/WDIData.csv')

# Extract the population data for 2018 (2019 has to many NaN values)
df_pop = df_wdi[df_wdi['Indicator Code'] == 'SP.POP.TOTL']

relevant_columns = ['Country Name', 'Country Code', '2018']
df_pop_2018 = df_pop[relevant_columns]

# Save population dataframe to pickle
df_pop_2018.to_pickle('../covidapp/data/df_pop_2018.pkl')
'''
