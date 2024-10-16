import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
gamble = pd.read_csv('../Data/PopTrendsBData3Aggs.csv')
codes = pd.read_csv('../Data/countrycode.csv')
codes = codes[['name', 'country-code']]



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

plt.xlabel('Winnings (USD)')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.show()