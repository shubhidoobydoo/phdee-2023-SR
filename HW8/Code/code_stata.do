local outputpath = "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW7\output" 
**Change the outpath

***Q1
collapse(mean) recyclingrate, by(year nyc nj ma)

line recyclingrate year if nyc == 1, lc(red) || line recyclingrate year if nj == 1, lc(blue) ||  line recyclingrate year if ma == 1, lc(green) xtitle("Year") ytitle("Avg Recycling Rate") 
legend(label(1 "NYC") label (2 "NJ") label(3 "MA"))

graph save "Graph" "/Users/shubhsrirajendra/Desktop/Classes/Env2/HW8/Q1.gph", replace

****Q2
***Data from 1997-04 

encode region, gen(region2)

drop if year > 2004

generate year0=nyc==1 & year==2002
g yearp1 = nyc==1 & year == 2003
g yearp2 = nyc == 1 & year == 2004 

g yearm2 = nyc == 1 & year == 2000 
g yearm3 = nyc == 1 & year == 1999 
g yearm4 = nyc == 1 & year == 1998
g yearm5 = nyc == 1 & year == 1997



areg recyclingrate  i.year i.yearm5 i.yearm4 i.yearm3 i.yearm2 i.year0 i.yearp1 i.yearp2, absorb(region2) cluster(region2)

generate treat=nyc==1 & year >= 2002

areg recyclingrate  treat, absorb(region2) cluster(region2)




**Q3
*Synthetic DID

g post = year > 2001
g treated = nyc == 1
g pause = 1 if nyc ==1 & year > 2001 & year < 2005
replace pause = 0 if pause == . 

sdid recyclingrate region2 year pause, vce(bootstrap) graph



***Q4
*Event Study

xtset region2 year
xtreg recyclingrate treated##ib2001.year, fe cluster(region2)
estimates store m1

coefplot (m1), drop (_cons ) ci xtitle(Year) ytitle(Recycling Rate) caption("Coefficients with 95% confidence intervals") title("Effect of Pause on Recycling Rate in NYC") ylabel(1 "1997" 2 "1998" 3 "1999" 4 "2000" 5 "2002" 6 "2003" 7 "2004" 8 "2005" 9 "2006" 10 "2007" 11 "2008" 12 "Treat x 1997" 13 "Treat x 1998" 14 "Treat x 1999" 15 "Treat x 2000" 16 "Treat x 2002" 17 "Treat x 2003" 18 "Treat x 2004" 19 "Treat x 2005" 20 "Treat x 2006" 21 "Treat x 2007" 22 "Treat x 2008")

*generate year0=nyc==1 & year==2002
*g yearp1 = nyc==1 & year == 2003
*g yearp2 = nyc == 1 & year == 2004 
*g yearp3 = nyc == 1 & year == 2005
*g yearp4 = nyc == 1 & year == 2006
*g yearp5 = nyc == 1 & year == 2007
*g yearp6 = nyc == 1 & year == 2008


*g yearm2 = nyc == 1 & year == 2000 
*g yearm3 = nyc == 1 & year == 1999 
*g yearm4 = nyc == 1 & year == 1998
*g yearm5 = nyc == 1 & year == 1997

*areg recyclingrate  i.year i.yearm5 i.yearm4 i.yearm3 i.yearm2 i.year0 i.yearp3 i.yearp2 i.yearp3 i.yearp4 i.yearp5 i.yearp6, absorb(region2) cluster(region2)




***Q5
*a. Plot

collapse(mean) recyclingrate, by(year nyc)

line recyclingrate year if nyc == 1, lc(red) || line recyclingrate year if nyc == 0, lc(blue)  xtitle("Year") ytitle("Avg Recycling Rate") legend(label(1 "Treated") label (2 "Control")) 
graph export "/Users/shubhsrirajendra/Desktop/Classes/Env2/HW8/5a.pdf", as(pdf) name("Graph")


*b. Plot - synthetic control 

g state = "NY" if nyc == 1
replace state = "MA" if ma == 1
replace state = "NJ" if nj == 1
encode state, gen(state2)

egen avg_ny = mean(recyclingrate) if nyc ==1, by(year nyc)
replace avg_ny = recyclingrate if avg_ny ==.

drop if region == "Bronx"|region == "Queens"

*Sorting - idk why but Lin said so

sort state region year
egen stateregionuniqueid = concat(state region)

replace stateregionuniqueid = "NYC" if stateregionuniqueid == "NYCBrooklyn"

encode stateregionuniqueid, gen(nstateuniqueregion)


*egen stateregion = group(state region)

tsset nstateuniqueregion year
synth avg_ny incomepercapita(1997(1)2001) nonwhite(1997(1)2001) munipop2000 collegedegree2000 democratvoteshare2000, trunit(208) trperiod(2002) fig



*c. Plot - Synthetic control and placebo

synth_runner avg_ny incomepercapita(1997(1)2001) nonwhite(1997(1)2001) munipop2000 collegedegree2000 democratvoteshare2000, trunit(208) trperiod(2002) gen_vars




*d. Plot - Final SC over time






