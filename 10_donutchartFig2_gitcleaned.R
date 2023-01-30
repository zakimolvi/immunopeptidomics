###
# Make donut chart to visualize tissue representation in the dataset
###

library(ggplot2)
library(dplyr)
library(ggrepel)

#library(lessR)

ndf <- read.csv("metadata_for_R.csv")

df2 <- tibble(ndf)
df <- count(df2, tissue)

# Increase the value to make the hole bigger
# Decrease the value to make the hole smaller
hsize <- 4

df %>% mutate(x = hsize)

ggplot(df, aes(x = hsize, y = n, fill = tissue)) +
  geom_col(color = "black") +
  coord_polar(theta = "y") +
  scale_fill_manual(values = c("#462e5a",
                               "#76d751",
                               "#ba4ad5",
                               "#ced03c",
                               "#5c43b7",
                               "#c6cf7c",
                               "#be4d9d",
                               "#66d5a6",
                               "#cb4669",
                               "#52853d",
                               "#6c7fc4",
                               "#d4913c",
                               "#72b1c3",
                               "#cd4a2f",
                               "#395042",
                               "#c697bd",
                               "#806a33",
                               "#c1cab1",
                               "#65302f",
                               "#cc8977")
                    ) +
  xlim(c(0.2, hsize + 0.5)) +
  geom_text(aes(label = n),
            position = position_stack(vjust = 0.5)) +
  theme_void() +
  guides(fill = guide_legend(title = "Tissue"))