#!/usr/bin/env python
# coding: utf-8

# In[5]:



from IPython import get_ipython
get_ipython().magic('reset -sf')


# In[158]:


pip install rdtools


# In[45]:


pip install scikit-learn


# In[13]:


pip install rdrobust


# In[51]:


pip install rdd


# In[67]:


pip install stargazer
#pip install linearmodels


# In[198]:


import math
import statsmodels.formula.api as smf

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
import mysql.connector
import rdrobust
from mysql.connector import Error
from scipy import stats
from pathlib import Path
from stargazer.stargazer import Stargazer as stargazer
from stargazer.stargazer import LineLocation
from linearmodels.iv import IV2SLS, IVGMM
#from rdrobust import rdrobust
from rdrobust import rdbwselect
from rdrobust import rdplot
from rdd import rdd
from statsmodels.graphics.regressionplots import abline_plot
from statsmodels.sandbox.regression.predstd import wls_prediction_std


# In[199]:


outputpath = r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW6\output'
data = pd.read_csv(r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW5\instrumentalvehicles.csv')


# In[200]:


data


# In[201]:


#Q2 Scatter plot
cutoff = 225

data['lc'] = data['length'] - cutoff
data['treated'] = (data['length'] > cutoff).astype(int)
treated = data['treated']

mpg = data['mpg']
length = data['length']
lc = data['lc']


plt.scatter(lc, mpg)
plt.axvline(x=0, color='r')
plt.xlabel('Length - Cutoff')
plt.ylabel('MPG')
plt.savefig('Q2.pdf',format='pdf')


# In[202]:


#Q3 First order polynomial fit

length = data['length']

df1 = data[data['length'] < 225]

y1 = df1['mpg']
x1 = df1['lc']

lhsols = sm.OLS(y1, sm.add_constant(x1)).fit()
#rhsols.summary()


df2 = data[data['length'] > 224]


y2 = df2['mpg']
x2 = df2['lc']


rhsols = sm.OLS(y2, sm.add_constant(x2)).fit()
#lhsols.summary()

fig, ax = plt.subplots()
ax.plot(x1, y1, 'o', label="Control")
#ax.plot(x1, y1, 'b-', label="True")
ax.plot(x1, lhsols.fittedvalues, 'r--.', label="OLS")
ax.legend(loc='best')


ax.plot(x2, y2, 'p', label="Treated")
#ax.plot(x1, y1, 'b-', label="True")
ax.plot(x2, rhsols.fittedvalues, 'g--.', label="OLS2")
ax.legend(loc='best')
plt.axvline(x=0, color='r')
plt.xlabel('Length - Cutoff')
plt.ylabel('MPG')
plt.savefig('Q3.pdf',format='pdf')


#Treatment effect

model = sm.OLS(data['mpg'], sm.add_constant(data[['treated', 'lc']])).fit(cov_type='HC1')
#print(model.summary())

output = stargazer([model])
output.covariate_order(['treated', 'lc', 'const'])
output.rename_covariates({'lc':'Length minus Cutoff','treated':'Treated', 'Const': 'Const'})
output.significant_digits(2)
output.show_degrees_of_freedom(False)
output

tex_file = open('outputhw6_3.tex', "w" ) #This will overwrite an existing file
tex_file.write( output.render_latex() )
tex_file.close()


# In[56]:


output


# In[206]:


#This worked too ig - maybe I can use this for q4

fig, ax = plt.subplots(figsize=(6, 6))

# add the plots for each dataframe
sns.regplot(x='length', y='mpg', data=df1, fit_reg=True, ci=None, ax=ax, label='After')
sns.regplot(x='length', y='mpg', data=df2, fit_reg=True, ci=None, ax=ax, label='Before')
ax.set(ylabel='y', xlabel='x')
ax.legend()
plt.show()


# In[203]:


#Q4 Second order

data['lc2'] = data['lc'] ** 2
below = data[data['treated'] == 0]

#below = sm.OLS(below['mpg'], sm.add_constant(below[['lc', 'lc2']])).fit()

#below.summary()

above = data[data['treated'] == 1]

#above = sm.OLS(above['mpg'], sm.add_constant(above[['lc', 'lc2']])).fit()


poly_above = np.polyfit(above['lc'], above['mpg'], 2)
poly_below = np.polyfit(below['lc'], below['mpg'], 2)

above['fitted_y'] = np.polyval(poly_above, above['lc'])
below['fitted_y'] = np.polyval(poly_below, below['lc'])
#above.summary()

fig, ax = plt.subplots()

ax.scatter(above['lc'], above['mpg'], label='Treated')
ax.scatter(below['lc'], below['mpg'], label='Control')
ax.plot(above['lc'], above['fitted_y'], 'r--.', label='Fitted (Treated)')
ax.plot(below['lc'], below['fitted_y'], 'g--.', label='Fitted (Control)')

ax.axvline(x=0, color='r')

ax.set_xlabel('Length - Cutoff')
ax.set_ylabel('MPG')
ax.legend()

plt.savefig('Q4.pdf',format='pdf')


# In[204]:


te = poly_above[0] - poly_below[0]
te


# In[208]:


#Q5 Fifth order
poly_above2 = np.polyfit(above['lc'], above['mpg'], 5)
poly_below2 = np.polyfit(below['lc'], below['mpg'], 5)

above['fitted_y2'] = np.polyval(poly_above2, above[['lc']])
below['fitted_y2'] = np.polyval(poly_below2, below[['lc']])
#above.summary()

fig, ax = plt.subplots()

ax.scatter(above['lc'], above['mpg'], label='Treated')
ax.scatter(below['lc'], below['mpg'], label='Control')
ax.plot(above['lc'], above['fitted_y2'], 'r--.', label='Fitted (Treated)')
ax.plot(below['lc'], below['fitted_y2'], 'g--.', label='Fitted (Control)')

ax.axvline(x=0, color='r')

ax.set_xlabel('Length - Cutoff')
ax.set_ylabel('MPG')
ax.legend()

plt.savefig('Q5.pdf',format='pdf')


# In[209]:


poly_above2[0] - poly_below2[0]


# In[210]:


#Q6 RD instrument for mpg

# first stage regression
data['mpg2'] = data['mpg']*data['mpg']
X = sm.add_constant(data[['treated', 'mpg', 'mpg2', 'car']])
model_1 = sm.OLS(data['mpg'], X).fit()

# predicted values of mpg
data['mpg_pred'] = model_1.predict(X)

# second stage regression
X = sm.add_constant(data[['mpg_pred', 'car']])
model_2 = sm.OLS(data['price'], X).fit()

# compute ATE
treatment = data[data['treated']>0]['price'].mean()
control = data[data['treated']<1]['price'].mean()
ATE = treatment - control

print('ATE:', ATE)
model_2.summary()


# In[211]:



data

