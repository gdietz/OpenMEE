# test interaction with rma.uni

library(metafor)

data(dat.bcg)

# add a bunch of fake studies
add.random.rows <- function() {
	for (i in 1:1000) {
		dat.bcg<-rbind(dat.bcg, c("99","nobody",1999,sample(600,1),sample(60000,1),sample(500,1),sample(60,1),sample(60,1),sample(c("alloc","systematic","random"),1)))
		dat.bcg$country <- sample(c("USA","RUSSIA","MEXICO"),size=nrow(dat.bcg), replace=TRUE)
		
		if (i%%1000 == 0) {
			cat(i)
		}
	}
	dat.bcg$tpos <- as.numeric(dat.bcg$tpos)
	dat.bcg$tneg <- as.numeric(dat.bcg$tneg)
	dat.bcg$cpos <- as.numeric(dat.bcg$cpos)
	dat.bcg$cneg <- as.numeric(dat.bcg$cneg)
	
	dat.bcg[dat$alloc=="alternate"] <- "alloc"
	
	dat.bcg <<- dat.bcg
}

add.random.rows()
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)
rma(yi, vi, mods = ~ factor(alloc)*factor(country), data=dat, method="REML", btt=c(2,3))

