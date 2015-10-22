make.histogram <- function(plot.path, data, params) {
	# make actual plot 
	if (length(grep(".png", plot.path)) != 0) {
		png(file=plot.path, width=600, height=600)
	}
	else{
		pdf(file=plot.path) # the pdf device seems to not like setting height and width, width=600, height=600)
	}
	
	qplot_param_keys = c("xlab","ylab","xlim", "ylim", "binwidth")
	geom_histogram_keys = c("binwidth")
	geom_bar_keys = c("binwidth", "fill","color")
	# 'count_key_name': is not the actual name of the parameter,
	#           the parameter appears to be just the first positional argument
	# 'low','high': can be the name of a color or rgb e.g. "#132B43"
	scale_fill_gradient_keys = c("name","low","high")
	
	# parse params
	qplot_params <- list()
	geom_histogram_params <- list()
	geom_bar_params <- list()
	scale_fill_gradient_params <- list()
	for (p in names(params)) {
		if (p %in% qplot_param_keys) {
			qplot_params[[p]] <- params[[p]]
		}
		if (p %in% geom_histogram_keys) {
			geom_histogram_params[[p]] <- params[[p]]
		}
		if (p %in% geom_bar_keys) {
			geom_bar_params[[p]] <- params[[p]]
		}
		if (p %in% scale_fill_gradient_keys) {
			scale_fill_gradient_params[[p]] <- params[[p]]
		}
	}
	
	if (params[['GRADIENT']]) {
		params.for.qplot <- c(list(data), qplot_params)
		myplot <- do.call(qplot, params.for.qplot) + geom_histogram(aes(fill = ..count..)) + do.call(scale_fill_gradient, scale_fill_gradient_params)			                             
	} else { # gradient
		# no gradient
		myplot <- do.call(qplot, c(list(data), qplot_params)) + do.call(geom_bar, geom_bar_params)
	}
	
	print(myplot)
	graphics.off()
}