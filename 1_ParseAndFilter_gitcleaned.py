"""
Script to:
1. Parse BYonic search results, filter for LogP >= 2 and dMod >= 20, format strings, remove <8mers, and reverse contaminants, remove intrasequence annotations from PTM mass shifts, demarcate phosphopeptides
2. Concatenate all filtered class I and II peptides into longform pandas dataframe
"""

import pandas as pd

def prepHLA(fname='HLAtypings.csv'):
    """
    create a dictionary of all the sample HLA typings
    return: HLA typing as query-able dictionary
    ex. sam_hla[PID] = [HLA typing as list]
    """
    import csv

    with open(fname, encoding='utf-8-sig') as csv_data:
        reader = csv.DictReader(csv_data)
        sam_hla = {}

        for row in reader:
            key = row['PID']
            val = row['HLA'].split(',')
            sam_hla[key] = val

    return sam_hla

def createDF(filename, sheetno, PID):
    """
    Creates dataframe for given sample, filters for Byonic logP>=2 & dMod >=20, remove decoys,
    remove modifications, remove <8mers, add class I, II annotations

    :param filename: input Excel file from RU PRC
    :param sheetno: integer sheet number
    :param PID: sample ID ex. 'AML14 DMSO'
    :return: filtered df
    """

    df = pd.read_excel(filename, sheet_name = sheetno)
    df = df.rename(index=str, columns=colDict)
    df = df[consCol]
    df = df[df['logP'] >= 2.00]
    df = df[df['dMod'] >= 20.00]
    df = df[~df['Protein Name'].str.contains('>Reverse')]

    # keep original peptide ID for locating phos
    df['original'] = df['peptide']

    # Remove irrelevant losses [+15.995] (ox) and [+42.011] (Ac) from all peptide sequences
    df['peptide'] = df['peptide'].str.replace('[+15.995]','',regex=False)
    df['peptide'] = df['peptide'].str.replace('[+42.011]','',regex=False)
    df['peptide'] = df['peptide'].str.replace('[.98]', '', regex=False)

    # get phosphopeptide rows and remove +79 shift from peptide sequence
    df['phosphopeptide'] = df['peptide'].str.contains('[+79', regex=False)
    df['peptide'] = df['peptide'].str.replace('[+79.966]', '', regex=False)

    # chop off first two and last two chars (Flanking X.PEPTIDE.X)
    df['peptide'] = df['peptide'].str[2:-2]

    # get length and protein IDs
    df['length'] = df['peptide'].str.len()
    df['Uniprot'] = df['Protein Name'].str.split("|").str[1]
    df['HGNC'] = df['Protein Name'].str.split("GN=").str[1].str.split(" PE=").str[0]

    #remove <8mers
    df = df[df['peptide'].str.len() >= 8]

    # add sample ID (PID)
    df['PID'] = PID
    df['class'] = ['class II' if 'classII' in x else 'class I' for x in df['PID']]

    return df

colDict = {'Peptide\n< ProteinMetrics Confidential >':'peptide', 'Starting\nposition': 'start pos', 'Delta\nMod': 'dMod',
           '|Log Prob|': 'logP', '# of unique\npeptides': 'unique count', 'Protein\nDB number': 'db'}
consCol = ['peptide', 'Modification Type(s)', 'start pos', 'Score', 'Delta', 'dMod', 'logP', 'unique count', 'Protein Name']

fdir = 'MS_data/'

#static file list
files = ['AML14_DCB.xlsx', 'OCI-AML2_DMSO.xlsx' ]

# harcoding df filtering because of discrepancies sample sheetnames
# concatenate all into long form dataframe
aml14_dcb = createDF(fdir+files[0], 'Spectra', files[0].split('.')[0]+'_classI')
ociaml2_dmso = createDF(fdir+files[2], 'Spectra', files[2].split('.')[0]+'_classI')

df = pd.concat([aml14_dcb, ociaml2_dmso], ignore_index=True)

df.to_csv('1_parsedDF.csv')
df.to_pickle('1_parsedDF.pkl')