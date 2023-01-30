#"""
#Working heatmap using tidyHeatmap and dplyr
#takes input csv in following format
#Sample  Peptide Value   HLA     Tissue
#s1      AA         1   A3      Melanoma
#s2      CCC        1   A11     EBV-BLCL
#s3      DDDD       0   other   Healthy B cells
#"""

library(tidyHeatmap)
library(dplyr)

df <- read.csv('long_matrix_forR.csv')
df2 = select(df, -1) #delete X col

#rename columns
df2 <- df2 %>% rename("Phosphopeptide detected" = "value")
df2 <- df2 %>% rename("Tissue" = "tissue")
plotdf <- as_tibble(df2) #tibble is df for dplyr

#drop samples that are wasting space due to irrelevant tissue or HLA type
# ex. drop Uterus tumor bc OVXW-1P is not A3/A11
#  drop TIL also bc TIL1 and TIL3 are not A3/A11
plotdf <- plotdf %>% filter(!`Tissue` == 'Uterus tumor')
plotdf <- plotdf %>% filter(!`Tissue` == 'TIL')
plotdf <- plotdf %>% filter(!`Tissue` == 'Cecal adenocarcinoma')
plotdf <- plotdf %>% filter(!`Tissue` == 'Breast cancer')
plotdf <- plotdf %>% filter(!`Tissue` == 'Breast ductal carcinoma')
plotdf <- plotdf %>% filter(!`Tissue` == 'Hepatocellular carcinoma')
plotdf <- plotdf %>% filter(!`Tissue` == 'Colorectal carcinoma')

colors = structure(1:2, names = c("0", "1"))

pp_heatmap <-
  plotdf %>% 
    heatmap(sample, peptide, .value = `Phosphopeptide detected`, 
            show_column_names = FALSE,
            col = colors,
            column_title = 'HLA-A3/A11 exclusive phosphopeptides',
            row_title = "",
            show_row_dend = FALSE) %>%
    add_tile(HLA, palette = c("#EFF5F5", "#FFFBC1", "#FEBE8C", "#F7A4A4") ) %>%
    add_tile(`Tissue`,
             palette = c("#522c5f",
                         "#81d358",
                         "#9a3eca",
                         "#d1bc51",
                         "#6760c5",
                         "#ce5e30",
                         "#84cbb1",
                         "#cf5ea7",
                         "#5d753b",
                         "#ab3e4c",
                         "#8d9dc7",
                         "#463d39",
                         "#c79986")
             )

save_pdf(pp_heatmap, "hmap.pdf", width=10, height=8, units="in")
