import delimited "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW2\kwh.csv"

local outputpath = "C:\Users\Sherry Baby\Desktop\Classes\Env-2\phdee-2023-SR\HW3\output" 

	cd "`outputpath'"

	ssc install coefplot, replace
	ssc install estout, replace
	ssc install outreg2, replace 
	ssc install blindschemes, all
	set scheme plotplainblind, permanently

	
*****Q5
g le = ln(electricity)
g ls = ln(sqft)
g lt = ln(temp)


***OLS
reg le ls retrofit lt 

***Bootstrap
reg le ls retrofit lt, vce(bootstrap, reps(1000))

***Also to basically show that I can do it the other way too: 

eststo treated:
		mat betas = J(1000,4,.) 
		forvalues i = 1/1000 {
			preserve 
				bsample 
				
				reg le ls retrofit lt
				
				mat betas[`i',1] = _b[ls] 
				mat betas[`i',2] = _b[retrofit]
				mat betas[`i',3] = _b[lt]
				mat betas[`i',4] = _b[_cons]
			restore 
		}
		
		
		capture program drop bootstrapsample
		program define bootstrapsample, eclass
			tempname betas betas1 betas2 betas3 betas4
			mat `betas' = J(1000,4,.)
			forvalues i = 1/1000 {
				preserve
					bsample 
					quietly: reg le ls retrofit lt
					
					mat `betas'[`i',1] = _b[ls] 
					mat `betas'[`i',2] = _b[retrofit]
					mat `betas'[`i',3] = _b[lt]
					mat `betas'[`i',4] = _b[_cons]
					di `i' 
				restore
			}
			svmat `betas', name(temp)
				corr temp1 temp2 temp3 temp4, cov 
				mat A = r(C) 
				drop temp1 temp2 temp3 temp4
				
			reg le ls retrofit lt
			ereturn repost V = A 
		end
		
		bootstrapsample 
		estimates store bootreg
		
		
		outreg2 [bootreg] using sampleoutput_stata.tex, label stat(coef ci) tex(frag) dec(2) replace ctitle("Ordinary least squares")


		

		
****Marginal effects - attempt 1

reg elec sqft retrofit temp
margins, dydx(*)

eststo controls:
mat betas = J(1000,4,.) 
		forvalues i = 1/1000 {
			preserve 
				bsample 
				
				reg elec sqft retrofit temp
				
				mat betas[`i',1] = _b[sqft] 
				mat betas[`i',2] = _b[retrofit]
				mat betas[`i',3] = _b[temp]
				mat betas[`i',4] = _b[_cons]
			restore 
		}
		
		
		capture program drop bootstrapsample
		program define bootstrapsample, eclass
			tempname betas betas1 betas2 betas3 betas4
			mat `betas' = J(1000,4,.)
			forvalues i = 1/1000 {
				preserve
					bsample 
					quietly: reg elec sqft retrofit temp
					
					mat `betas'[`i',1] = _b[sqft] 
					mat `betas'[`i',2] = _b[retrofit]
					mat `betas'[`i',3] = _b[temp]
					mat `betas'[`i',4] = _b[_cons]
					di `i' 
				restore
			}
			svmat `betas', name(temp)
				corr temp1 temp2 temp3 temp4, cov 
				mat A = r(C) 
				drop temp1 temp2 temp3 temp4
				
			reg elec sqft retrofit temp
			ereturn repost V = A 
		end
		
		bootstrapsample 
		estimates store bootreg2
		


		
		
*****Making table

	esttab treated controls, cells("b(star pattern(1 1 ) fmt(2))" ci(pattern(1 1))) label nonumbers mtitles("Coefficient" "Marginal Effects")
	
****Plot


	coefplot, drop(_cons || retrofit) vertical yline(0) ytitle("Coefficient estimate")

	
	graph export graph.pdf, replace