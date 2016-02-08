library(openmeer)

context("Standard Meta-Analysis")

# prepare data
tmp_obj <- new(
  'ContinuousData',
  N1=c(60, 65, 40, 200, 45, 85),
  mean1=c(92.0, 92.0, 88.0, 82.0, 88.0, 92.0),
  sd1=c(20.0, 22.0, 26.0, 17.0, 22.0, 22.0),
  N2=c(60, 65, 40, 200, 50, 85),
  mean2=c(94.0, 98.0, 98.0, 94.0, 98.0, 96.0),
  sd2=c(22.0, 21.0, 28.0, 19.0, 21.0, 21.0),
  y=c(
    -0.0945241585203,
    -0.277355866266,
    -0.366544429516,
    -0.664385099891,
    -0.461806281288,
    -0.185164437399
  ),
  SE=c(
    0.182676111563,
    0.176252946255,
    0.225476645393,
    0.102721757438,
    0.208193827499,
    0.153721347104
  ),
  study.names=c(
    "Carroll, 1997",
    "Grant, 1981",
    "Peck, 1987",
    "Donat, 2003",
    "Stewart, 1990",
    "Young, 1995"
  ),
  years=c(
    as.integer(),
    as.integer(),
    as.integer(),
    as.integer(),
    as.integer(),
    as.integer()),
  covariates=list()
)

params <- data.frame(
  conf.level = 95,
  digits = 3L,
  fp_col2_str = "[default]",
  fp_col3_str = "Ev/Trt",
  fp_col4_str = "Ev/Ctrl",
  fp_xticks = "[default]",
  fp_show_col4 = FALSE,
  fp_show_col3 = FALSE,
  fp_xlabel = "[default]",
  fp_show_col1 = TRUE,
  fp_show_col2 = TRUE,
  fp_outpath = "./r_tmp/forest.png",
  rm.method = "DL",
  fp_plot_ub = "[default]",
  fp_col1_str = "Studies",
  measure = "SMD",
  fp_plot_lb = "[default]",
  fp_show_summary_line = TRUE
)

test_that("Standard Meta-Analysis Runs (Continuous Random)", {
  set.global.conf.level(95)
  results <- continuous.random(tmp_obj, params)

  image.path <- results$images[["Forest Plot"]]
  expect_true(file.exists(image.path))
})
