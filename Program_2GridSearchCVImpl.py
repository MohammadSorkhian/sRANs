import pandas as pd
import sklearn
import glob
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier


# # Reading new Feature Tables
# featureTableName_List = glob.glob("./*.tsv")
# featureTable_list = [pd.read_csv(featureTableName_List[x], "\t", index_col=0) for x in range(len(featureTableName_List))]
# combinedDataset = pd.concat(featureTable_list)

# # pd.set_option('display.max_columns', None)

# combinedDataset.to_csv("./combinedDataset_nFeatureTable.tsv", sep="\t")


combinedDataset = pd.read_csv("./combinedDataset_nFeatureTable(shuffled).tsv", "\t")
combinedDatasetPrevious = combinedDataset.iloc[:,range(8)]
# combinedDataset = sklearn.utils.shuffle(combinedDataset)

y_train = combinedDataset.Class
X_train = combinedDataset.drop(["id","Class"], axis=1)
# X_train.reset_index(inplace=True, drop=True)


param_grid = {
    'max_features':['sqrt'],
    'min_samples_leaf': [5,6],
    'min_samples_split': [5,6],
    'n_estimators': [300]}

param_grid_previous = {
    'max_features':['sqrt'],
    'min_samples_leaf': [5,6],
    'min_samples_split': [4,5],
    'n_estimators': [300]}


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


grid_search = grid.fit(X_train, y_train)
grid_search_previous = grid_Previous.fit(X_train, y_train)
print("-----Mine----")
print(grid_search.best_params_)
print(grid.best_score_)
print("-----Megha----")
print(grid_search_previous.best_params_)
print(grid_Previous.best_score_)
