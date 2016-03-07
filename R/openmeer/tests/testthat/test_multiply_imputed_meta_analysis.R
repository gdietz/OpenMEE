library(openmeer)

context("Multiply-Imputed Meta-Analysis")

# prepare data
mice.source.df <- data.frame(
  STATE = c(NA, "MA", "MA", NA, "RI", "RI"),
  tx.A.N = c(60L, 65L, 40L, 200L, 50L, 85L),
  tx.B.N = c(60L, 65L, 40L, 200L, 45L, 85L)
)

impute.results <- impute(
  m=5,
  maxit=5,
  data=mice.source.df,
  defaultMethod=c("pmm","logreg","polyreg","polr")
)

imputations <- impute.results$imputations

original.dataset <- data.frame(
  yi = c(
    -0.09452415852033,
    -0.277355866265512,
    -0.366544429515919,
    -0.664385099891136,
    -0.461806281287715,
    -0.185164437399104
  ),
  STATE = c(NA, "MA", "MA", NA, "RI", "RI"),
  tx.A.N = c(60, 65, 40, 200, 50, 85),
  vi = c(
    0.0333705617355999,
    0.0310651010636611,
    0.0508397176175572,
    0.0105517594511967,
    0.0433446698087316,
    0.0236302525555215
  ),
  slab = c(
    "Carroll, 1997",
    "Grant, 1981",
    "Peck, 1987",
    "Donat, 2003",
    "Stewart, 1990",
    "Young, 1995"
  ),
  tx.B.N = c(60, 65, 40, 200, 45, 85)
)

imputed.datasets <- combine.imputations.with.dataset(
  original.dataset,
  imputations
)

params <- list(
  digits = 3L,
  knha = FALSE,
  method = "REML",
  level = 95
)

mods <- list(
  interactions = list(),
  numeric = c("tx.A.N", "tx.B.N"),
  categorical = "STATE"
)

test_that("Multiply-Imputed Meta-Analysis Runs", {
  results <- multiply.imputed.meta.analysis(
    imputed.datasets=imputed.datasets,
    mods=mods,
    rma.args=params
  )
  expect_true("Summary" %in% names(results))
})
