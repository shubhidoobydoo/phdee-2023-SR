ssc install weakivtest

import delimited "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW5\instrumentalvehicles.csv"

local outputpath = "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW5\output" 

	cd "`outputpath'"


*Q1	
ivregress liml price  car (mpg = weight car) , vce(robust)

estimates store r1

outreg2 using yourtablefile, replace bdec(3) ctitle("Second-Stage Results: IV Liml") title(Dependent Variable: Car) addstat(N, mean, sd) starlevels(* 0.1 ** 0.05 *** 0.01) eqlabels("Independent Variable" "Weight (Excluded Instrument)" "Constant") se b(2) tstat(2) pvalue(2)

outreg2 using q1.tex, replace bdec(3) ctitle("Second-Stage Results: IV Liml") title(Dependent Variable: Car)  se


*Q2

estout r1
weakivtest