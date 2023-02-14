#!/usr/bin/env python
# coding: utf-8

# In[1]:



from IPython import get_ipython
get_ipython().magic('reset -sf')


# In[2]:


pip install mysql-connector-python


# In[4]:


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
from mysql.connector import Error
from scipy import stats
from pathlib import Path


# In[5]:


outputpath = r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW4\output'
fbc = pd.read_csv(r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW4\fishbycatch.csv')


# In[6]:


#Reshaping
fbc2 = pd.wide_to_long(fbc, ['salmon', 'shrimp', 'bycatch'], i = 'firm', j = 'month' )
fbc2 = fbc2.reset_index()


# In[7]:


c = fbc2[(fbc2['treated'] == 0)]
t = fbc2[(fbc2['treated'] == 1)]


# In[8]:


t2 = t.groupby(['month']).mean('bycatch')
t2 = t2.reset_index()
t2.style.format("{:.1f}")
lines = t2.plot(x='bycatch', y = 'month')


# In[9]:


c2 = c.groupby(['month']).mean('bycatch')
c2 = c2.reset_index()
c2.style.format("{:.1f}")
#lines = c2.plot(x='bycatch', y = 'month')


# In[10]:


#Q1 visual representation of bycatch by treatment status

fig = plt.figure()
plt.ticklabel_format(style='plain')
for frame in [c2, t2]:
    plt.plot(frame['month'], frame['bycatch'], label = ['treated', 'control'])
plt.xlabel('Month')
plt.ylabel('Bycatch')
plt.title("Treated vs Control")
plt.gca().legend(('Control','Treated'))
plt.savefig('HW4Q1.pdf',format='pdf')
#plt.show()


# In[11]:


#Q2 DiD
#Pretreated
q2t= fbc2[(fbc2['treated'] == 1) & (fbc2['month'] == 12)].mean()

#Post
q2t2 = fbc2[(fbc2['treated'] == 1) & (fbc2['month'] == 13)].mean()

diff1 = q2t2['bycatch'] - q2t['bycatch']
diff1

#Precontrol

q2c= fbc2[(fbc2['treated'] == 0) & (fbc2['month'] == 12)].mean()

#Post
q2c2 = fbc2[(fbc2['treated'] == 0) & (fbc2['month'] == 13)].mean()



diff2 = q2c2['bycatch'] - q2c['bycatch']
diff2

fdiff = diff1 - diff2
fdiff


# In[42]:


#Q3a. 

#Estimate the treatment effect of the program on bycatch using a regression-based two-period 
#difference-in-differences estimator with estimating equation:

#bycatch_it = alpha + Lambda_2017 + Gamma*g(i) + Delta*treat_it + error_it
#Lambda = Pre period
#g(i) = Treated firm 
#Treat = Treatment (time sensitive)


#Between dec 2017 and jan 2018
time = fbc2[(fbc2['month'] == 12) | (fbc2['month'] == 13)]


#Pre period intercept

time['lambda'] = 0 
time.loc[fbc2['month'] == 12, 'lambda'] = 1


#Treatment/control group indicator
time['treatment'] = 0
time.loc[fbc2['treated'] == 1, 'treatment'] = 1

#Treated and at time i indicator
time['timetr'] = 0
time.loc[(time['treatment'] == 1) & (time ['month'] == 13) , 'timetr'] = 1


ols = sm.OLS(time['bycatch'],
                sm.add_constant(time[['lambda', 'treatment', 'timetr']]))
results = ols.fit()


#Formatting table
robust = results.get_robustcov_results(cov_type = 'cluster', groups = time['firm']) 
beta = np.round(robust.params,2) 
params, = np.shape(beta) 

nobs = np.array(robust.nobs) 


#CI and formatiing 
ci = pd.DataFrame(np.round(robust.conf_int(),2)) 
cif = '(' + ci.loc[:,0].map(str) + ', ' + ci.loc[:,1].map(str) + ')' 

output = pd.DataFrame(pd.concat([pd.Series(np.append(beta,nobs)),cif],axis = 1).stack()) 
output.columns = ['(1)']
output.index = pd.concat([pd.Series(['Alpha','Pre period','Treated','Time treated','Observations']),pd.Series([' ']*params)], axis = 1).stack()

output


# In[43]:


#Q3b. #Suppose you would like to use the full monthly sample to improve on what you did in the previous #question. Using the full monthly sample, estimate the treatment effect of the program on bycatch #using a regression-based difference-in-differences estimator using the regression:

#bycatch_i,t = c_i + λ_t + γg(i) + δtreat_i,t + ε_i,t

#Lambda - Time period indicator

#Dummy for month 

dv = pd.get_dummies(fbc2['month'],prefix = 'time')

#Specific time period of being treated


fbc2['timetr'] = 0 
fbc2.loc[(fbc2['treated'] == 1) & (fbc2 ['month'] > 12) , 'timetr'] = 1


xvar = pd.concat([fbc2[['treated', 'timetr']],dv],axis = 1) 
yvar = fbc2['bycatch']

ols2 = sm.OLS(yvar,sm.add_constant(xvar)).fit()

robust2 = ols2.get_robustcov_results(cov_type = 'cluster', groups = fbc2['firm'])

#Formatting

beta2 = np.round(robust2.params,2) 
params2, = np.shape(beta2)

nobs2 = np.array(robust2.nobs)




#CI and formatiing 
ci2 = pd.DataFrame(np.round(robust2.conf_int(),2)) 
cif2 = '(' + ci2.loc[:,0].map(str) + ', ' + ci2.loc[:,1].map(str) + ')'

output2 = pd.DataFrame(pd.concat([pd.Series(np.append(beta2,nobs2)),cif2],axis = 1).stack())
output2.columns = ['(2)'] 
output2.index = pd.concat([pd.Series(['Alpha','Treated','Time Treated','dum','dum','dum', 'dum', 'dum', 'dum','dum','dum','dum', 'dum', 'dum', 'dum', 'dum','dum','dum', 'dum', 'dum', 'dum', 'dum','dum','dum', 'dum', 'dum', 'dum', 'Observations']),pd.Series([' ']*params2)], axis = 1).stack()

#output2.drop(output2.index [8:]) 
output2


# #Q3b.
# #Suppose you would like to use the full monthly sample to improve on what you did in the previous
# #question. Using the full monthly sample, estimate the treatment effect of the program on bycatch
# #using a regression-based difference-in-differences estimator using the regression:
# 
# #bycatch_i,t = c_i + λ_t + γg(i) + δtreat_i,t + ε_i,t
# 
# #Lambda - Time period indicator
# 
# 
# #Dummy for month
# dv = pd.get_dummies(fbc2['month'],prefix = 'time')
# 
# 
# #Specific time period of being treated
# 
# fbc2['timetr'] = 0
# fbc2.loc[(fbc2['treated'] == 1) & (fbc2 ['month'] > 12) , 'timetr'] = 1
# 
# xvar = pd.concat([fbc2[['treated', 'timetr']],dv],axis = 1)
# yvar = fbc2['bycatch']
# 
# ols2 = sm.OLS(yvar,sm.add_constant(xvar)).fit()
# 
# robust2 = ols2.get_robustcov_results(cov_type = 'cluster', groups = fbc2['firm'])
# 
# #Formatting
# 
# beta2 = np.round(robust2.params,2) 
# params, = np.shape(beta2) 
# 
# nobs2 = np.array(robust2.nobs) 
# 
# 
# #CI and formatiing 
# ci2 = pd.DataFrame(np.round(robust2.conf_int(),2)) 
# cif2 = '(' + ci2.loc[:,0].map(str) + ', ' + ci2.loc[:,1].map(str) + ')' 
# 
# 
# 
# dropdummy = []
# for i in ['treated','timetr']: 
#     dropdummy.append(xvar.columns.get_loc(i))
# dropdummy.append(params1-1) # Adds constant term
# 
# 
# output2 = pd.DataFrame(pd.concat([pd.Series(np.append(beta2,nobs2)),cif2],axis = 1).stack()) 
# output2.columns = ['(2)']
# output2
# 
# 
# #output2.index = pd.concat([pd.Series(['Treatment group','Treated','Pre-period','Constant','Observations']),pd.Series([' ']*params)], axis = 1).stack()
# 
# #output2.drop(output2.index [8:])
# #output2

# In[44]:


#Q3c. B but with added var: firm size, shrimp, salmon

yvar2 = fbc2['bycatch']
dv2 = pd.get_dummies(fbc2['month'],prefix = 'time',drop_first = True)
xvar2 = pd.concat([fbc2[['treated','timetr','shrimp','salmon','firmsize']],dv2],axis = 1)

ols3 = sm.OLS(yvar2,sm.add_constant(xvar2)).fit()

#olsrobust2.summary()

robust3 = ols3.get_robustcov_results(cov_type = 'cluster', groups = fbc2['firm'])


#Formatting

beta3 = np.round(robust3.params,2) 
params3, = np.shape(beta3) 

nobs3 = np.array(robust3.nobs) 

#CI and formatiing 
ci3 = pd.DataFrame(np.round(robust3.conf_int(),2)) 
cif3 = '(' + ci3.loc[:,0].map(str) + ', ' + ci3.loc[:,1].map(str) + ')' 

output3 = pd.DataFrame(pd.concat([pd.Series(np.append(beta3,nobs3)),cif3],axis = 1).stack())
output3

output3.columns = ['(3)']

output3.index = pd.concat([pd.Series(['Alpha','Treated','Time Treated', 'shrimp', 'salmon', 'firmsize', 'dum','dum','dum', 'dum', 'dum', 'dum', 'dum','dum','dum', 'dum', 'dum', 'dum', 'dum','dum','dum', 'dum', 'dum', 'dum', 'dum','dum','dum', 'dum', 'dum', 'Observations']),pd.Series(['']*params3)], axis = 1).stack()

output3


# In[47]:


#All together in one table

#output.reset_index(inplace=True, drop=True)

#output2.reset_index(inplace=True, drop=True)


#output3.reset_index(inplace=True, drop=True)

pd.set_option('display.max_columns', 3) #replace n with the number of columns you want to see completely
pd.set_option('display.max_rows', 123)

total = pd.concat([output, output2, output3], axis=0)

total

total.to_latex('python.tex')

