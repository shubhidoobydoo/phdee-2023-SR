local outputpath = "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW2\output" 

	cd "`outputpath'"

	ssc install coefplot, replace
	ssc install estout, replace
	ssc install outreg2, replace 
	ssc install blindschemes, all
	set scheme plotplainblind, permanently

*****Q1 - Table
	eststo control: quietly estpost summarize electricity sqft temp if retrofit == 0
	eststo treatment: quietly estpost summarize electricity sqft temp  if retrofit == 1
	eststo diff: quietly estpost ttest electricity sqft temp, by(retrofit) unequal
	esttab control treatment diff, cells("mean(pattern(1 1 0) fmt(2)) b(star pattern(0 0 1) fmt(2))" sd(pattern(1 1 0))) label nonumbers mtitles("Control" 		"Treatment" "Comparison")	
	
	outreg2 using table_stata.tex, label 2aster tex(frag) dec(2) replace ctitle("Summary Table")

***Q2 - 2 way plot

	twoway (scatter electricity sqft)
	graph export twoway_stata.pdf, replace

***Q3 - Regression
	reg electricity sqft temp retrofit

	outreg2 using output_stata.tex, label 2aster tex(frag) dec(2) replace ctitle("Ordinary least squares")
			
