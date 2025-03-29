import pandas as pd
import streamlit as st
import pandaslib as pl

survey_data = pd.read_csv('cache/survey_data.csv')
states_data = pd.read_csv('cache/states.csv')
cost_of_living_data = []
for year in survey_data['year'].unique():
    living_cost_year = pd.read_csv(f'cache/living_cost_{year}.csv')
    cost_of_living_data.append(living_cost_year)
cost_of_living_data = pd.concat(cost_of_living_data, ignore_index=True)
survey_data['country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)
survey_states_combined = survey_data.merge(states_data, left_on="If you're in the U.S., what state do you work in?", right_on='State', how='inner')

survey_states_combined['full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['country']

survey_states_combined.to_csv('cache/survey_states_combined.csv')

combined = survey_states_combined.merge(
    cost_of_living_data,
    left_on=['year', 'full_city'],
    right_on=['year', 'City'],
    how='inner'
)

combined['What is your annual salary?'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"]

combined['__annual_salary_cleaned'] = combined['What is your annual salary?'].apply(pl.clean_currency).astype(float)
combined['_annual_salary_adjusted'] = combined['__annual_salary_cleaned'] / combined['Cost of Living Index']

combined.to_csv('cache/survey_dataset.csv', index=False)

annual_salary_adjusted_by_location_and_age = combined.pivot_table(
    values='_annual_salary_adjusted',
    index='full_city',
    columns='How old are you?',
    aggfunc='mean'
)
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

annual_salary_adjusted_by_location_and_education = combined.pivot_table(
    values='_annual_salary_adjusted',
    index='full_city',
    columns='What is your highest level of education completed?',
    aggfunc='mean'
)
annual_salary_adjusted_by_location_and_education.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')