import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('PopTrendsBData3Aggs.csv')
print(df)
print(df.columns)
print(df.info())
df.dropna(inplace=True)



#fig = px.bar(df, x=)
df['Loss'] = -1*(df['StakeA'] - df['WinA'])
print('Max Loss: ', df.Loss.min())
print('Max Win: ', df.Loss.max())
print('Avg Win/Loss: ', df.Loss.mean())

# Create normalized histogram using seaborn
sns.histplot(df,x='Loss',
             bins=30,
             binrange=[-750,400],
             kde=False,
             stat='frequency')

plt.xlabel('Data')
plt.ylabel('Probability Density')
plt.title('Normalized Histogram')
plt.show()