import pandas as pd
import re
from datetime import datetime

# read the raw data
wine_df = pd.read_csv("../data/raw/winemag-data-130k-v2.csv",index_col=0)


def extract_year(text):
    """ extract year from title, year range from 1900 to 2020

    Parameters
    ----------
    text : text
        read in text 

    Returns
    -------
    year : int
        return year from 1900 to 2020 as a integer
    """    
    #match = re.search(r'\d{4}', text) 
    match = re.search(r'\b(19[9][0-9]|20[0-2][0-9])\b', text) 
    if match:
        return int(match.group())
    else:
        return

# add a new column 'year'
wine_df['year'] = wine_df['title'].apply(extract_year)

# save processed data
wine_df.to_csv('../data/processed/wine.csv',index=False)