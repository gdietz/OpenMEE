# OpenMEE specific analysis definitions to help in generating wizards
# automatically

get.data.exploration.analyses <- function () {
	# Maybe in future do introspection via lsf.str() but for now just explicitly list definitions

	list(
		ORDER = c('WEIGHTED.HISTOGRAM'),
		WEIGHTED.HISTOGRAM=list(
			ACTIONTEXT = 'Weighted Histogram', # for the menu option in OpenMEE
			MAIN = 'weighted.histogram',
			WIZARD.WINDOW.TITLE = 'Weighted Histogram',
			WIZARD.PAGES = list(
				DATALOCATION = list(SHOW.RAW.DATA=FALSE),
				REFINESTUDIES = list(),
				SUMMARY = list()
			)

		)
	)
}