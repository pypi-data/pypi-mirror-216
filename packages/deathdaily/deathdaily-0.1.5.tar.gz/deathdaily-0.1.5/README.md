# COVID-19 daily death prediction

deathdaily is a Python program using new_deaths.csv for predicting daily deaths due to COVID-19 in the next seven days. The prediction is based on the Xthe degree polynomial curve-fitting.

According to PyPI Stats, deathdaily has been downloaded by 10356 users worldwide as of Oct.14 2021.

X-axis is the xth day from Jan.22 2020 to the day you have downloaded new_deaths.csv file. Y-axis depicts the number of daily deaths in the country.

# new_deaths.csv

deathdaily needs a new_deaths.csv file for predicting the daily deaths of the next seven days.

The new_deaths.csv file is automatically downloaded by deathdaily from the following site:

https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv


# How to install deathdaily

$ pip install deathdaily

# How to run deathdaily using country with days and degree of polynomial curve-fitting

"country" shows which country you would like to predict the daily deaths of the next seven days.

"days" indicates how many days are used for Xth degree polynomial curve-fitting.

"degree" determined the degree of polynomial curve-fitting.

$ deathdaily Japan days degree

$ deathdaily Japan 200 7

country="Japan", days=200, degree=11

<img src="https://github.com/ytakefuji/covid-19_daily_death_prediction/raw/main/Japan.png" width=320 height=240 >


$ deathdaily 'United States' 200 11

<img src="https://github.com/ytakefuji/covid-19_daily_death_prediction/raw/main/United States.png" width=320 height=240 >

$ deathdaily Israel 200 9

<img src="https://github.com/ytakefuji/covid-19_daily_death_prediction/raw/main/Israel.png" width=320 height=240 >

$ deathdaily 'United Kingdom' 100 11

<img src="https://github.com/ytakefuji/covid-19_daily_death_prediction/raw/main/United Kingdom.png" width=320 height=240 >
