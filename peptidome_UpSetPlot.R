###
# Generate upset plot using ggupset of sample peptidomes
# takes longform csv of peptide sequences and their associated sample

# Example input csv with relevant columns:
## peptide,Modification Type(s),start pos,Score,Delta,dMod,logP,unique count,Protein Name,original,phosphopeptide,length,Uniprot,HGNC,PID,class,sample
## RTMSEAALVRK,"M[+16], S[+80]",184.0,590.07,439.88,83.93,6.79,6.0,>sp|Q6ZTQ3|RASF6_HUMAN Ras association domain-containing protein 6 OS=Homo sapiens (Human) OX=9606 GN=RASSF6 PE=1 SV=1,Y.RTM[+15.995]S[+79.966]EAALVRK.R,True,11,Q6ZTQ3,RASSF6,FiatLCL_WT_classI,class I,JD LCL
## ATASPPRQK,S[+80],1176.0,388.63,190.06,190.06,4.06,4.0,>sp|Q9UQ35|SRRM2_HUMAN Serine/arginine repetitive matrix protein 2 OS=Homo sapiens (Human) OX=9606 GN=SRRM2 PE=1 SV=2,D.ATAS[+79.966]PPRQK.D,True,9,Q9UQ35,SRRM2,FiatLCL_WT_classI,class I,JD LCL
## SVSSPVKSK,S[+80],53.0,670.44,238.77,116.32,7.88,9.0,>sp|Q8IWI9|MGAP_HUMAN MAX gene-associated protein OS=Homo sapiens (Human) OX=9606 GN=MGA PE=1 SV=4,S.SVSS[+79.966]PVKSK.G,True,9,Q8IWI9,MGA,FiatLCL_WT_classI,class I,JD LCL
## RSPSPAPEK,S[+80],208.0,678.82,294.92,154.48,8.32,5.0,>sp|Q8IYB3|SRRM1_HUMAN Serine/arginine repetitive matrix protein 1 OS=Homo sapiens (Human) OX=9606 GN=SRRM1 PE=1 SV=2,S.RSPS[+79.966]PAPEK.K,True,9,Q8IYB3,SRRM1,FiatLCL_WT_classI,class I,JD LCL

###

library(ggupset)
library(tidyverse, warn.conflicts = FALSE)
library(ggplot2)

df <- read.csv('peptidome_df_for_R.csv')
df <- tibble(df)

# For each peptide, make a col. that lists which samples it's in

plot <- df %>%
  group_by(peptide) %>%
  summarize(samples = list(sample)) %>%
  ggplot(aes(x = samples)) +
    geom_bar() +
    geom_text(stat='count', aes(label=after_stat(count)), vjust=-1)+
    scale_x_upset(order_by="degree") +
    scale_y_continuous(limits=c(0,55) )

ggsave("upset.pdf", plot,
       device="pdf", width=6, height=4.5, dpi=300)
ggsave("upset.eps", plot,
       device="eps", width=6, height=4.5, dpi=300)
