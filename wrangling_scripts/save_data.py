import pickle
from wrangle_data import return_figures, return_last_date

figures = return_figures()
last_date = return_last_date()

with open('covidapp/data/figures.txt', 'wb') as figures_pickle:
    pickle.dump(figures, figures_pickle)

with open('covidapp/data/last_date.txt', 'wb') as date_pickle:
    pickle.dump(last_date, date_pickle)
