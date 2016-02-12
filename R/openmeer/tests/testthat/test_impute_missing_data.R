library(openmeer)

context("Data Exploration: Impute Missing Data")

# prepare data
mice.source.df <- data.frame(
  STATE = c(NA, 'MA', 'MA', 'RI', 'RI', 'RI'),
  tx.B.mean = c(92, 92, 88, 82, 88, 92)
)

test_that("Impute Missing Data with MICE", {
  results <- impute(
    m=5,
    maxit=5,
    data=mice.source.df,
    defaultMethod=c("pmm","logreg","polyreg","polr")
  )

  expect_true("Summary" %in% names(results))
  expect_true("imputations" %in% names(results))
})
