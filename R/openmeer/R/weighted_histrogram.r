################################################################################
# Weighted histogram for meta-analysis
#
#	Requires the following packages to be installed:
#		splines, survival, ggplot2, RColorBrewer, Hmisc
#
#	Arguments:
#		args: list containing the following keys:
#			data: dataframe containing:
#				yi: effect sizes
#				vi: variances
#
#	Based on code by Fred Oswald:
#		Please cite as:
#		Oswald, F. L., & Ercan, S. (2013). Illustrating heterogeneity in meta-analysis
#		using a new-yet-simple plot. Presented at the Society for Research Synthesis Methods, Boston, MA.
################################################################################
weighted.histogram <- function (data) {
	# Make and save plot data
	base.path <- default.plot.path()
	plot.data <- data
	plot.data.path <- paste0(base.path,".plotdata")
	save(plot.data, file=plot.data.path)
	#print(paste0("Saved plot data to: ",getwd(),plot.data.path))

	plot.results <- weighted.histogram.plot(plot.data=data, base.path=base.path, image.format="png")
	results <- list(
		images=c("Weighted Histogram of Correlations"=plot.results[['images']][[1]]),
		plot.data.paths=c("Weighted Histogram of Correlations"=plot.data.path),
		save.plot.function=c("Weighted Histogram of Correlations"="weighted.histogram.plot"),
		References=paste(
			"Oswald, F. L., & Ercan, S. (2013). Illustrating heterogeneity in meta-analysis",
			"using a new-yet-simple plot. Presented at the Society for Research Synthesis Methods, Boston, MA.",
			sep='\n')
	)
}

################################################################################
# Weighted Histogram plot.
#
#	Writes out a histogram plot to a png or pdf file.
#
#	Required arguments:
#		args: list containing the following keys:
#			plot.data: list with keys:
#				data: dataframe containing:
#					yi: effect sizes
#					vi: variances
#			base.path - base path containing location to save the plot and plot
#				data e.g. '\Users\yourusername\myimage'
#			image.format
#	Returns:
#		list containing the follows keys:
#			images - vector of image paths
################################################################################
weighted.histogram.plot <- function (plot.data, base.path, image.format) {
	data <- plot.data

	# set image format and begin plotting
	if (image.format == 'png') {
		image.path = paste0(base.path,'.png')
		#png(file=image.path, width=10, height=10, units='in', res=72)
		png(file=image.path, width=600, height=600)
	} else if (image.format == 'pdf') {
		image.path = paste0(base.path,'.pdf')
		pdf(file=image.path)
	} else {
		stop(sprintf("%s is not a supported image format", image.format))
	}

	# compute weighted medians (these can be adjusted by changing values on 'probs' below,
	# along with corresponding labels)
	wquant <- wtd.quantile(data$yi, weights=data$vi, probs=c(.25, .50, .75), normwt=TRUE)
	xlab <- paste("vertical lines: wt 25%ile =", as.character(round(wquant[1],3)),
	", wt median =", as.character(round(wquant[2],3)),
	", wt 75% =", as.character(round(wquant[3],3)))

	# create 5 categories of shading
	a <- cut(data$vi,5)
	# use the Blues palette (see Color Brewer for other pallettes)
	fills <- rev(brewer.pal(7, 'Blues'))[1:5]
	mg <- qplot(data$yi, data = data, geom = "histogram", fill=a, main="Weighted Histogram of Correlations\n")
	myplot <- mg +
	scale_x_continuous(breaks=seq(-1,1,.1)) + scale_y_continuous(breaks=seq(0,100,1), minor_breaks=NULL) +
	geom_vline(xintercept = wquant[1]) + geom_vline(xintercept = wquant[2], size=1) + geom_vline(xintercept = wquant[3]) +
	labs(x=xlab, y="frequency", fill="sampling error variance") +
	scale_fill_manual(values=fills) + theme(plot.title = element_text(size = rel(1.5)))

	# end plotting
	print(myplot)
	dev.off()

	return(list(
		images = c(image.path)
	))
}
