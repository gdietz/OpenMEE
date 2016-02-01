library(openmeer)

context("Histogram")

data <- c(94, 98, 98, 94, 98, 96)
params <- list(GRADIENT=FALSE, xlab="tx A mean", color="#000000", fill="#FFFFFF")
plot.type = "HISTOGRAM"

if (!dir.exists("r_tmp")) {
  dir.create("r_tmp")
}

test_that("Histogram is generated", {
  results <- exploratory.plotter(data, params, plot.type)
  image.path <- results$images[["Histogram"]]

  expect_true("images" %in% names(results))
  expect_true(file.exists(image.path))
})
