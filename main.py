# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 19:46:47 2021

@author: Adam
"""

## Alternative:

#####################################Documentation####################################

##https://newsapi.org/docs
##ref: https://github.com/mattlisiv/newsapi-python/blob/master/README.md

#####################################Documentation############################

# API imports:

from newsapi import NewsApiClient
import TwitterRetrieval
from TwitterRetrieval import TwitterApi


# Data Processing and cleaning:

import re
import pandas as pd
from pandas import DataFrame
import numpy as np

# Visualization:

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as md

# Text processing:

from textblob import TextBlob

# env vars

from Keys import environment_vars



site = input('Which stonk would you like to get info about?')
t = TwitterApi(q=site)
t.apiParser()

twitter_out = {"Word": t.userRetriever(),
 "Score": [TextBlob(i).sentiment.polarity for i in t.userRetriever()]}

print("Output: ")
print(TwitterRetrieval.sentiment(site, 200, np.mean(twitter_out["Score"])))


""""
News API Section
"""

## TO FIX: Exception handling
## exception handling for date start

# try:

date_start = input('When would you like to start the search?(yyyy-mm-dd) ')
check = re.findall('2021-[0-9]{2}-[0-9]{2}', date_start)   # regex to check correct input

#     if len(check) != 0:
#         check = True
#     else:
#         raise Exception('Please enter a date in the correct format')
# except Exception as err:
#     print(err)

## Exception handling for date end
# try:
print(" \n Thorough Exception handling planned for the next version \n")
date_end = input('When would you like to end the search?(yyyy-mm-dd) ')
check = re.findall('2021-[0-9]{2}-[0-9]{2}', date_end)   # regex to check correct input

#     if len(check) != 0:
#         check = True
#     else:
#         raise Exception('Please enter a date in the correct format')
# except Exception as err:
#     print(err)

## Part II: we send the user input and get a response

newsapi = NewsApiClient(api_key=environment_vars("keys.env")["NEWS"])  # API auth key (env var to be used!!!)

# if check == True: # Exception handling is broken, to be fixed later

all_articles = newsapi.get_everything(q=site,
                                      from_param=date_start,
                                      to=date_end,
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)  # we trigger the request if input tests are passed
print(all_articles)  # print all
all_articles = DataFrame(all_articles["articles"])  #we make a dataframe out of it

## Part III: data cleaning + Text Blob

headlines = []


# sentiment analysis:

sentiment_description = all_articles["description"].apply(lambda x: TextBlob(x).sentiment.polarity)
sentiment_title = all_articles["title"].apply(lambda x: TextBlob(x).sentiment.polarity)

sentiment = (sentiment_title + sentiment_description)*0.5  # Naive averaging method


label = []
for score in sentiment:  # for loop labeling each of the items with a sentiment
    if score < 0:
        label.append('negative')
    elif score >= 0 and score <= 0.4:
        label.append('neutral')
    else:
        label.append('overwhelmingly positive')

final_df = DataFrame(
    {
        "sentiment" : sentiment,
        "label" : label,
        "date" : all_articles["publishedAt"]
    }
)

print(final_df)


"""
Plotting 
"""
fig, ax = plt.subplots(figsize = (20, 10))
sns.set_style("whitegrid")

sns.lineplot(x="date", y="sentiment", data=final_df, ci=None)
plt.title(f'Polarization report for {site}')

ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday = 1))  # per week
ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90) # rotate ticks
ax.xaxis.set_minor_locator(md.DayLocator(interval=1))

# set ticks length
ax.tick_params(axis ='x', which ='major', length=10)
ax.tick_params(axis ='x', which ='minor', length=5)

plt.show()

print("End")
