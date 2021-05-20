import pandas as pd
import sklearn
import glob
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier


# # Reading new Feature Tables
# featureTable_List = glob.glob("./*.tsv")


# # Combining Feature Tables
# CombinedDataset = pd.read_csv(featureTable_List[0], "\t")
# for x in featureTable_List[1:]:
#     file = pd.read_csv(x, "\t")
#     CombinedDataset = pd.merge(CombinedDataset, file, how='outer')

# pd.set_option('display.max_columns', None)
# print(CombinedDataset.shape)
# print(CombinedDataset)

# CombinedDataset.to_csv("./CombinedDataset_nFeatureTable.tsv", sep="\t")


CombinedDataset = pd.read_csv("./CombinedDataset_nFeatureTable.tsv", "\t", index_col=0)

CombinedDataset = sklearn.utils.shuffle(CombinedDataset)

y_train = CombinedDataset.Class
X_train = CombinedDataset.drop(["id","Class"], axis=1)
# X_train.reset_index(inplace=True, drop=True)


param_grid = {
    # 'max_features':[2,5,7,'sqrt','log2'],
    'max_features':[13],
    # 'min_samples_leaf': [1,2,3,4,5],
    'min_samples_leaf': [4],
    # 'min_samples_split': [2,5],
    'min_samples_split': [5],
    # 'n_estimators': [200,300,400,500,600,700,800]}
    'n_estimators': [350]}


grid = GridSearchCV(estimator=RandomForestClassifier(), 
                    param_grid=param_grid,
                    cv=200, 
                    n_jobs=-1,
                    scoring='average_precision')


grid_search = grid.fit(X_train, y_train)
print("----Best Params-----")
print(grid_search.best_params_)
print(grid.best_score_)
