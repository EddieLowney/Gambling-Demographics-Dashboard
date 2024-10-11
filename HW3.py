import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pytz import country_names

import df_loading as dfl

# Load the CSV file
gamble = dfl.load_csv('PopTrendsBData3Aggs.csv')
codes = dfl.load_csv('countrycode.csv')
codes = codes[['name', 'country-code']]
gamble[country_names] = codes[name] where gamble[CountryID] == codes[country-code]


#fig = px.bar(df, x=)
gamble['Loss'] = -1*(gamble['StakeA'] - gamble['WinA'])
print('Max Loss: ', gamble.Loss.min())
print('Max Win: ', gamble.Loss.max())
print('Avg Win/Loss: ', gamble.Loss.mean())

# Create normalized histogram using seaborn
sns.histplot(gamble,x='Loss',
             bins=30,
             binrange=[-750,400],
             kde=False,
             stat='frequency'
             )

plt.xlabel('Data')
plt.ylabel('Probability Density')
plt.title('Normalized Histogram')
plt.show()