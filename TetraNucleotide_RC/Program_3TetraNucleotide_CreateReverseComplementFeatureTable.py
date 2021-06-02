from pandas.io.formats.format import common_docstring
from skbio import DNA
import pandas as pd
import os


CombinedDataset_path = "../TetraNucleotide/combinedDataset_nFeatureTable.tsv"

# Reading combined Feature Table
combinedDataset = pd.read_csv(CombinedDataset_path, index_col=0, sep="\t")

# Extracting Tetranucleotides' name
featuresName = [ x for x in combinedDataset.keys()[7:-1]]

# Calculating new features based on tetraNucleotides & their reverse complement
while len(featuresName)>0 : 
    tetraNucleotideName = featuresName[0]

    seq = DNA(tetraNucleotideName)
    tetraNucleotide_ReverseComp = str(seq.reverse_complement())

    combinedDataset[f'{tetraNucleotideName}/{tetraNucleotide_ReverseComp}'] = combinedDataset[tetraNucleotideName] + combinedDataset[tetraNucleotide_ReverseComp]

    combinedDataset.drop(tetraNucleotideName, axis=1, inplace=True)

    featuresName.remove(tetraNucleotideName)

    if (tetraNucleotide_ReverseComp != tetraNucleotideName):
        combinedDataset.drop(tetraNucleotide_ReverseComp, axis=1, inplace=True)
        featuresName.remove(tetraNucleotide_ReverseComp)

combinedDataset.to_csv(f"./combinedDataset_nFeatureTable_TetraNucleotide_RC.tsv", sep="\t")
# pd.set_option('display.max_columns', None)


