import pandas as pd
import re
from datetime import datetime

wine_df = pd.read_csv("../data/raw/winemag-data-130k-v2.csv",index_col=0)

# extract year from title, year range from 1900 to 2020
def extract_year(text):
    #match = re.search(r'\d{4}', text) 
    match = re.search(r'\b(19[9][0-9]|20[0-2][0-9])\b', text) 
    if match:
        return int(match.group())
    else:
        return

wine_df['year'] = wine_df['title'].apply(extract_year)
wine_df.to_csv('../data/processed/wine.csv',index=False)