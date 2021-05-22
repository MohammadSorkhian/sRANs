from skbio import Sequence
import itertools
import pandas as pd
import os


# path_Sequence = "./R_capsulatus/R_capsulatus_sRNAs_Sequences.txt"
# path_Featuretable = "./R_capsulatus/R_capsulatus_FeatureTable_sRNAs.tsv"
# path_Sequence = "./R_capsulatus/R_capsulatus_RAND_Sequences.txt"
# path_Featuretable = "./R_capsulatus/R_capsulatus_FeatureTable_RAND.tsv"

# path_Sequence = "./S_enterica/S_enterica_sRNAs_Sequences.txt"
# path_Featuretable = "./S_enterica/S_enterica_FeatureTable_sRNAs.tsv"
# path_Sequence = "./S_enterica/S_enterica_RAND_Sequences.txt"
# path_Featuretable = "./S_enterica/S_enterica_FeatureTable_RAND.tsv"

# path_Sequence = "./S_pyogenes/S_pyogenes_sRNAs_Sequences.txt"
# path_Featuretable = "./S_pyogenes/S_pyogenes_FeatureTable_sRNAs.tsv"
path_Sequence = "./S_pyogenes/S_pyogenes_RAND_Sequences.txt"
path_Featuretable = "./S_pyogenes/S_pyogenes_FeatureTable_RAND.tsv"



# Reading previouse Feature Table
featureTable = pd.read_csv(path_Featuretable, "\t")


# Reading sRNAs/RAND sequences & Extracting sequence Id
Sequences = pd.read_csv(path_Sequence, header=None, sep="\t")
Sequences.iloc[:,0] = Sequences.iloc[:,0].str.split("(",expand=True).iloc[:,0]


# Number of sequrnces
rowsCount = Sequences.shape[0]


# Appending TrinucleotidesColumn(new features) and initialize with zeros
iter = itertools.product('ACGT', repeat=3)
for i in iter:
    colLable = "".join(i)
    colValues_zeros = [0]*rowsCount
    featureTable[colLable] = colValues_zeros


# Filling TrinucleotidesColumn with their frequency for each sequence
for idIndex in range(rowsCount):
    id = Sequences.iloc[idIndex,0]
    seq = Sequences.iloc[idIndex,1]
    s = Sequence(seq)
    freqs = s.kmer_frequencies(3, relative=True, overlap=True)
    for trinucleotide in freqs:
        featureTable.loc[id , trinucleotide] = freqs[trinucleotide]


# Adding Class(0-1)
is_sRNAs = True if os.path.basename(path_Sequence).find("sRNAs") > 0 else False
if(is_sRNAs):
    featureTable["Class"] = [1]*rowsCount
else:
    featureTable["Class"] = [0]*rowsCount


# Export extended Feature Table
bacteriaName = path_Featuretable.split("/")
print(bacteriaName)
sRNAsOrRand = "sRNAs" if "sRNAs" in path_Featuretable else "RAND"
print(sRNAsOrRand)
featureTable.to_csv(f"./{bacteriaName[1]}_nFeatureTable_{sRNAsOrRand}.tsv", sep="\t")


# pd.set_option('display.max_columns', None)
# print(featureTable)


