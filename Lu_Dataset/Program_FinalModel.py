import os
import pandas as pd
import numpy as np
import sklearn
import glob
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve,auc
from sklearn.metrics import precision_recall_curve,auc
import matplotlib.pyplot as plt


# # Reading new Feature Tables and create a combined one
# featureTableName_List = glob.glob("./Bacterias_FeatureTable/*.tsv")
# featureTable_list = []
# for x in range(len(featureTableName_List)):
#     featureTable = pd.read_csv(featureTableName_List[x], "\t", index_col=0)
#     rowsCount = featureTable.shape[0]
#     is_sRNAs = True if os.path.basename(featureTableName_List[x]).find("sRNAs") > 0 else False
#     if(is_sRNAs):
#         featureTable["Class"] = [1]*rowsCount
#     else:
#         featureTable["Class"] = [0]*rowsCount
#     featureTable_list.append(featureTable)

# combinedDataset = pd.concat(featureTable_list)
# combinedDataset.to_csv("./combinedDataset_nFeatureTable_Lu.tsv", sep="\t")
# # pd.set_option('display.max_columns', None)




training_df = pd.read_csv("../TetranucleotideWith5Bacteria_RC/combinedDataset_nFeatureTable_TetraNucleotide_RC.tsv", "\t")
training_df = sklearn.utils.shuffle(training_df)
Y_train = training_df.Class
X_train = training_df.drop(["id","Class"], axis=1)
X_train_previous = X_train.iloc[:,range(7)]


rfc = RandomForestClassifier(
    max_features=25, 
    min_samples_leaf=1,
    min_samples_split=2,
    n_estimators=500,)
    
rfc.fit(X_train, Y_train)


rfc_previous = RandomForestClassifier(
    max_features="sqrt", 
    min_samples_leaf=5,
    min_samples_split=4,
    n_estimators=300,)

rfc_previous.fit(X_train_previous, Y_train)


#Save model to a file
# import pickle
# filename = 'model_rf_all_combined_1.sav'
# pickle.dump(rfc, open(filename, 'wb'))

test_df = pd.read_csv("./combinedDataset_nFeatureTable_Lu.tsv", "\t")
# test_df = sklearn.utils.shuffle(test_df)
Y_test = test_df.Class
X_test = test_df.drop(["id","Class"], axis=1)
# X_test.reset_index(inplace=True, drop=True)
X_test_previous = X_test.iloc[:,range(7)]

Y_pred = rfc.predict_proba(X_test)[:, 1]
Y_pred_previous = rfc_previous.predict_proba(X_test_previous)[:,1]

# load the model, if saved to a file
# loaded_model = pickle.load(open(filename, 'rb'))
# y_pred = loaded_model.predict_proba(X_test)[:, 1]


# Plot the Precision-Recall curve


precision, recall, thresholds = precision_recall_curve(Y_test, Y_pred)
precision_previous, recall_previous, thresholds_previous = precision_recall_curve(Y_test, Y_pred_previous)

# Use AUC function to calculate the area under the curve of precision recall curve
auc_precision_recall          = auc(recall, precision)
auc_precision_recall_previous = auc(recall_previous,precision_previous)

print(F" Mine     : {auc_precision_recall}")
print(F" Previous : {auc_precision_recall_previous}")

plt.plot(recall, precision , label= F"With Trinucleotide RC      =  {round(auc_precision_recall,3)}", color = '#5F4B8BFF')
plt.plot(recall_previous, precision_previous, label=F"Without Trinucleotide RC =  {round(auc_precision_recall_previous,3)}", color='#E69A8DFF')

plt.ylabel('Precision')
plt.xlabel('Recall')

leg = plt.legend(loc='lower left', ncol=1, fancybox=True)
leg.get_frame().set_alpha(0.5)

plt.title('Precision-Recall Curve')

# plt.yticks(np.arange(0, 1.2, step=0.2))

plt.savefig('nucleotide')

plt.show()



