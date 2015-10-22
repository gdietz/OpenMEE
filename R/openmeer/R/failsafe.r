failsafe.wrapper <- function(data, type="Rosenthal", alpha=.05, target=NULL, digits=4) {
	# wraps metafor fsn() to yield results suitable for use in OpenMEE results window output
	
	res <- fsn(yi=data$yi, vi=data$vi, type=type, alpha=alpha, target=target, digits=digits)
	
	#results.info <- c(list(Summary=list(type="vector", description="Failsafe Analysis Summary")),
	#		fsn.info())
	
	summary_str <- paste(capture.output(res), collapse="\n")
	
	
	results <- list("Summary"  = res,
			        "res"      = c(list(Summary=summary_str), res),
					"res.info" = fsn.info()
					)
	results
}

fsn.info <- function() {
	list(
		Summary = list(type="vector", description="Failsafe Analysis Summary"),
		type   = list(type="vector", description='the method used'),
		fsnum  = list(type="vector", description='the calculated fail-safe N.'),
		alpha  = list(type="vector", description='the target alpha level.'),
		pval   = list(type="vector", description='the p-value of the observed results. NA for the Orwin method.'),
		meanes = list(type="vector", description='the average effect size of the observed results. NA for the Rosenthal method.'),
		target = list(type="vector", description= 'the target effect size. NA for the Rosenthal and Rosenberg methods.')
	)
}