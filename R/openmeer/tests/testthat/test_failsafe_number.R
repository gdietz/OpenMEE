library(openmeer)

context("Fail-safe number")

data <- data.frame(
  yi=c(
    -0.0945241585203,
    -0.277355866266,
    -0.366544429516,
    -0.664385099891,
    -0.461806281288,
    -0.185164437399),
  vi=c(
    0.0333705617356,
    0.0310651010637,
    0.0508397176176,
    0.0105517594512,
    0.0433446698087,
    0.0236302525555)
)

if (!dir.exists("r_tmp")) {
  dir.create("r_tmp")
}

test_that("Fail-safe number", {
  results <- failsafe.wrapper(data, digits=4, alpha=0.05, type="Rosenthal")

  expect_true("Summary" %in% names(results))
  expect_true("res" %in% names(results))
})
