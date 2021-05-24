renv::activate()
library(feather)

path_file <- "data/nhanes_merged_2018_06202020.Rdata"
nb_patient_sample <- 100  # Only for big data frames

name_loaded_file <- list(load(path_file))

print(names_loaded_file)