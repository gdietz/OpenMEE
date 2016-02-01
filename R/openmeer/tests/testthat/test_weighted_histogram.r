library(openmeer)

context("Weighted Histogram")

test.data.path = file.path(getwd(),"test_weighted_histogram_test_data.csv")
data <- read.csv(test.data.path) # a dataframe containing yi and vi

if (!dir.exists("r_tmp")) {
  dir.create("r_tmp")
}

test_that("Weighted Histogram plot is generated", {
  results <- weighted.histogram(data)
  image.path <- results$images[["Weighted Histogram of Correlations"]]

  expect_true("images" %in% names(results))
  expect_true(file.exists(image.path))
})

test_that("Saving histogram plot from plotdata works", {
  results <- weighted.histogram(data)
  plot.data.path <- results$plot.data.paths[["Weighted Histogram of Correlations"]]
  save.plot.fn.name <- results$save.plot.function[["Weighted Histogram of Correlations"]]
  load(plot.data.path)

  base.path <- file.path(getwd(),"r_tmp","saved_weighted_histogram")
  final.image.path <- paste0(base.path,".png")

  save.plot.results <- do.call(
    save.plot.fn.name, list(
      plot.data = plot.data,
      base.path = file.path("r_tmp","saved_weighted_histogram"),
      image.format = "png"
    )
  )
  expect_true(file.exists(final.image.path))
})
