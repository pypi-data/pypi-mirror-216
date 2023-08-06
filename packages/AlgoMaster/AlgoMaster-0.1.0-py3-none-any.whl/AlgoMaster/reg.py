import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from regressor import Regression

data=pd.read_csv('F:\packagesPyPi\AlgoMaster\Drug.csv')
for column in data.columns:
    mode_value = data[column].mode()[0]
    data[column].replace('\r\r\n', mode_value, inplace=True)
le=LabelEncoder()
label_mappings = {}
columns_to_encode=['Type','Indication','Form','Drug','Condition']
for col in columns_to_encode:
    le.fit(data[col])
    data[col] = le.transform(data[col])
    label_mappings[col] = {encoded: label for encoded, label in zip(le.transform(le.classes_), le.classes_)}
x=data[['Condition','Drug','EaseOfUse','Form','Indication','Price','Reviews','Satisfaction','Type']]
y=data['Effective']

clg=Regression(x,y,0.2,42)
# print(clg.model_training())
# print(clg.ensemble_prediction(4))

sample_data = [1,30,5.0,1,2,224.77,2.5,5.0,2]
# print(clg.KNeighbors_test(sample_data))
# print(clg.Linear_test(sample_data))
# print(clg.Ridge_test(sample_data))
# print(clg.Elastic_test(sample_data))
# print(clg.DecisionTree_test(sample_data))
# print(clg.RandomForest_test(sample_data))
# print(clg.AdaBoost_test(sample_data))
# print(clg.XGB_test(sample_data))
# print(clg.GradientBoosting_test(sample_data))
# print(clg.TheilSen_test(sample_data))
# print(clg.RANSAC_test(sample_data))
# print(clg.Huber_test(sample_data))
# print(clg.SVR_test(sample_data))
# print(clg.ARD_test(sample_data))
# print(clg.Bagging_test(sample_data))
# print(clg.ExtraTrees_test(sample_data))
# print(clg.Bayesian_test)

# print(clg.hyperparameter_tuning())
print(clg.knn_hyperparameter(sample_data))
print(clg.ridge_hyperparameter(sample_data))
print(clg.DecisionTree_hyperparameter(sample_data))
print(clg.RandomForest_hyperparameter(sample_data))
print(clg.AdaBoost_hyperparameter(sample_data))
# #print(clg.SVR_hyperparameter(sample_data))
print(clg.Lasso_hyperparameter(sample_data))
print(clg.Elastic_hyperparameter(sample_data))
print(clg.Bayesian_hyperparameter(sample_data))
print(clg.TheilSen_hyperparameter(sample_data))
print(clg.RANSAC_hyperparameter(sample_data))
# # print(clg.Huber_hyperparameter(sample_data))
print(clg.ARD_hyperparameter(sample_data))
print(clg.Bagging_hyperparameter(sample_data))
print(clg.ExtraTrees_hyperparameter(sample_data))
print(clg.xgb_hyperparameter(sample_data))
print(clg.GradientBoosting_hyperparameter(sample_data))
