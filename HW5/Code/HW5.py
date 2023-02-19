#!/usr/bin/env python
# coding: utf-8

# In[1]:



from IPython import get_ipython
get_ipython().magic('reset -sf')


# In[184]:


pip install stargazer


# In[185]:


pip install linearmodels


# In[3]:


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
from stargazer.stargazer import Stargazer as stargazer
from stargazer.stargazer import LineLocation
from linearmodels.iv import IV2SLS, IVGMM


# In[4]:


outputpath = r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW5\output'
data = pd.read_csv(r'C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW5\instrumentalvehicles.csv')


# In[5]:


#Q1. Run the ordinary-least-squares regression of price on mpg, the car indicator variable, and a constant.
#Report and interpret the coefficient on miles per gallon (do not construct a table).

ols = sm.OLS(data['price'],
                sm.add_constant(data[['mpg', 'car']])).fit()
ols.summary()


# In[6]:


#Q3a. Perform two-stage-least-squares estimation by hand using weight as the excluded instrument.
#(First regress mpg on all of the instruments. Save the fitted values from the first stage ˆmpg and
#use the fitted values in place of the endogenous variable in the second stage price regression.)

#Basically, z is weight abhi 



#Stage1
y = data['mpg']
x = data['car']
z = data[['weight', 'car']]

z_c = sm.add_constant(z)
fsls = sm.OLS(y,sm.add_constant(z_c)).fit()
mpg = fsls.fittedvalues


fstat = fsls.tvalues.loc['weight']**2
fstats = round(fstat,2)

#Stage2 
y2 = data['price']
#mpg = fittedv
x_c = sm.add_constant(x)
xv = pd.concat([x_c, mpg], axis = 1)

xv.columns = ["Cons", "Car", "MPG"]
ssls = sm.OLS(y2, sm.add_constant(xv)).fit()

#ssls = sm.OLS(y2, sm.add_constant(pd.concat([x_c,mpg],axis = 1))).fit()


ssls.summary()
fstats


# In[7]:


#Q3b. Weight sq

#Stage1
y2 = data['mpg']
x2 = data['car']
data['weight2'] = data['weight'].apply(lambda x: x ** 2)
z2 = data[['weight2', 'car']]

z_c2 = sm.add_constant(z2)
fsls2 = sm.OLS(y,sm.add_constant(z_c2)).fit()
mpg2 = fsls2.fittedvalues


fstat2 = fsls2.tvalues.loc['weight2']**2
fstats2 = round(fstat2,2)

#Stage2 
y22 = data['price']
#mpg = fittedv
x_c2 = sm.add_constant(x2)
xv2 = pd.concat([x_c2, mpg2], axis = 1)

xv2.columns = ["Cons", "Car", "MPG"]
ssls2 = sm.OLS(y22, sm.add_constant(xv2)).fit()
ssls2.summary()


# In[8]:


#Q3c. Height IV
#Stage1
y3 = data['mpg']
x3 = data['car']
z3 = data[['height', 'car']]

z_c3 = sm.add_constant(z3)
fsls3 = sm.OLS(y,sm.add_constant(z_c3)).fit()
mpg3 = fsls3.fittedvalues


fstat3 = fsls3.tvalues.loc['height']**2
fstats3 = round(fstat3,2)

#Stage2 
y23 = data['price']
#mpg = fittedv
x_c3 = sm.add_constant(x3)
xv3 = pd.concat([x_c3, mpg3], axis = 1)

xv3.columns = ["Cons", "Car", "MPG"]
ssls3 = sm.OLS(y23, sm.add_constant(xv3)).fit()

#ssls = sm.OLS(y2, sm.add_constant(pd.concat([x_c,mpg],axis = 1))).fit()

ssls3.summary()


# In[14]:


#Formatting with Stargazer


output = stargazer([ssls, ssls2, ssls3])
output.covariate_order(['MPG','Car', 'Cons'])
output.rename_covariates({'MPG':'MPG','Car':'Car type (Sedan)', 'Constant': 'Const'})
output.add_line('F-test for Stage 1',[fstats, fstats2, fstats3], LineLocation.FOOTER_TOP)
output.significant_digits(2)
output.show_degrees_of_freedom(False)
output

#Fking genius is what this stargazer is!


# In[176]:


#To latex
#output.render_latex()

tex_file = open('outputhw5.tex', "w" ) #This will overwrite an existing file
tex_file.write( output.render_latex() )
tex_file.close()


# In[12]:


#Q4 Calculate the IV estimate using GMM with weight as the excluded instrument. 
#Report the estimated second-stage coefficient and standard error or confidence
#interval for mpg What factors account for the differences in the standard errors?


gmm = IVGMM.from_formula('price ~ 1 + car + [mpg ~ weight]',data).fit() 
gmm

