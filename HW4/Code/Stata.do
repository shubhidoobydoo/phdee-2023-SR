***HW4

import delimited "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW4\fishbycatch.csv"

local outputpath = "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW4\output" 

	cd "`outputpath'"



*Reshape
reshape long salmon shrimp bycatch, i(firm) j(month)

g before = 0
replace before = 1 if month < 13


g after = 0
replace after = 1 if month > 12

*Q1
*Indicator var is created by the i
*Regression

reg bycatch after##treated salmon shrimp before after i.firm i.month, cluster(firm)


estimates store hw4a
outreg2 [hw4a] using hw4a.tex, label 2aster tex(frag) dec(2) replace ctitle("Model (a)")
	
*Q2
*Within estimation

*Demean

egen bcm = mean(bycatch), by (firm) 
g dm = bycatch - bcm

egen sm = mean(shrimp), by (firm) 
g shm = shrimp - sm

egen sam = mean(salmon), by (firm) 
g salm = salmon - sam

g interaction = after*treated

egen im = mean(interaction), by(firm)
g intm = interaction - im

regress dm intm shm salm i.firm i.month, cluster(firm)
estimates store hw4b
outreg2 [hw4b] using hw4b.tex, label 2aster tex(frag) dec(2) replace ctitle("Model (b)")

*Q3
*Format - 1 table
outreg2 [hw4a] using hw4c.tex, label 2aster tex(frag) dec(2) replace ctitle("Model (a)") keep(interaction shrimp salmon)

outreg2 [hw4b] using hw4c.tex, label 2aster tex(frag) dec(2) append ctitle("Model (b)") keep(intm salm shm)
