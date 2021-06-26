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
# path_Sequence = "./S_pyogenes/S_pyogenes_RAND_Sequences.txt"
# path_Featuretable = "./S_pyogenes/S_pyogenes_FeatureTable_RAND.tsv"

# path_Sequence = "./E_coli/E_coli_sRNAs_Sequences.txt"
# path_Featuretable = "./E_coli/E_coli_FeatureTable_sRNAs.tsv"
# path_Sequence = "./E_coli/E_coli_RAND_Sequences.txt"
# path_Featuretable = "./E_coli/E_coli_FeatureTable_RAND.tsv"

# path_Sequence = "./M_tuberculosis/M_tuberculosis_sRNAs_Sequences.txt"
# path_Featuretable = "./M_tuberculosis/M_tuberculosis_FeatureTable_sRNAs.tsv"
# path_Sequence = "./M_tuberculosis/M_tuberculosis_RAND_Sequences.txt"
# path_Featuretable = "./M_tuberculosis/M_tuberculosis_FeatureTable_RAND.tsv"

path_Sequence = "./X_nematophila_RAND_sequences.txt"
path_Featuretable = "./X_nematophila_RAND_FeatureTable.tsv"


# Reading previouse Feature Table
featureTable = pd.read_csv(path_Featuretable, "\t")


# Reading sRNAs/RAND sequences & Extracting sequence Id
Sequences = pd.read_csv(path_Sequence, header=None, sep="\t")
Sequences.iloc[:,0] = Sequences.iloc[:,0].str.split("(",expand=True).iloc[:,0]


# Number of sequrnces
rowsCount = Sequences.shape[0]

# Number of Nucleotide
NucleotideNum = 4


# Appending TrinucleotidesColumn(new features) and initialize with zeros
iter = itertools.product('ACGT', repeat=NucleotideNum)
iterJoin = []

for i in iter:
    colLable = "".join(i)
    iterJoin.append(colLable)
    colValues_zeros = [0]*rowsCount
    featureTable[colLable] = colValues_zeros

# Filling TrinucleotidesColumn with their frequency for each sequence
for idIndex in range(rowsCount):
    id = Sequences.iloc[idIndex,0]
    seq = Sequences.iloc[idIndex,1]
    s = Sequence(seq)
    freqs = s.kmer_frequencies(NucleotideNum, relative=True, overlap=True)
    for trinucleotide in freqs:
        if trinucleotide in iterJoin :
            featureTable.loc[id , trinucleotide] = freqs[trinucleotide]


# Adding Class(0-1)
is_sRNAs = True if os.path.basename(path_Sequence).find("sRNAs") > 0 else False
if(is_sRNAs):
    featureTable["Class"] = [1]*rowsCount
else:
    featureTable["Class"] = [0]*rowsCount


# Export extended Feature Table
bacteriaName = path_Featuretable.split("/")
sRNAsOrRand = "sRNAs" if "sRNAs" in path_Featuretable else "RAND"
featureTable.to_csv(f"./{bacteriaName[1]}_nFeatureTable_{sRNAsOrRand}.tsv", sep="\t")


# pd.set_option('display.max_columns', None)
# print(featureTable)


