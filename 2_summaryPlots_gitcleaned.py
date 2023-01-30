"""
Generate summary statistics plots in .png and .eps format:
-unique peptides per sample (hue = phos, nonphos) x (class I, II)
-length dist of unique peptides across all samples (phos, nonphos) x (class I, II)
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pal = sns.color_palette(['#F5B8AB', '#F5DDB0', '#DB9DF4', '#ABF5D9', '#A6C8F5'])
sns.set(palette=pal, style='ticks', context='notebook')

df = pd.read_pickle('1_parsedDF.pkl') #longform cleaned DF output by 1_ParseAndFilter.py
plotdf = df.drop_duplicates(['PID', 'peptide', 'phosphopeptide']) #remove dupe peptides

## peptide count plots
f, axs  = plt.subplots(1, 2, figsize=(10,6))

plotorder1 = plotdf[plotdf['class'] == 'class I']['sample'].value_counts(ascending=True).index
plotorder2 = plotdf[plotdf['phosphopeptide'] == True]['sample'].value_counts(ascending=True).index

sns.countplot(x='sample', hue='class', data=plotdf[plotdf['phosphopeptide'] == False], ax=axs[0], edgecolor='k', order=plotorder1)
sns.countplot(x='sample', hue='class', data=plotdf[plotdf['phosphopeptide'] == True], ax=axs[1], edgecolor='k', order=plotorder2)
axs[0].set_title('Nonphosphopeptides')
axs[1].set_title('Phosphopeptides')
axs[0].set_ylabel('unique peptide count')
axs[1].set_ylabel('')

xtl1 = axs[0].get_xticklabels()
axs[0].set_xticklabels(xtl1, rotation=90)
xtl2 = axs[1].get_xticklabels()
axs[1].set_xticklabels(xtl2, rotation=90)

axs[1].legend(loc='upper left')
axs[0].legend(loc='upper left')

sns.despine()
plt.tight_layout()

savdir = 'summaryPlots/'
plt.savefig(savdir+'countplot.png', dpi=300)
plt.savefig(savdir+'countplot.eps', format='eps')
plt.clf()

f, axs  = plt.subplots(1, 2, figsize=(10,4))

## lenght dist plots
lengthdf = df.drop_duplicates(['peptide', 'phosphopeptide']) #looking at all peptides in aggregate

sns.countplot(x='length', hue='class', data=lengthdf[lengthdf['phosphopeptide'] == False], ax=axs[0], edgecolor='k')
sns.countplot(x='length', hue='class', data=lengthdf[lengthdf['phosphopeptide'] == True], ax=axs[1], edgecolor='k')
axs[0].set_title('Nonphosphopeptides')
axs[1].set_title('Phosphopeptides')
axs[0].set_ylabel('unique peptide count')
axs[1].set_ylabel('')
axs[1].legend(loc='upper right')
axs[0].legend(loc='upper right')
axs[0].set_xlabel('peptide length')
axs[1].set_xlabel('peptide length')

sns.despine()
plt.tight_layout()
plt.savefig(savdir+'lengthdist.png', dpi=300)
plt.savefig(savdir+'lengthdist.eps', format='eps')
