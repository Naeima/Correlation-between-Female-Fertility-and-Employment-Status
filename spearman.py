
#Student Number: C1887413

'''This code calculates the Spearman Rank Correlation Coefficient (Rs). 

to run:
........python  spearman.py

'''

# importing libraries 
import numpy as np
import pandas as pd
import scipy.stats

#  Open and read the data
df=pd.read_csv('master.csv')
#print(df)

x= df['Fertility Rate']
y= df['Unemployment Rate']
# Calculating  Spearman's using Scipy for Fertility Rate Vs Unemployment Rate.
res= scipy.stats.spearmanr(x, y)[0]
print(res)

# Calculating Spearman's using Scipy for Fertility Rate Vs Employment Rate.
x1= df['Fertility Rate']
y1= df['Employment Rate']
# Spearman's using Scipy
res1= scipy.stats.spearmanr(x1, y1)[0]
print(res1)
