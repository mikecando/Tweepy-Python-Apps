import pandas
import numpy as np

# Load the data into a DataFrame
data = pandas.read_csv('trendData.csv')

groupTime = data.groupby('Timestamp')

print groupTime.groupby('TrendPhrase')

#for d in data:
    #print d

#groupTime = data.groupby('Timestamp').nunique().reset_index()
#data.groupby["Timestamp"] #.nunique().reset_index()
#print groupTime['Timestamp'].count()





groupTrend = data.groupby('TrendPhrase')

#print bytreatment.describe()
#print groupTrend['TrendPhrase'].count()


