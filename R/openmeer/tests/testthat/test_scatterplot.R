library(openmeer)

context("Scatterplot")

data <- data.frame(y=c(20, 22, 26, 17, 22, 22), x = c(94, 98, 98, 94, 98, 96));
params <- list(xlab="tx A mean", ylab="tx B SD")
plot.type = "SCATTERPLOT"

if (!dir.exists("r_tmp")) {
  dir.create("r_tmp")
}

test_that("Scatterplot is generated", {
  results <- exploratory.plotter(data, params, plot.type)
  image.path <- results$images[["Scatterplot"]]

  expect_true("images" %in% names(results))
  expect_true(file.exists(image.path))
})
