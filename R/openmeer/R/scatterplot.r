make.scatterplot <- function(plot.path, mydata, params) {
	if (length(grep(".png", plot.path)) != 0){
		png(file=plot.path, width=600, height=600)
	}
	else{
		pdf(file=plot.path) # the pdf device seems to not like setting height and width, width=600, height=600)
	}

	if ('slab' %in% names(mydata)) {
		# rpy2 converts strvectors to Factors in dataframes by default
		mydata$slab <- as.character(mydata$slab)
	}

	tmp.data <<- mydata

	p <- ggplot(tmp.data, aes(x=x, y=y, label=tmp.data$slab, hjust=0, vjust=0)) + geom_point()
	# add on parameters
	if ('slab' %in% names(mydata)) {
		p <- p+geom_text()
	}
	if ('xlab' %in% names(params)) {
		p <- p + xlab(params$xlab)
	}
	if ('ylab' %in% names(params)) {
		p <- p + ylab(params$ylab)
    }
	if ('xlim' %in% names(params)) {
		p <- p + xlim(params$xlim)
	}
	if ('ylim' %in% names(params)) {
		p <- p + ylim(params$ylim)
	}

	print(p)

	graphics.off()
}
