import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here

data = pd.read_csv('https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv')
url = 'https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv'
states = pd.read_csv(url)

data['year'] = data['Timestamp'].apply(pl.extract_year_mdy)

data.to_csv('cache/survey_data.csv', index=False)
states.to_csv('cache/states.csv', index=False)

years = data['year'].unique()
for year in years:
    living_cost_year = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    living_cost_year = living_cost_year[1]
    living_cost_year['year'] = year
    living_cost_year.to_csv(f'cache/living_cost_{year}.csv', index=False)