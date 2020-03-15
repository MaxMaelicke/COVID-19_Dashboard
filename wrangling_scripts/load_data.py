import pickle

def load_figures():
    with open('data/figures.txt', 'rb') as figures_pickle:
        figures = pickle.load(figures_pickle)
    return figures

def load_last_date():
    with open('data/last_date.txt', 'rb') as date_pickle:
        last_date = pickle.load(date_pickle)
    return last_date
