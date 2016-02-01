funnel.wrapper <- function(fname, data, params, ...) {
	# fname: the name of the function that would have been called if this were
	#        a regular meta-analysis
	# data: binary or continuous data object
	# params: parameters for function specified by fname
	# ... : parameters for funnel()


	# set data (avoid some annoying copy pasta, too many calories)
	binary.data <- data
	cont.data <- data

	# run meta-analysis
	res <- switch(fname,
                  binary.fixed.inv.var=rma.uni(yi=binary.data@y, sei=binary.data@SE, slab=binary.data@study.names,
						  level=params$conf.level, digits=params$digits, method="FE", add=c(params$adjust,params$adjust),
						  to=c(as.character(params$to), as.character(params$to))),
		  		  binary.random=rma.uni(yi=binary.data@y, sei=binary.data@SE,
						  slab=binary.data@study.names,
						  method=params$rm.method, level=params$conf.level,
						  digits=params$digits,
						  add=c(params$adjust,params$adjust),
						  to=as.character(params$to)),
	              continuous.fixed=rma.uni(yi=cont.data@y, sei=cont.data@SE,
	 		              slab=cont.data@study.names,
	 		              method="FE", level=params$conf.level,
	 		              digits=params$digits),
	              continuous.random = rma.uni(yi=cont.data@y, sei=cont.data@SE,
	 		              slab=cont.data@study.names,
	 		              method=params$rm.method, level=params$conf.level,
	 		              digits=params$digits)
		  		) # end of switch

	funnel.params <- list(...)
	funnel.plot.data.path <- save.funnel.data(res=res, funnel.params=funnel.params)

	# draw plot & save funnel data
	plot.path = paste(funnel.plot.data.path, ".png", sep="")
	make.funnel.plot(plot.path, res, funnel.params)

	results <- list(
		images=c("Funnel Plot"=plot.path),
		plot_params_paths=c("Funnel Plot"=funnel.plot.data.path),
		References="funnel plot reference placeholder"
	)
}

make.funnel.plot <- function(plot.path, res, funnel.params) {
	# make actual plot
	if (length(grep(".png", plot.path)) != 0){
		png(file=plot.path, width=600, height=600)
	}
	else{
		pdf(file=plot.path) # the pdf device seems to not like setting height and width, width=600, height=600)
	}

  #funnel(res, ...)
	do.call(funnel, c(list(res), funnel.params))

	graphics.off()
}

regenerate.funnel.plot <- function(out.path, plot.path, edited.funnel.params=NULL) {
	# Used when saving or editing the plot

	# out.path is the path to r_tmp/{timestamp}* or whatever

	# load res and funnel.params in to function workspace
	load(paste(out.path, ".res", sep=""))

	# load the stored funnel params when we are just saving, not editing
	if (is.null(edited.funnel.params)) {
		load(paste(out.path, ".funnel.params", sep=""))
	}
	else {
		funnel.params <- edited.funnel.params
		save.funnel.data(res, funnel.params, out.path=out.path)
	}

	make.funnel.plot(plot.path, res, funnel.params)
}

get.funnel.params <- function(out.path) {
	# accessor for python to load the stored funnel params
	load(paste(out.path, ".funnel.params", sep=""))
	funnel.params
}

save.funnel.data <- function(res, funnel.params, data=NULL, params=NULL, out.path=NULL) {
	# adapted from save.data() in utilities.r

	# save the data, result and plot parameters to a tmp file on disk
	if (is.null(out.path)){
		# by default, we use thecurrent system time as a 'unique enough' filename
		out.path <- paste("r_tmp/",
				as.character(as.numeric(Sys.time())), sep="")
	}

	#save(data, file=paste(out.path, ".data", sep=""))
	save(res, file=paste(out.path, ".res", sep=""))
	#save(params, file=paste(out.path, ".params", sep=""))
	save(funnel.params, file=paste(out.path, ".funnel.params", sep=""))
	out.path
}
