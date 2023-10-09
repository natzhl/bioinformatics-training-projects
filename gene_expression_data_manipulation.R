# script to manipulate and visualize gene expression data

# load libraries
library(dplyr)
library(tidyverse)
library(GEOquery)
library(tidyverse)
library(ggplot2)

# read the data
data <- read.table(file = 'C:/Users/Oleg/OneDrive/Документы/R/data manipulation/data/GSE228043_Camk2aTRAP_RPKM.txt')
dim(data)

# get metadata
gse <- getGEO(GEO = 'GSE228043', GSEMatrix = TRUE)
gse

metadata <- pData(phenoData(gse[[1]]))
head(metadata)

# chose columns for the analysis
metadata %>%
  select(1,8,9,11,12) %>%
  head()

metadata.modified <- metadata %>%
  select(1,8,9,11,12) %>%
  rename(tissue = source_name_ch1) %>%
  rename(cell_type = characteristics_ch1.1) %>%
  rename(genotype = characteristics_ch1.2) %>%
  rename(organism = organism_ch1) %>%
  mutate(cell_type = gsub('cell type: ', '', cell_type)) %>%
  mutate(genotype = gsub('genotype: ', '', genotype))

head(data)

# correct header in data
data.long <- data
colnames(data.long) <- c("GeneID", "GeneSymbol","389Input", "389Neg", "389Pos","391Input", "391Neg", "391Pos","392Input","392Neg", "392Pos", "396Input", "396Neg", "396Pos")
data.long = data.long[-1,]

# trasforming data
data.long <- data.long %>%
  gather(key = 'fraction', value = 'RPKM', -GeneID, -GeneSymbol)

# joining data frames
data.long <- data.long %>%
  left_join(., metadata.modified, by = c('fraction' = 'title')) 

# explore data
data.long$RPKM = as.numeric(as.character(data.long$RPKM)) 

data.long %>%
  filter(GeneSymbol == "Cldn2" | GeneSymbol == "Crb2") %>%
  group_by(fraction) %>%
  summarize(mean_RPKM = mean(RPKM),
            median_RPKM = median(RPKM))
