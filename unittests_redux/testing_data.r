####
# datasets for OpenMEE unittests.
#
# these are (almost?) entirely reproduced from the
# very nice metafor documentation:
# http://www.metafor-project.org/doku.php/analyses
#
# each method below loads and returns a dataframe.
####

# contains helpful data
library(metafor)

###
# this is a binary dataset; specifically the
# BCG vaccine dataset (Colditz et al., 1994)
get.bcg <- function(){
    data(dat.bcg)
    print("loaded `bcg'; columns are: ")
    print(dat.bcg.names)
    # example of passing this to escalc:
    #   dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)
    dat.bcg
}

###
# mortality risks from Hine et al. 1989
# this is more 2x2 data.
get.hine89 <- function(){
    data(dat.hine1989)
    print("loaded `hine89'; columns are: ")
    print(dat.hine1989.names)
    dat.hine1989
}


###
# From Practical meta-analysis by Lipsey and Wilson (2001). 
# This is just basic point estimate/variance data.
#
# Call rma, e.g., as follows: 
#   res <- rma(yi, vi, data=dat, method="FE")
###
get.lipsey.wilson <- function{
    dat <- data.frame(
        id = c(100, 308, 1596, 2479, 9021, 9028, 161, 172, 537, 7049),
        yi = c(-0.33, 0.32, 0.39, 0.31, 0.17, 0.64, -0.33, 0.15, -0.02, 0.00),
        vi = c(0.084, 0.035, 0.017, 0.034, 0.072, 0.117, 0.102, 0.093, 0.012, 0.067),
        random = c(0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
        intensity = c(7, 3, 7, 5, 7, 7, 4, 4, 5, 6)
    )
    dat 
}