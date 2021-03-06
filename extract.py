#!/usr/bin/python3
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from datetime import date


# In[3]:


def get_countries_table():
    url = "https://www.numbeo.com/cost-of-living/rankings_by_country.jsp"
    tables = pd.read_html(url)
    country_table = tables[1]
    del country_table['Rank']
    country_table.to_csv("countries.csv", index=False)
    return country_table


# In[5]:


countries_table = get_countries_table()


# In[6]:


countries_table


# In[7]:


def get_country_info(country):
    country=country.capitalize().replace(' ', '+')
    url = f"https://www.numbeo.com/cost-of-living/country_result.jsp?country={country}&displayCurrency=USD"
    tables = pd.read_html(url)
    country_info_table = tables[1]
    country_info_table.columns = ['Item', 'Price', 'Range']
    return country_info_table

def get_items():
    items = get_country_info("germany")
    return items['Item']


# In[9]:


country_list = countries_table['Country'].values
df = pd.DataFrame()
df['Item'] = get_items()
for country in country_list:
    df[country] = get_country_info(country)['Price']
    print("Scraping Country: "+ country)
df = df[df.Germany!='Edit']


# In[11]:


filename = f"cost_of_living_all-{date.today().strftime('%d-%m-%Y')}.csv"
df.to_csv(filename)


# In[ ]:




