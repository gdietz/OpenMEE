validate.tree <- function(tree) {
	# error checking for phylogenetic tree
	
	if (!is.ultrametric(tree)) {
		stop("Your tree is not ultrametric, it may not fit a BM model of evolution.")
	}
	
	speciesDuplicates <- data.frame(table(tree$tip.label))
	if(nrow(speciesDuplicates[speciesDuplicates[,2]>1,]) > 0) {
		stop("Sorry, there are dublicate species names in the tree, please provide unique names for each duplicate.")
	}
		
}

#phylo.wrapper <- function(data, method, level, digits, mods.str="~ 1", btt=NULL) {
#	# Construct call to rma
#	call_str <- sprintf("rma.uni(yi,vi, mods=%s, data=data, method=\"%s\", level=%f, digits=%d)", mods.str, method, level, digits)
#	#cat(call_str,"\n")
#	expr<-parse(text=call_str) # convert to expression
#	res <- eval(expr) # evaluate expression
#	res
#}

phylo.meta.analysis <- function(tree, evo.model, 
                                data, method, level, digits, plot.params, metric,
								btt=NULL,
                                lambda=1.0, alpha=1.0, include.species=TRUE) {
	# data: should be a dataframe of the type that metafor likes ie
	#   yi and vi for the effect and variance columns
	#   slab holds study names
	#   the parts that are 'factors' have already been made in to factors with
	#   the appropriate reference values
	#   should include 'species' column 
	# evo.model: "BM" or "OU" # evolutionary model
	# include.species: TRUE or FALSE, include species as random factor if possible 
	
	# blankDataFrame used to extract correlation matrix
	blankDataFrame <- data.frame(tree$tip.label)
	rownames(blankDataFrame) <- tree$tip.label
	
	if(evo.model == "BM") {
		M <- corPagel(value = lambda, phy = tree, fixed=TRUE) # ape function to define model
	} else { # model is "OU"
		M <- corMartins(value = alpha, phy = tree, fixed=TRUE) # ape function to define model
	}
	C <- corMatrix(Initialize(M, blankDataFrame)) # nlme function corMatrix to extract correlation matrix from model
	
	######## end of constructing phylogenetic correlation matrix for rma.mv #########
	
	# additional columns needed for rma.mv
	betweenStudyVariance <- rep(1:nrow(data)) # used to initialize a random-effects meta-analysis
	phylogenyVariance <- data$species # used to initialize phylogeny as a random-factor in analyses
	
	if (include.species) {
		unique.species <- unique(data$species)
		if (length(unique.species) == length(data$species)) {
			stop("All species are unique, no good")
		}
		## random-effects meta-analysis including species and phylogeny as random factors (phylogenetic meta-analysis with a random-effects model), 
		## here 'species' is included as a random factor because we have multiple replicates within species (e.g., two A's)
		#res <- rma.mv(yi, vi, data=data, random = list(~ 1 | betweenStudyVariance, ~ 1 | data$species, ~ 1 | phylogenyVariance), R=list(phylogenyVariance=C)) 
		res <- rma.mv(yi, vi, data = data, random = list(~1 | betweenStudyVariance, ~1 | species , ~1 | phylogenyVariance), R = list(phylogenyVariance = C))
	} else {
		# include phylogeny as a random factor
		res <- rma.mv(data$yi, data$vi, data=data, random = list(~ 1 | phylogenyVariance), R=list(phylogenyVariance=C))
	}

	# generate forest plot
	paths = regenerate_phylo_forest_plot(
			     plot.params=plot.params,
			     data=data,
				 res=res,
				 level=level,
				 params.out.path=NULL, out.path=NULL)
	forest.path <- paths[["img.path"]]
	forest.plot.params.path <- paths[["params.path"]] 

#	# Now we package the results in a dictionary (technically, a named 
#	# vector). In particular, there are two fields that must be returned; 
#	# a dictionary of images (mapping titles to image paths) and a list of texts
#	# (mapping titles to pretty-printed text). In this case we have only one 
#	# of each. 
	plot.params.paths <- c("Forest Plot__phylo"=forest.plot.params.path)
	images <- c("Forest Plot__phylo"=forest.path)
	plot.names <- c("forest plot"="forest_plot")
	
	results <- list("images"=images,
			"Summary"=paste(capture.output(res), collapse="\n"), # convert print output to a string
			"plot_names"=plot.names,
			"plot_params_paths"=plot.params.paths,
			"res"=res,
			"res.info"=rma.mv.value.info())
}

regenerate_phylo_forest_plot <- function(plot.params, data, res, level, params.out.path=NULL, out.path=NULL) {
	#### Set confidence level, then unset it later on.
	old.global.conf.level <- get.global.conf.level(NA.if.missing=TRUE)
	set.global.conf.level(level)
	                                                                     ##
	if (is.null(out.path)) {
		forest.path <- paste(plot.params$fp_outpath, sep="")
	} else {
		forest.path <- paste(out.path, sep="")
	}
	
	plot.data <- create.phylogenetic.ma.plot.data(data, res, params=plot.params, conf.level=level)
	## dump the forest plot params to disk; return path to
	## this .Rdata for later use
	forest.plot.params.path <- save.plot.data.and.params(
			#plot.data=plot.data,
			data=data,
			params=plot.params,
			res=res,
			level=level,
			out.path=params.out.path)
	# Make the actual plot
	forest.plot(forest.data=plot.data, outpath=forest.path)
	
	##### Revert confidence level
	set.global.conf.level(old.global.conf.level)
	
	list("img.path"=forest.path,
		 "params.path"=forest.plot.params.path)
}

create.phylogenetic.ma.plot.data <- function (data, res, params, conf.level) {
# creates plot.data for forest.plot to make a forest plot with
# calculates plot sizes and layout
# outputs: forest.data is a list contains the following fields:
#
#   NOTE: last element of effect.disp, effects, label, types are for the 'overall' values found in res
#
# - effects.disp - list with 3 fields:
#     - y.disp - vector of effect sizes in display scale
#     - lb.disp - conf. int. lower bound in display scale
#     - ub.disp - conf. int. upper bound in display scale
#
# - effects - list with 3 fields:
#     - ES - vector of effect sizes in calc. scale
#     - LL - conf. int. lower bound in calc. scale
#     - UL - conf. int. upper bound in calc. scale
#
# - types - vector specifying row types:
#     - 0 - study-level data
#     - 1 - subgroup summary data
#     - 2 - overall summary data
#     - 3 - row of column labels
#     - 4 - blank row (e.g. for empty summary row in right-hand side of cumulative plot)
#     - 5 - overall summary data with unscaled diamond (e.g. for leave-one-out plots)
# 
# - label - vector of row labels of length 1 more than length of effect sizes.
#           First entry is usually "Studies" assuming first row has type 3.
#
# - scale - transformation scale - takes one of the following values:
#     - "standard" - untransformed
#     - "log"
#     - "logit"
#     - "arcsine" 
#
# - options - plot options
#
# - plot range - range of x-values in which to draw plot
#
	
	metric <- as.character(params$measure) # we need the metric for transformation/scaling issues
	
	#forest.data <- list(conf.level=conf.level)
	forest.data <- list()
	#alpha <- 1.0-(conf.level/100.0)
	#mult <- abs(qnorm(alpha/2.0))
	
	# Get yi and vi for overall result
	tmp <- data.frame(yi=res$b, lb=res$ci.lb, ub=res$ci.ub)
	# calling raw.to.trans with metric="GEN" just gives the yi and vi for a given yi and conf.interval
	overall.yi.and.vi <- raw.to.trans(metric="GEN", source.data=tmp, conf.level=conf.level) 
	
	### Make effects.disp sublist. Note: 'raw' is 'display' scale
	effects.disp <- list()
	raw.scale <- trans.to.raw(metric, data, conf.level)
	overall.raw.scale <- trans.to.raw(metric, overall.yi.and.vi, conf.level)
	effects.disp$y.disp  <- c(raw.scale$yi, overall.raw.scale$yi)
	effects.disp$lb.disp <- c(raw.scale$lb, overall.raw.scale$lb)
	effects.disp$ub.disp <- c(raw.scale$ub, overall.raw.scale$ub)
	# attach to forest.data
	forest.data$effects.disp <- effects.disp 
	
	### Make effects sublist
	effects <- list()
	# calling trans.to.raw with metric="GEN" just gets the yi, lb, and ub for a given effect size and variance
	calc.scale <- trans.to.raw(metric="GEN",data, conf.level)
	overall.calc.scale <- trans.to.raw(metric="GEN", overall.yi.and.vi, conf.level)
	effects$ES <- c(calc.scale$yi, overall.calc.scale$yi)
	effects$LL <- c(calc.scale$lb, overall.calc.scale$lb)
	effects$UL <- c(calc.scale$ub, overall.calc.scale$ub)
	# attach to forest.data
	forest.data$effects <- effects
	
	### scale
	scale <- switch(metric,
			SMD = "standard", # Hedges d
			ROM = "log",     # Ln Response Ratio
			OR  = "log",     # Log Odds Ratio
			RD  = "standard", # Rate Difference
			RR  = "log",     # Log Relative Rate
			GEN  = "standard", # generic effect 
			"standard") ##ZCOR = rtoz(),     # Fisher's Z-transform
	# attach to forest.data
	forest.data$scale <- scale
	
	#### label
	"Overall (I^2=94% , P< 1e-06)"
	cutoff = 0.0001
	if (res$pval > cutoff) {
		pval.str <- paste("=", formatC(res$pval, digits = 4, format = "f")) 
	} else {
		pval.str <- paste0("< ", cutoff)
	}
	overall.str <- sprintf("Overall (P %s)", pval.str) # I^2 not in rma.mv ??
	label <- c(as.character(params$fp_col1_str),data$slab,overall.str)
	forest.data$label <- label # attach to forest.data
	
	### types
	nstudies <- nrow(data) # number of studies
	types <- c(3,rep(0,nstudies),2)
	forest.data$types <- types # attach types to forest.data
	

	
	######### Oy, using yucky code from before to set options #################
	plot.options <- set.plot.options(params)
	if (params$fp_plot_lb == "[default]") {
		plot.options$plot.lb <- params$fp_plot_lb
	} else {
		#plot.lb <- eval(parse(text=paste("c(", params$fp_plot_lb, ")", sep="")))
		####plot.options$plot.lb <- eval(call(transform.name, params$measure))$calc.scale(plot.lb, n)
		plot.lb <- as.numeric(as.character(params$fp_plot_lb))
		plot.options$plot.lb <- raw.scale.single.val.to.trans.scale(plot.lb, metric)
	} 
	
	if (params$fp_plot_ub == "[default]")  {
		plot.options$plot.ub <- params$fp_plot_ub
	} else {
		#plot.ub <- eval(parse(text=paste("c(", params$fp_plot_ub, ")", sep="")))
		if (scale == "logit") {
			plot.ub <- min(1, plot.ub)
		}  
		#plot.options$plot.ub <- eval(call(transform.name, params$measure))$calc.scale(plot.ub, n)
		plot.ub <- as.numeric(as.character(params$fp_plot_ub))
		plot.options$plot.ub <- raw.scale.single.val.to.trans.scale(plot.ub, metric)
	} 
	########################## end of yucky code ##############################
	
	
	
	### options
	forest.data$options <- plot.options
	
	### plot.range
	plot.range <- calc.plot.range(effects, plot.options)
	# Calculate a reasonable range for the x-values to display in plot.
	

#	if (scale=="log") {
#		# Plot range is in calc scale, so put back in display scale to update params.
#	
#		plot.range.disp.lower <- trans.scale.single.val.to.raw.scale(plot.range[1], metric)
#		plot.range.disp.upper <- trans.scale.single.val.to.raw.scale(plot.range[2], metric)
#	} else {
#		plot.range.disp.lower <- plot.range[1]
#		plot.range.disp.upper <- plot.range[2]
#	}
	forest.data$plot.range <- plot.range
	
	forest.data
}