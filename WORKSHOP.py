import pandas as pd

cpi = pd.read_csv('data/cpi.csv', header=0).dropna()
print(cpi)

exchange_rate = pd.read_csv('data/exchange_rate.csv',header=0).dropna()

print(exchange_rate)

cpi_mean = cpi.groupby('half_year').mean()
print(cpi_mean)

def discard_date(string):
    splits = string.split('/')
    year = splits[2]
    month = splits[1]
    half_year = 'H1'

    if(int(year) <= 20):
        year = '20' + str(year)
    else:
        year = '19' + str(year)
    if(int(month) > 6):
        half_year = 'H2'
    return year + '-' + half_year



exchange_rate['date'] = exchange_rate['date'].apply(discard_date)
exchange_rate = exchange_rate.groupby('date').mean()

### change column from date -> half_year in exchange rate dataset ###
exchange_rate.index.names = ['half_year']

### change column from value -> exchange_rate in exchange rate dataset ###
exchange_rate = exchange_rate.rename(columns={'value':'exchange_rate'})

cpi_mean = cpi_mean.rename(columns={'value':'CPI'})

print(exchange_rate, cpi)

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15,8))
ax.plot(exchange_rate['exchange_rate'], label='Exchange Rate')

ax2 = ax.twinx()
ax2.plot(cpi_mean['CPI'], color='orange', label='CPI Value')

plt.legend()
plt.show()
merged = pd.merge(exchange_rate, cpi_mean, on='half_year')

print(merged.corr())

