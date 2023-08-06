# Project Title

Simplifying Regression and Classification Modeling

## Guide

### Installation setup

`pip install AlgoMaster`

### Classfication model

1.  Initialize the model

        `Classifier=AlgoMaster.Classifier(X,Y,test_size=0.2,random_state=20)`

2.  Train the model and predict the results in table format

        `Classifier.model_training()`

3.  Ensemble technique

        `Classifier.ensemble_prediction(No. of models)`

4.  Single Training
    To predict unseen data

        `data=[1,2,3,4,5,6,7,8,9]
        Classifier.logistic_test(data)
        Classifier.KNeighbors_test(data)
        Classifier.GaussianNB_test(data)
        Classifier.Bagging_test(data)
        Classifier.ExtraTrees_test(data)
        Classifier.RandomForest_test(data)
        Classifier.DecisionTree_test(data)
        Classifier.AdaBoost_test(data)
        Classifier.GradientBoosting_test(data)
        Classifier.XGBoost_test(data)
        Classifier.SGD_test(data)
        Classifier.SVC_test(data)
        Classifier.Ridge_test(data)
        Classifier.BernoulliNB_test(data)`

5.  Hyperparameter Turning
    To find the best parameters for the model

        `Classifier.hyperparameter_tuning()`

6.  Single Hyperparameter Turning
    To find the best parameters for the model

        `Classifier.logistic_hyperparameter()
        Classifier.KNeighbors_hyperparameter()
        Classifier.GaussianNB_hyperparameter()
        Classifier.Bagging_hyperparameter()
        Classifier.ExtraTrees_hyperparameter()
        Classifier.RandomForest_hyperparameter()
        Classifier.DecisionTree_hyperparameter()
        Classifier.AdaBoost_hyperparameter()
        Classifier.GradientBoosting_hyperparameter()
        Classifier.XGBoost_hyperparameter()
        Classifier.SGD_hyperparameter()
        Classifier.SVC_hyperparameter()
        Classifier.Ridge_hyperparameter()
        Classifier.BernoulliNB_hyperparameter()`

### Regression model

1.  Initialize the model

        `Regressor=AlgoMaster.Regressor(X,Y,test_size=0.2,random_state=20)`

2.  Train the model and predict the results in table format

        `Regressor.model_training()`

3.  Ensemble technique

        `Regressor.ensemble_prediction(No. of models)`

4.  Single Training

        `data=[1,2,3,4,5,6,7,8,9]
        Regressor.LinearRegression_test(data)
        Regressor.KNeighbors_test(data)
        Regressor.Bagging_test(data)
        Regressor.ExtraTrees_test(data)
        Regressor.RandomForest_test(data)
        Regressor.DecisionTree_test(data)
        Regressor.AdaBoost_test(data)
        Regressor.GradientBoosting_test(data)
        Regressor.XGBoost_test(data)
        Regressor.TheilSen_test(data)
        Regressor.SVR_test(data)
        Regressor.Ridge_test(data)
        Regressor.RANSAC_test(data)
        Regressor.ARD_test(data)
        Regressor.BayesianRidge_test(data)
        Regressor.HuberRegressor_test(data)
        Regressor.Lasso_test(data)
        Regressor.ElasticNet_test(data)`

5.  Hyperparameter Turning
    To find the best parameters for the model

        `Regressor.hyperparameter_tuning()`

6.  Single Hyperparameter Turning
    To find the best parameters for the model

        `Regressor.KNeighbors_hyperparameter()
        Regressor.Bagging_hyperparameter()
        Regressor.ExtraTrees_hyperparameter()
        Regressor.RandomForest_hyperparameter()
        Regressor.DecisionTree_hyperparameter()
        Regressor.AdaBoost_hyperparameter()
        Regressor.GradientBoosting_hyperparameter()
        Regressor.XGBoost_hyperparameter()
        Regressor.TheilSen_hyperparameter()
        <!-- Regressor.SVR_hyperparameter() -->
        Regressor.Ridge_hyperparameter()
        Regressor.RANSAC_hyperparameter()
        Regressor.ARD_hyperparameter()
        Regressor.BayesianRidge_hyperparameter()
        Regressor.Lasso_hyperparameter()
        Regressor.ElasticNet_hyperparameter()`
