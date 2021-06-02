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



#TetraNucleotide

combinedDataset = pd.read_csv("./TetraNucleotide/combinedDataset_nFeatureTable.tsv", "\t")

param_grid = {
    'max_features':[23],
    'min_samples_leaf': [1],
    'min_samples_split': [3],
    'n_estimators': [500]}

param_grid_previous = {
    'max_features':['sqrt'],
    'min_samples_leaf': [5],
    'min_samples_split': [4],
    'n_estimators': [300]}



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




mine = []
previous = []

for x in range(10):
    grid_search = grid.fit(X_train, y_train)
    grid_search_previous = grid_Previous.fit(X_train_previous, y_train)
    print("-----Mine----")
    # print(grid_search.best_params_)
    print(grid.best_score_)
    mine.append(grid.best_score_)

    print("\n-----Previous----")
    # print(grid_search_previous.best_params_)
    print(grid_Previous.best_score_, '\n')
    previous.append(grid_Previous.best_score_)

print("Mine Average = ", sum(mine)/len(mine))
print("Previous Average = ", sum(previous)/len(previous))

# tri_mine =     0.71  0.720
# tri_previous = 0.70  0.715

# tetra_mine =     0.73  0.72
# tetra_previous = 0.71  0.70

# tetraRC_mine =     0.725  0.72
# tetraRC_Previous = 0.720  0.71