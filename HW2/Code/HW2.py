#!/usr/bin/env python
# coding: utf-8

# In[629]:



from IPython import get_ipython
get_ipython().magic('reset -sf')


# In[1032]:



import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statistics
import style
import researchpy as rp
import scipy
from scipy import stats
from pathlib import Path


# In[631]:


outputpath = r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW2\output'


# In[632]:


elec_data = pd.read_csv(r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW2\kwh.csv')
df = pd.DataFrame(elec_data, columns = ['electricity','sqft','temp', 'retrofit'])


# In[906]:


control = df.loc[df['retrofit'] == 0]
treatment = df.loc[df['retrofit'] == 1]
cols = ['electricity','sqft','temp']
nobs2 = df.count().min()

rname = pd.concat([pd.Series(['electricity','sqft','temp']), pd.Series(["", "", ""])], axis = 1).stack()
cname = [("Control", "Mean", "(Std dev)"), ("Treatment", "Mean", "(Std dev)"), ("", "p-value", "")]


# In[907]:


cmean = control[cols].mean()
cmeans = cmean.map('{:.2f}'.format)
cstd = control[cols].std()
cstds = cstd.map('{:.2f}'.format)


tmean = treatment[cols].mean()
tmeans = tmean.map('{:.2f}'.format)
tstd = treatment[cols].std()
tstds = tstd.map('{:.2f}'.format)

diff = stats.ttest_ind(control[cols], treatment[cols])

pv = pd.Series(diff[1], index = ['electricity','sqft','temp'])
pv = pv.map('{:.2f}'.format)


# In[908]:


col0 = pd.concat([cmeans,cstds],axis = 1).stack()
col1 = pd.concat([tmeans,tstds],axis = 1).stack()
col0 = pd.DataFrame(col0)

nan = pd.Series(np.array(["","",""]), index = ['electricity','sqft','temp']) 
pn = pd.concat([pv,nan], axis = 1).stack()
tab = pd.concat([col0, col1, pn], axis = 1)
tab = pd.DataFrame(tab)

tab.index = rname
tab.columns = pd.MultiIndex.from_tuples(cname)
tab

os.chdir(outputpath) 
tab.to_latex('mean_py.tex') 


# In[575]:


##To get the number of each

numberobs = rp.summary_cat(df['retrofit'])
numberobs.T


# In[445]:


stats.ttest_ind(control['sqft'], treatment['sqft'])


# In[642]:


####Question 2 

#Provide graphical evidence that the retrofits worked. Plot kernel density plots of the electricity use for
#treated group and control group on the same graph using Python. Make sure to label the histogram
#appropriately

sns.displot(data = elec_data, x = 'electricity',  hue = "retrofit", kind = "kde")
plt.xlabel('Electricity use')
plt.savefig('Q2_density.pdf',format='pdf')


sns.displot(data = elec_data, x = 'electricity',  hue = "retrofit", kind = "hist")
plt.xlabel('Electricity use')
plt.savefig('Q2_hist.pdf',format='pdf')


# In[942]:


####Question 3

#Suppose you want to estimate the linear equation Y = βX + ε where Y is an n × 1 vector of the
#dependent variable, X is an n × p + 1 matrix of the predictor variables in table 1 and a column of
#ones, and ε is an n × 1 vector of unobserved random error. Use the following methods to estimate ˆβ,
#presenting coefficients in a single table with a column for each estimation technique (note I am not
#requiring that you present confidence intervals):


#(a) OLS by hand. Use the Numpy package in Python to create an array X that is the n × p + 1 matrix
#of the predictor variables in table 1 and a column of ones and an array Y that is the n × 1 vector
#of the dependent variable. Use matrix operations to calculate ˆβ. Recall that ˆβ = (X′X)−1X′Y
#is the closed-form solution to the least-squares minimization problem

N = elec_data.shape[0]
X = np.stack([np.ones((N,)), elec_data.sqft.values, elec_data.temp.values, elec_data.retrofit.values], axis = 1)
X
Y = elec_data.electricity.values[:,np.newaxis]
betahat = np.linalg.inv(X.T @ X) @ X.T @ Y
B_hat = pd.DataFrame(betahat, index = ['Constant', 'sqft', 'temp', 'retrofit'], columns = ['Estimates'])
B_hat
B_hat.to_latex('OLS_hand.tex')


# In[1055]:


#(b) OLS by simulated least squares. Use the Scipy.optimize.minimize() function in Python to numerically minimize
#the sum of squares objective function. Recall that the sum of squares isPn
#i=1 (yi − βxi)2 where yi and xi are (1 × 1) and (1 × p + 1) vectors respectively

xv = np.array([np.ones(1000), elec_data.sqft, elec_data.temp, elec_data.retrofit])
xxv = xv.transpose()
yv = np.array(elec_data.electricity)

beta = [1, 2, 3, 4]


def f(beta):
    return np.sum((yv - np.dot(xxv, beta))**2)

solsg = scipy.optimize.minimize(f,beta)
final = solsg.x
final2 = pd.DataFrame(final,  index = ['Constant', 'sqft', 'temp', 'retrofit'], columns = ['Estimates'])
final2

final2.to_latex('final.tex')


# In[1046]:





# In[758]:


#(c) OLS using a canned routine. Use the StatsModels package in Python using the OLS routine.


ols = sm.OLS(elec_data['electricity'],sm.add_constant(elec_data.drop('electricity',axis = 1))).fit()
olsresult = ols.summary()
olsresult

betaols = ols.params.to_numpy() # save estimated parameters
params, = np.shape(betaols) # save number of estimated parameters
nobs3 = int(ols.nobs)

betaols = np.round(betaols,2)
#order = [1,2,0]
output = pd.DataFrame(np.column_stack([betaols])).reindex(order)

rownames = pd.Series(['sqft','retrofit','temp','Observations'])
colnames = ['Estimates']


output = pd.DataFrame(output.stack().append(pd.Series(nobs3)))
output.index = rownames
output.columns = colnames

## Output directly to LaTeX
output.to_latex('sampleoutput.tex')

#olsresult.to_latex('olsc.tex')

