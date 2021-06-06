import pandas as pd
import sklearn
import glob
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier


# # Reading new Feature Tables
# featureTableName_List = glob.glob("./*.tsv")
# featureTable_list = [pd.read_csv(featureTableName_List[x], "\t", index_col=0) for x in range(len(featureTableName_List))]
# combinedDataset = pd.concat(featureTable_list)
# combinedDataset.to_csv("./combinedDataset_nFeatureTable.tsv", sep="\t")
# # pd.set_option('display.max_columns', None)







# #TriNucleotide

# combinedDataset = pd.read_csv("./TriNucleotide/combinedDataset_nFeatureTable.tsv", "\t")

# param_grid = {
#     'max_features':[15],
#     'min_samples_leaf': [2],
#     'min_samples_split': [5],
#     'n_estimators': [600]}

# param_grid_previous = {
#     'max_features':['sqrt'],
#     'min_samples_leaf': [5],
#     'min_samples_split': [4],
#     'n_estimators': [300]}



# #TetraNucleotide

# combinedDataset = pd.read_csv("./TetraNucleotide/combinedDataset_nFeatureTable.tsv", "\t")

# param_grid = {
#     'max_features':[23],
#     'min_samples_leaf': [1],
#     'min_samples_split': [3],
#     'n_estimators': [500]}

# param_grid_previous = {
#     'max_features':['sqrt'],
#     'min_samples_leaf': [5],
#     'min_samples_split': [4],
#     'n_estimators': [300]}



# #TetraNucleotide_RC

# combinedDataset = pd.read_csv("./TetraNucleotide_RC/combinedDataset_nFeatureTable_TetraNucleotide_RC.tsv", "\t")

# param_grid = {
#     'max_features':['sqrt'],
#     'min_samples_leaf': [1],
#     'min_samples_split': [3],
#     'n_estimators': [500]}

# param_grid_previous = {
#     'max_features':['sqrt'],
#     'min_samples_leaf': [5],
#     'min_samples_split': [4],
#     'n_estimators': [300]}



#TetraNucleotide_With5Bacteria

combinedDataset = pd.read_csv("./TetranucleotideWith5Bacteria/combinedDataset_nFeatureTable.tsv", "\t")

param_grid = {
    'max_features':['sqrt'],
    'min_samples_leaf': [1],
    'min_samples_split': [3],
    'n_estimators': [500]}

param_grid_previous = {
    'max_features':['sqrt'],
    'min_samples_leaf': [5],
    'min_samples_split': [4],
    'n_estimators': [300]}



combinedDataset = sklearn.utils.shuffle(combinedDataset)
y_train = combinedDataset.Class
X_train = combinedDataset.drop(["id","Class"], axis=1)
X_train_previous = X_train.iloc[:,range(7)]
# X_train.reset_index(inplace=True, drop=True)



grid = GridSearchCV(estimator=RandomForestClassifier(), 
                    param_grid=param_grid,
                    cv=10, 
                    n_jobs=-1,
                    scoring='average_precision')
                    
grid_Previous = GridSearchCV(estimator=RandomForestClassifier(), 
                    param_grid=param_grid_previous,
                    cv=10, 
                    n_jobs=-1,
                    scoring='average_precision')




mine_mean = []
previous_mean = []
mine_std = []
previous_std = []

iteration = 10

for x in range(iteration):
    grid_search = grid.fit(X_train, y_train)
    grid_search_previous = grid_Previous.fit(X_train_previous, y_train)
    print("-----Mine----")
    mine_mean.append(grid.cv_results_['mean_test_score'])
    mine_std.append(grid.cv_results_['std_test_score'])
    print("\n-----Previous----")
    previous_mean.append(grid_Previous.cv_results_['mean_test_score'])
    previous_std.append(grid_Previous.cv_results_['std_test_score'])

print("Mine Average = ", sum(mine_mean)/iteration)
print("Previous Average = ", sum(previous_mean)/iteration)

print("Mine STD = ", sum(mine_std)/iteration)
print("Previous STD = ", sum(previous_std)/iteration)


                                                                            
# # tri_mine =     0.71  0.720          0.72(0.09)      0.70(0.087)
# # tri_previous = 0.70  0.715          0.70(0.07)      0.70(0.100)

# # tetra_mine =     0.73  0.72         0.735(0.068)    0.72(0.071)
# # tetra_previous = 0.71  0.70         0.70 (0.067)    0.71(0.072)

# # tetraRC_mine =     0.725  0.72      0.73(0.083)     0.72(0.065)         0.72(0.096)  0.71(0.082)  0.73(0.079)    after not doubeling similar Tretranucleotide and its RC
# # tetraRC_Previous = 0.720  0.71      0.71(0.080)     0.70(0.073)         0.71(0.126)  0.70(0.071)  0.71(0.105)

# # tetraWith5Bacteria_mine =       0.78(0.0728)    0.78(0.055)     0.78(0.048)
# # tetraWith5Bacteria_Previous =   0.74(0.0710)    0.74(0.056)     0.75(0.067)