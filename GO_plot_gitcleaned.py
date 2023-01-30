"""
Plot enriched GO terms obtained from STRING-DB horizontally by -log(p-val)
"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

pal = sns.color_palette(['#F5B8AB', '#F5DDB0', '#DB9DF4', '#ABF5D9', '#A6C8F5'])
sns.set(palette=pal, style='ticks', context='notebook')

df = pd.read_csv('a3a11_pp_STRING_enrichment.Function.tsv', sep='\t') #.tsv file from STRING-DB

plotdf = df[['term description', 'false discovery rate']]
plotdf = plotdf[plotdf['false discovery rate'] <=1E-4]
plotdf['-log(FDR)'] = [np.log10(x)*-1 for x in plotdf['false discovery rate']]

sns.barplot(x='-log(FDR)', y='term description', data=plotdf, facecolor='#F5B8AB', edgecolor='k')
plt.xlabel('$-log_{10}(FDR)$')
plt.ylabel('')
sns.despine()
plt.tight_layout()
plt.savefig('a3a11_pp_GO_MolecularFunction.png', dpi=300)