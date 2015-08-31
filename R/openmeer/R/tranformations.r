trans.scale.single.val.to.raw.scale <- function(value, metric) {
	# transforms a single value in the 'transformed' scale back to the 'raw' scale
	
	unlog <- function(x) {exp(x)}
	no.change <- function(x) {x}
	ztor <- function(x) {transf.ztor(x)}
	
	raw.scale.val <- switch(metric,
			SMD = no.change(value), # Hedges d
			ROM = unlog(value),     # Ln Response Ratio
			OR  = unlog(value),     # Log Odds Ratio
			RD  = no.change(value), # Rate Difference
			RR  = unlog(value),     # Log Relative Rate
			ZCOR = ztor(value),      # Fisher's Z-transform
			GEN = no.change(value)
	)
	raw.scale.val
}

raw.scale.single.val.to.trans.scale <- function(value, metric) {
	no.change <- function(x) {x}
	relog     <- function(x) {log(x)}
	rtoz      <- function(x) {transf.rtoz(x)}
	
	trans.scale.val <- switch(metric,
			SMD = no.change(value), # Hedges d
			ROM = relog(value),     # Ln Response Ratio
			OR  = relog(value),     # Log Odds Ratio
			RD  = no.change(value), # Rate Difference
			RR  = relog(value),     # Log Relative Rate
			ZCOR = rtoz(value),     # Fisher's Z-transform
			GEN  = no.change(value) # generic effect 
	)
	trans.scale.val
}

trans.to.raw <- function(metric, source.data, conf.level) {
	# transforms data given in source.data dataframe and returns the result
	# in another dataframe
	#
	# Source data consists of an effect size and variance:
	#    source.data = data.frame(yi=c(...), vi=c(...))
	# The return value consists of effect size, lower bound, upper_bound:
	#    return value: data.frame(yi=c(...), lb=c(...), ub=c(...))
	# metric is given as the trans-metric name (like escalc expects):
	#    SMD, ROM, OR, RD, RR, ZCOR, GEN
	
	alpha <- 1.0-(conf.level/100.0)
	mult <- abs(qnorm(alpha/2.0))
	
	yi.source <- source.data$yi
	vi.source <- source.data$vi
	
	no.change <- function() {
		# just takes the yi and vi and gives back the yi, lb, and ub
		
		yi <- yi.source
		addend = sqrt(vi.source)*mult
		lb <- yi.source - addend
		ub <- yi.source + addend
		
		return(data.frame(yi=yi,lb=lb,ub=ub))
	}
	
	unlog <- function() {
		return(exp(no.change()))
	}
	
	ztor <-function() {
		input <- no.change()
		output <- data.frame(yi=transf.ztor(input$yi),
				            lb=transf.ztor(input$lb),
						    ub=transf.ztor(input$ub),)
		return(output)
	}
	
	switch(metric,
			SMD = no.change(), # Hedges d
			ROM = unlog(),     # Ln Response Ratio
			OR  = unlog(),     # Log Odds Ratio
			RD  = no.change(), # Rate Difference
			RR  = unlog(),     # Log Relative Rate
			ZCOR = ztor(),      # Fisher's Z-transform
			GEN = no.change()
			)
}

raw.to.trans <- function(metric, source.data, conf.level) {
	# transforms data given in source.data dataframe and returns the result
	# in another dataframe
	#
	# Source data consists of effect size, upper bound, lower bound
	# The return value consists of effect size, variance (yi,vi)
	#
	# metric is given as the trans-metric name (like escalc expects)
	
	alpha <- 1.0-(conf.level/100.0)
	mult <- abs(qnorm(alpha/2.0))
	
	yi.source <- source.data$yi
	lb.source <- source.data$lb
	ub.source <- source.data$ub
	
	get.yi.vi <- function(yi,lb,ub) {
		# just takes the yi,lb,ub and gives the yi, and vi
		vi <- ((ub-yi)/mult)^2
		vi <- ifelse(is.na(vi), ((ub-yi)/mult)^2, vi)
		vi <- ifelse(is.na(vi), ((ub-lb)/(2*mult))^2, vi)
		
		return(data.frame(yi=yi,vi=vi))
	}
	
	no.change <- function() {
		return(get.yi.vi(yi.source, lb.source, ub.source))
	}
	
	relog <- function() {
		yi <- log(yi.source)
		lb <- log(lb.source)
		ub <- log(ub.source)
		
		return(get.yi.vi(yi, lb, ub))
	}
	
	rtoz <-function() {
		yi <- transf.rtoz(yi.source)
		lb <- transf.rtoz(lb.source)
		ub <- transf.rtoz(ub.source)
		
		return(get.yi.vi(yi,lb,ub))
	}
	
	switch(metric,
			SMD = no.change(), # Hedges d
			ROM = relog(),     # Ln Response Ratio
			OR  = relog(),     # Log Odds Ratio
			RD  = no.change(), # Rate Difference
			RR  = relog(),     # Log Relative Rate
			ZCOR = rtoz(),     # Fisher's Z-transform
			GEN  = no.change() # generic effect 
	)
}