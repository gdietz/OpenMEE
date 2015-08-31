################################################################################
# Default plot path
#
#	Get the default path for drawing plots based on the system time.
################################################################################
default.plot.path <- function () {
	out.path <- paste0("r_tmp/", as.character(as.numeric(Sys.time())))
	return(out.path)
}