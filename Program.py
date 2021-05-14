from skbio import Sequence
import itertools
import pandas as pd


path_Sequence = "./R_capsulatus/R_capsulatus_sRNAs_Sequences.txt"
path_Featuretable = "./R_capsulatus/R_capsulatus_FeatureTable_sRNAs.tsv"
# path_Sequence = "./R_capsulatus/R_capsulatus_RAND_Sequences.txt"
# path_Featuretable = "./R_capsulatus/R_capsulatus_FeatureTable_RAND.tsv"

# path_Sequence = "./S_enterica/S_enterica_sRNAs_Sequences.txt"
# path_Featuretable = "./S_enterica/S_enterica_FeatureTable_sRNAs.tsv"
# path_Sequence = "./S_enterica/S_enterica_RAND_Sequences.txt"
# path_Featuretable = "./S_enterica/S_enterica_FeatureTable_RAND.tsv"

# path_Sequence = "./S_pyogenes/S_pyogenes_sRNAs_Sequences.txt"
# path_Featuretable = "./S_pyogenes/S_pyogenes_FeatureTable_sRNAs.tsv"
# path_Sequence = "./S_pyogenes/S_pyogenes_RAND_Sequences.txt"
# path_Featuretable = "./S_pyogenes/S_pyogenes_FeatureTable_RAND.tsv"

featureTable = pd.read_csv(path_Featuretable, "\t")

Sequences = pd.read_csv(path_Sequence, header=None, sep="\t")
Sequences.iloc[:,0] = Sequences.iloc[:,0].str.split("(",expand=True).iloc[:,0]

rowsCount = Sequences.shape[0]


# Append Zero-value TrinucleotidesColumn
iter = itertools.product('ACGT', repeat=3)
for i in iter:
    colLable = "".join(i)
    colValues_zeros = [0]*rowsCount
    featureTable[colLable] = colValues_zeros


# Fill TrinucleotidesColumn
for idIndex in range(rowsCount):
    id = Sequences.iloc[idIndex,0]
    seq = Sequences.iloc[idIndex,1]
    # Calculate Frequencies
    s = Sequence(seq)
    freqs = s.kmer_frequencies(3, relative=True, overlap=False)
    for trinucleotide in freqs:
        featureTable.loc[id , trinucleotide] = freqs[trinucleotide]


# pd.set_option('display.max_columns', None)
print(featureTable)