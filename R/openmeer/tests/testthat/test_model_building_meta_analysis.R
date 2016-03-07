library(openmeer)

context("Model-Building Meta-Analysis")

# prepare data
tmp_obj <- data.frame(
  yi = c(
    -0.09452415852033,
    -0.277355866265512,
    -0.366544429515919,
    -0.664385099891136,
    -0.461806281287715,
    -0.185164437399104
  ),
  vi = c(
    0.0333705617355999,
    0.0310651010636611,
    0.0508397176175572,
    0.0105517594511967,
    0.0433446698087316,
    0.0236302525555215
  ),
  STATE = c("MA", "MA", "MA", "RI", "RI", "RI"),
  slab = c(
    "Carroll, 1997",
    "Grant, 1981",
    "Peck, 1987",
    "Donat, 2003",
    "Stewart, 1990",
    "Young, 1995"
  ),
  tx.A.N = c(60, 65, 40, 200, 50, 85)
)

test_that("Model-Building Meta-Analysis Runs", {
  results <- model.building(
    data = tmp_obj,
    full.mods = list(
      interactions = list("STATE:tx.A.N" = c("STATE", "tx A N")),
      numeric = "tx.A.N",
      categorical = "STATE"
    ),
    reduced.mods = list(
      interactions = list(),
      numeric = "tx.A.N",
      categorical = "STATE"
    ),
    method = "REML",
    level = 95.0,
    digits = 4
  )

  expect_true("Summary" %in% names(results))
})
