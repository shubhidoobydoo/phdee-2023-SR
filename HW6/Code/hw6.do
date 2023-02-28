
import delimited "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW5\instrumentalvehicles.csv"

local outputpath = "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW6\output" 
cd "`outputpath'"



*Treated variable
g treated = 1 if length > 224
replace treated = 0 if length < 225

g mpg2 = mpg*mpg

*MPG as y
reg mpg treated mpg2 car length
predict mpgh

*Second stage

ivregress 2sls price (mpg = mpgh) car

estimates store r1

outreg2 using yourtablefile, replace bdec(3) ctitle("Second stage - RD as IV") title(Dependent Variable: MPG) addstat(N, mean, sd)

outreg2 using hw6q1.tex, replace bdec(3) ctitle("Second-Stage Results: RD as IV") title(Dependent Variable: Car)  se


*ATE
estat firststage



*plot 

rdplot mpgh length, c(225) n(20 20) p(2)





