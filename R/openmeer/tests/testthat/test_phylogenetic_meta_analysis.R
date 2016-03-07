library(openmeer)

context("Phylogenetic Meta-Analysis")


# phylo tree
phylo.tree.path = file.path(getwd(),"test_phylo_tree.txt")

if (!dir.exists("r_tmp")) {
  dir.create("r_tmp")
}

# prepare data
tmp_obj <- data.frame(
  yi = c(0.5, 0.2, 0.2, 0.1, 0.8, 0.9, 1),
  vi = c(0.2, 0.1, 0.4, 0.8, 0.9, 0.2, 0.1),
  slab = c(
    "study 1",
    "study 2",
    "study 3",
    "study 4",
    "study 5",
    "study 6",
    "study 7"
  ),
  species = c("A", "A", "B", "C", "D", "E", "E")
)

plot.params <- data.frame(
  digits       = 4L,
  fp_outpath   = structure(1L, .Label = "./r_tmp/forest.png", class = "factor"),
  fp_col2_str  = structure(1L, .Label = "[default]", class = "factor"),
  fp_col3_str  = structure(1L, .Label = "Ev/Trt", class = "factor"),
  fp_col4_str  = structure(1L, .Label = "Ev/Ctrl", class = "factor"),
  fp_xticks    = structure(1L, .Label = "[default]", class = "factor"),
  fp_show_col4 = TRUE,
  fp_show_col3 = TRUE,
  fp_xlabel    = structure(1L, .Label = "[default]", class = "factor"),
  fp_show_col1 = TRUE,
  fp_show_col2 = TRUE,
  fp_show_summary_line = TRUE,
  fp_plot_ub  = structure(1L, .Label = "[default]", class = "factor"),
  fp_col1_str = structure(1L, .Label = "Studies", class = "factor"),
  measure     = structure(1L, .Label = "OR", class = "factor"),
  fp_plot_lb  = structure(1L, .Label = "[default]", class = "factor")
)

test_that("Phylogenetic Meta-Analysis Runs", {
  results <- phylo.meta.analysis(
    treepath=phylo.tree.path,
    treeformat="newick",
    evo.model="BM",
    data=tmp_obj,
    method="ML",
    level=95.0,
    digits=4,
    btt=NULL,
    lambda=1.0,
    alpha=1.0,
    include.species=TRUE,
    plot.params=plot.params
  )

  forest.plot.path <- results[['images']][['Forest Plot__phylo']]

  expect_true(file.exists(forest.plot.path))
  expect_true("Summary" %in% names(results))
})
