local outputpath = "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW7\output" 
cd "`outputpath'"

tab date if month == 3 & year == 2020 & day == 1

*Binary treatment 
g treat = 1 if date >= 21975
replace treat = 0 if treat == .


*Log variable 
g ln_mw = ln(mw)
 
*Zone as a string wont work
encode zone, gen(zone1)

 
*Q1a
gen X = temp*pcp
reg ln_mw i.zone1 i.month i.dow i.hour treat X, vce(robust)
 
*Q1b
 
drop if month == 1 | month == 2
 
*Mahalanobis is default 
 
teffects nnmatch (ln_mw temp pcp) (treat), ematch(zone1 dow hour month) atet vce(robust) nneighbor(1)
 
 
*Q2a
reg ln_mw i.zone1 i.month i.dow i.hour i.year treat X, vce(robust)

*Q3

drop if year < 2019

g y2020 = 1 if year == 2020
replace y2020 = 0 if y2020 == .


g y2019 = 1 if year == 2019
replace y2019 = 0 if y2019 == . 

teffects nnmatch (ln_mw temp pcp) (y2020), ematch(zone1 dow hour month) atet vce(robust) nneighbor(1) generate(mw_hat)

egen mw_hat22 = rowmean(mw_hat?)

gen ln_mw_hat = ln(mw_hat22)

g y = ln_mw - ln_mw_hat

reg y y2020, vce(robust)