import pandas as pd
from sklearn.model_selection import  train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,AdaBoostRegressor,BaggingRegressor,ExtraTreesRegressor
from sklearn.linear_model import (Lasso,ElasticNet,Ridge,ARDRegression,RANSACRegressor,
TheilSenRegressor,HuberRegressor,BayesianRidge,LinearRegression)
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np
import math
from heapq import nlargest
from sklearn.model_selection import RandomizedSearchCV

class Regression:
    def __init__(self, X, Y, test_size=0.2, random_state=20):
        self.X = X
        self.Y = Y
        self.results = {}
        self.sample= None
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=test_size, random_state=random_state)
        self.model = [
            LinearRegression(),DecisionTreeRegressor(),
            KNeighborsRegressor(),RandomForestRegressor(),AdaBoostRegressor(),XGBRegressor(),GradientBoostingRegressor(),SVR(),Ridge(),Lasso(),ElasticNet(),
            TheilSenRegressor(),RANSACRegressor(),HuberRegressor(),ARDRegression(),BayesianRidge(),BaggingRegressor(),ExtraTreesRegressor()
        ]

        self.model_name = ['LinearRegression','DecisionTreeRegressor','KNeighborsRegressor','RandomForestRegressor','AdaBoostRegressor','XGBRegressor','GradientBoostingRegressor',
                           'SVR','Ridge','Lasso','ElasticNet','TheilSenRegressor','RANSACRegressor','HuberRegressor','ARDRegression','BayesianRidge','BaggingRegressor','ExtraTreesRegressor'
                        ]

        self.model_table = pd.DataFrame(columns=['model name', 'MSE', 'RMSE', 'r2', 'MAE'])
        self.models={
            'KNeighborsRegressor':{
                'model':KNeighborsRegressor(),
                'params':{
                    'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                    'weights': ['uniform', 'distance'],
                    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                    'leaf_size': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                    'p': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                    'metric': ['euclidean', 'manhattan', 'chebyshev', 'minkowski'],
                    'n_jobs': [-1],
                } 
            },
            'Ridge': {
                'model': Ridge(),
                'params': {
                    'alpha': [0.1, 1.0, 10.0],  # Regularization strength (smaller values specify stronger regularization)
                    'fit_intercept': [True, False],  # Whether to calculate the intercept for this model
                    'copy_X': [True, False],  # Whether to copy the input data (set to False if input is already a NumPy array)
                    'max_iter': [None, 100, 1000],  # Maximum number of iterations for solver to converge
                    'tol': [0.0001, 0.001, 0.01],  # Tolerance for stopping criterion
                    'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga'],  # Solver algorithm to use
                    'positive': [False],  # Whether to constrain the coefficients to be positive (applies only to 'lsqr', 'sparse_cg', 'sag', 'saga' solvers)
                    'random_state': [None, 42]  # Seed for random number generator
                }
            },
            'DecisionTreeRegressor': {
                'model': DecisionTreeRegressor(),
                'params': {
                    'splitter': ['best', 'random'],  # Strategy used to choose the split at each node
                    'criterion': ['friedman_mse', 'poisson', 'absolute_error', 'squared_error'],
                    'max_depth': [None, 5, 10, 20],  # Maximum depth of the tree
                    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
                    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
                    'min_weight_fraction_leaf': [0.0, 0.1, 0.2],  # Minimum weighted fraction of the input samples required to be at a leaf node
                    'random_state': [None, 42],  # Seed for random number generator
                    'max_leaf_nodes': [None, 10, 20],  # Maximum number of leaf nodes in the tree
                    'min_impurity_decrease': [0.0, 0.1, 0.2],  # Minimum impurity decrease required for a split to happen
                    'ccp_alpha': [0.0, 0.1, 0.2]  # Complexity parameter used for Minimal Cost-Complexity Pruning
                }
            },
            'RandomForestRegressor': {
                'model': RandomForestRegressor(),
                'params': {
                    'n_estimators': [50, 100, 200],  # Number of trees in the forest
                    'criterion': ['friedman_mse', 'poisson', 'absolute_error', 'squared_error'],
                    'max_depth': [None, 5, 10, 20],  # Maximum depth of the trees
                    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
                    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
                    'min_weight_fraction_leaf': [0.0, 0.1, 0.2],  # Minimum weighted fraction of the input samples required to be at a leaf node
                    'max_leaf_nodes': [None, 10, 20],  # Maximum number of leaf nodes in each tree
                    'min_impurity_decrease': [0.0, 0.1, 0.2],  # Minimum impurity decrease required for a split to happen
                    'bootstrap': [True],  # Whether bootstrap samples are used when building trees
                    'oob_score': [False],  # Whether to use out-of-bag samples to estimate the R^2 on unseen data
                    'random_state': [None, 42],  # Seed for random number generator
                    'ccp_alpha': [0.0, 0.1, 0.2],  # Complexity parameter used for Minimal Cost-Complexity Pruning
                    'max_samples': [None, 0.5, 0.8]  # Maximum number of samples used for training each tree
                }
            },
            'AdaBoostRegressor':{
                'model':AdaBoostRegressor(),
                'params':{
                    'n_estimators': [50, 100, 200],  # Number of estimators (base models) in the ensemble
                    'learning_rate': [0.1, 0.5, 1.0],  # Learning rate shrinks the contribution of each estimator
                    'loss': ['linear', 'square', 'exponential'],  # Loss function to use when updating weights after each boosting iteration
                    'random_state': [None, 42],  # Seed for random number generator
                }
            },
            'GradientBoostingRegressor':{
                'model':GradientBoostingRegressor(),
                'params':{
                    'loss': ['absolute_error', 'huber', 'quantile', 'squared_error'],  # Loss function to optimize during gradient boosting
                    'learning_rate': [0.1, 0.01, 0.001],  # Learning rate shrinks the contribution of each estimator
                    'n_estimators': [100, 200, 500],  # Number of boosting stages to perform
                    'subsample': [0.8, 1.0],  # Subsample ratio of the training instances
                    'criterion': ['friedman_mse', 'poisson', 'absolute_error', 'squared_error'],  # Function to measure the quality of a split
                    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
                    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
                    'min_weight_fraction_leaf': [0.0, 0.1, 0.2],  # Minimum weighted fraction of the sum total of weights
                    'max_depth': [3, 5, 7],  # Maximum depth of the individual regression estimators
                    'min_impurity_decrease': [0.0, 0.1, 0.2],  # Minimum impurity decrease required for a split to happen
                    'init': [None],  # Estimator object used to initialize the boosting
                    'random_state': [None, 42],  # Seed for random number generator
                    'alpha': [0.9, 0.95, 0.99],  # The alpha-quantile of the huber loss function and the quantile loss function
                    'max_leaf_nodes': [None],  # Maximum number of leaf nodes in each tree
                    'warm_start': [False],  # When set to True, reuse the solution of the previous call to fit
                    'validation_fraction': [0.1],  # Fraction of training data to use as validation set for early stopping
                    'n_iter_no_change': [None],  # Number of iterations with no improvement to wait before early stopping
                    'tol': [0.0001],  # Tolerance for the early stopping criterion
                    'ccp_alpha': [0.0]  # Complexity parameter used for Minimal Cost-Complexity Pruning
                }
            },
            'Lasso':{
                'model':Lasso(),
                'params':{
                    'alpha': [1.0, 0.1, 0.01, 0.001],  # Regularization strength
                    'fit_intercept': [True, False],  # Whether to calculate the intercept for the model
                    'precompute': [False],  # Whether to use precomputed Gram matrix
                    'copy_X': [True],  # Whether to make a copy of X
                    'max_iter': [1000, 2000],  # Maximum number of iterations
                    'tol': [0.0001, 0.00001],  # Tolerance for stopping criterion
                    'warm_start': [False],  # Whether to reuse the solution of the previous call
                    'positive': [False],  # Whether to constrain the coefficients to be positive
                    'random_state': [None],  # Seed of the pseudo-random number generator
                    'selection': ['cyclic', 'random']  # Method used to select the active features
                }
            },
            'ElasticNet':{
                'model':ElasticNet(),
                'params':{
                    'alpha': [1.0, 0.1, 0.01, 0.001],  # Regularization strength
                    'l1_ratio': [0.5, 0.3, 0.7],  # Mixing parameter, with 0 <= l1_ratio <= 1
                    'fit_intercept': [True, False],  # Whether to calculate the intercept for the model
                    'precompute': [False],  # Whether to use precomputed Gram matrix
                    'max_iter': [1000, 2000],  # Maximum number of iterations
                    'copy_X': [True],  # Whether to make a copy of X
                    'tol': [0.0001, 0.00001],  # Tolerance for stopping criterion
                    'warm_start': [False],  # Whether to reuse the solution of the previous call
                    'positive': [False],  # Whether to constrain the coefficients to be positive
                    'random_state': [None],  # Seed of the pseudo-random number generator
                    'selection': ['cyclic', 'random']  # Method used to select the active features
                }
            },
            'TheilSenRegressor':{
                'model':TheilSenRegressor(),
                'params':{
                    'fit_intercept': [True, False],  # Whether to calculate the intercept for the model
                    'copy_X': [True],  # Whether to make a copy of X
                    'max_subpopulation': [10000.0],  # Maximum number of samples for a subpopulation
                    'n_subsamples': [None],  # Number of subsamples to generate
                    'max_iter': [300],  # Maximum number of iterations
                    'tol': [0.001, 0.0001],  # Tolerance for stopping criterion
                    'random_state': [None],  # Seed of the pseudo-random number generator
                    'n_jobs': [None],  # Number of parallel jobs to run
                }
            },
            'RANSACRegressor':{
                'model':RANSACRegressor(),
                'params':{
                    'estimator': [None],  # Estimator object to be used for fitting the data
                    'min_samples': [None],  # Minimum number of samples required to fit the estimator
                    'residual_threshold': [None],  # Maximum residual for a data sample to be considered an inlier
                    'is_data_valid': [None],  # Custom function to validate the input data
                    'is_model_valid': [None],  # Custom function to validate the fitted model
                    'max_trials': [100],  # Maximum number of RANSAC iterations
                    'max_skips': [float('inf')],  # Maximum number of consecutive skipped samples
                    'stop_n_inliers': [float('inf')],  # Stop RANSAC if at least this number of inliers is found
                    'stop_score': [float('inf')],  # Stop RANSAC if the current score is below this threshold
                    'stop_probability': [0.99],  # Desired probability of achieving the stop_score
                    'loss': ['absolute_error'],  # Loss function to be minimized during RANSAC fitting
                    'random_state': [None],  # Seed of the pseudo-random number generator
                    'base_estimator': ['deprecated']  # Deprecated parameter
                }
            },
            'ARDRegression':{
                'model':ARDRegression(),
                'params':{
                    'n_iter': [300],  # Maximum number of iterations
                    'tol': [0.001],  # Tolerance for stopping criteria
                    'alpha_1': [1e-06],  # Hyperparameter for the Gamma distribution prior over the alpha parameter
                    'alpha_2': [1e-06],  # Hyperparameter for the Gamma distribution prior over the lambda parameter
                    'lambda_1': [1e-06],  # Hyperparameter for the Gamma distribution prior over the alpha parameter
                    'lambda_2': [1e-06],  # Hyperparameter for the Gamma distribution prior over the lambda parameter
                    'compute_score': [False],  # Whether to compute the log marginal likelihood at each iteration
                    'threshold_lambda': [10000.0],  # Threshold for removing (pruning) irrelevant features
                    'fit_intercept': [True],  # Whether to calculate the intercept for the model
                    'copy_X': [True],  # Whether to copy the input data
                }
            },
            'BayesianRidge':{
                'model':BayesianRidge(),
                'params':{
                    'n_iter': [300],  # Maximum number of iterations
                    'tol': [0.001],  # Tolerance for stopping criteria
                    'alpha_1': [1e-06],  # Hyperparameter for the Gamma distribution prior over the alpha parameter
                    'alpha_2': [1e-06],  # Hyperparameter for the Gamma distribution prior over the lambda parameter
                    'lambda_1': [1e-06],  # Hyperparameter for the Gamma distribution prior over the alpha parameter
                    'lambda_2': [1e-06],  # Hyperparameter for the Gamma distribution prior over the lambda parameter
                    'alpha_init': [None],  # Initial value for the alpha parameter
                    'lambda_init': [None],  # Initial value for the lambda parameter
                    'compute_score': [False],  # Whether to compute the log marginal likelihood at each iteration
                    'fit_intercept': [True],  # Whether to calculate the intercept for the model
                    'copy_X': [True],  # Whether to copy the input data
                }
            },
            'BaggingRegressor':{
                'model':BaggingRegressor(),
                'params':{
                    'n_estimators': [10],  # Number of base estimators in the ensemble
                    'max_samples': [1.0],  # Maximum number/ratio of samples to draw from the training data for each base estimator
                    'bootstrap': [True],  # Whether to bootstrap the samples
                    'bootstrap_features': [False],  # Whether to bootstrap the features
                    'oob_score': [False],  # Whether to use out-of-bag samples to estimate the generalization performance
                    'warm_start': [False],  # Whether to reuse the previous solution to initialize the next fit
                    'n_jobs': [None],  # Number of jobs to run in parallel for both fit and predict
                    'random_state': [None],  # Random seed for reproducibility
                }       
            },         
            'ExtraTreesRegressor':{
                'model':ExtraTreesRegressor(),
                'params':{
                    'n_estimators': [100],  # Number of trees in the forest
                    'criterion': ['squared_error'],  # Criterion used to measure the quality of a split
                    'max_depth': [None],  # Maximum depth of the tree
                    'min_samples_split': [2],  # Minimum number of samples required to split an internal node
                    'min_samples_leaf': [1],  # Minimum number of samples required to be at a leaf node
                    'min_weight_fraction_leaf': [0.0],  # Minimum weighted fraction of the sum total of weights required to be at a leaf node
                    'max_leaf_nodes': [None],  # Maximum number of leaf nodes in each tree
                    'min_impurity_decrease': [0.0],  # Minimum impurity decrease required for a split to happen
                    'bootstrap': [True],  # Whether bootstrap samples are used when building trees
                    'oob_score': [False],  # Whether to use out-of-bag samples to estimate the generalization performance
                    'n_jobs': [None],  # Number of jobs to run in parallel for both fit and predict
                    'random_state': [None],  # Random seed for reproducibility
                    'warm_start': [False],  # Whether to reuse the previous solution to initialize the next fit
                    'ccp_alpha': [0.0],  # Complexity parameter used for Minimal Cost-Complexity Pruning
                    'max_samples': [None]  # Number/ratio of samples to draw from the training data for each tree
                }
            },
            'XGBRegressor':{
                'model':XGBRegressor(),
                'params':{
                    'max_depth': [3, 4, 5, 6, 7, 8, 9, 10],
                    'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                    'subsample': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                    'colsample_bytree': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                    'colsample_bylevel': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                    'reg_alpha': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                    'reg_lambda': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                }
            },
        }
        
    def format_input_data(self):
        if isinstance(self.sample, np.ndarray):
            if self.sample.ndim == 2 and self.sample.shape[0] == 1:
                return self.sample
            else:
                return self.sample.reshape(1, -1)
        else:
            return np.asarray(self.sample).reshape(1, -1)

    def model_accuracy(self, y_test, y_pred, model_name):
        mse=mean_squared_error(y_test, y_pred)
        rmse=math.sqrt(mse)
        mae=mean_absolute_error(y_test, y_pred)
        r2=r2_score(y_test, y_pred)
        return {'model':model_name,'MSE':mse,'RMSE':rmse,'r2':r2,'MAE':mae}

    def model_training(self):
      model_results = []
      for model, model_name in zip(self.model, self.model_name):
          model.fit(self.X_train, self.Y_train)
          y_pred = model.predict(self.X_test)
          model_result = pd.DataFrame([self.model_accuracy(self.Y_test, y_pred, model_name)])
          model_results.append(model_result)
      self.model_table = pd.concat(model_results, ignore_index=True)
      self.model_table = self.model_table.sort_values('r2', ascending=False)  # Sort by "r2" column
      self.model_table.reset_index(drop=True, inplace=True)
      return self.model_table

    def ensemble_prediction(self, count):
        top_models = nlargest(count, self.model_table.iterrows(), key=lambda x: x[1]['r2'])
        ensemble_predictions = []
        ensemble_algorithms = []
        for _, model_row in top_models:
            model_index = self.model_name.index(model_row['model'])
            model = self.model[model_index]
            y_pred = model.predict(self.X_test)
            ensemble_predictions.append(y_pred)
            ensemble_algorithms.append(model_row['model'])
        ensemble_predictions = np.array(ensemble_predictions)
        averaged_predictions = np.mean(ensemble_predictions, axis=0)
        ensemble_name = ', '.join(ensemble_algorithms)
        return self.model_accuracy(self.Y_test, averaged_predictions, f'Algorithms used for Ensemble [{ensemble_name}]')

    def training(self, model, model_name):
        self.sample = self.format_input_data()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict = model.predict(self.sample)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, model_name)
    
    def KNeighbors_test(self, pred):
        self.sample=pred
        model = KNeighborsRegressor()
        return self.training(model, 'KNeighbors Regressor')
    
    def LinearRegression_test(self, pred):
        self.sample=pred
        model = LinearRegression()
        return self.training(model, 'LinearRegression')
    
    def Ridge_test(self, pred):
        self.sample=pred
        model = Ridge()
        return self.training(model, 'Ridge')
    
    def Lasso_test(self, pred):
        self.sample=pred
        model = Lasso()
        return self.training(model, 'Lasso')
    
    def ElasticNet_test(self, pred):
        self.sample=pred
        model = ElasticNet()
        return self.training(model, 'ElasticNet')
    
    def DecisionTree_test(self, pred):
        self.sample=pred
        model = DecisionTreeRegressor()
        return self.training(model, 'DecisionTreeRegressor')
    
    def RandomForest_test(self, pred):
        self.sample=pred
        model = RandomForestRegressor()
        return self.training(model, 'RandomForestRegressor')
    
    def AdaBoost_test(self, pred):
        self.sample=pred
        model = AdaBoostRegressor()
        return self.training(model, 'AdaBoostRegressor')
    
    def XGBoost_test(self, pred):
        self.sample=pred
        model = XGBRegressor()
        return self.training(model, 'XGBRegressor')
    
    def GradientBoosting_test(self, pred):
        self.sample=pred
        model = GradientBoostingRegressor()
        return self.training(model, 'GradientBoostingRegressor')
    
    def TheilSen_test(self, pred):
        self.sample=pred
        model = TheilSenRegressor()
        return self.training(model, 'TheilSenRegressor')
    
    def RANSAC_test(self, pred):
        self.sample=pred
        model = RANSACRegressor()
        return self.training(model, 'RANSACRegressor')
    
    def HuberRegressor_test(self, pred):
        self.sample=pred
        model = HuberRegressor()
        return self.training(model, 'HuberRegressor')
    
    def SVR_test(self, pred):
        self.sample=pred
        model = SVR()
        return self.training(model, 'SVR')
    
    def ARD_test(self, pred):
        self.sample=pred
        model = ARDRegression()
        return self.training(model, 'ARDRegression')
    
    def Bayesian_test(self, pred):
        self.sample=pred
        model = BayesianRidge()
        return self.training(model, 'BayesianRidge')
    
    def Bagging_test(self, pred):
        self.sample=pred
        model = BaggingRegressor()
        return self.training(model, 'BaggingRegressor')
    
    def ExtraTrees_test(self, pred):
        self.sample=pred
        model = ExtraTreesRegressor()
        return self.training(model, 'ExtraTreesRegressor')
    
    def hyperparameter_tuning(self):
        self.result={}
        cv_sets=5
        for model_name, model_data in self.models.items():
            model = model_data['model']
            param_grid = model_data['params']
            grid_search = RandomizedSearchCV(
                    estimator=model,
                    param_distributions=param_grid,
                    n_iter=5,
                    scoring='neg_mean_squared_error',
                    cv=cv_sets,
                    n_jobs=-1
                )
            grid_search.fit(self.X_train, self.Y_train)
            self.results[model_name] = {
                    'best_score': grid_search.best_score_,
                    'best_params': grid_search.best_params_,
                    'test_score': grid_search.score(self.X_test, self.Y_test)
            }
        return self.results
    
    def hyper_training(self):
        self.sample=self.format_input_data()
        self._data.fit(self.X_train,self.Y_train)
        self.ypred=self.model_data.predict(self.sample)
        return self.ypred
    
    def single_hyper(self):
        self.results={}
        grid_search=RandomizedSearchCV(
            estimator=self.models[self.model_name]['model'],
            param_distributions=self.models[self.model_name]['params'],
            n_iter=5,
            scoring='neg_mean_squared_error',
            cv=5,
            n_jobs=-1
        )
        grid_search.fit(self.X_train,self.Y_train)
        self.results[self.model_name]={
            'best_score':grid_search.best_score_,
            'best_params':grid_search.best_params_,
            'test_score':grid_search.score(self.X_test,self.Y_test)
        }
    
    def XGBoost_hyperparameter(self, pred):
        self.sample = pred
        if 'XGBRegressor' not in self.results():
            self.model_name = 'XGBRegressor'
            self.single_hyper()
        self.model_data = XGBRegressor(**self.results['XGBRegressor']['best_params'])
        return self.hyper_training()

    def KNeighbors_hyperparameter(self,pred):
        self.sample=pred
        if 'KNeighborsRegressor' not in self.results:
            self.model_name='KNeighborsRegressor'
            self.single_hyper()
        self.model_data=KNeighborsRegressor(**self.results['KNeighborsRegressor']['best_params'])
        return self.hyper_training()
    
    def Ridge_hyperparameter(self,pred):
        self.sample=pred
        if 'Ridge' not in self.results:
            self.model_name='Ridge'
            self.single_hyper()
        self.model_data=Ridge(**self.results['Ridge']['best_params'])
        return self.hyper_training()
    
    def DecisionTree_hyperparameter(self,pred):
        self.sample=pred
        if 'DecisionTreeRegressor' not in self.results:
            self.model_name='DecisionTreeRegressor'
            self.single_hyper()
        self.model_data=DecisionTreeRegressor(**self.results['DecisionTreeRegressor']['best_params'])
        return self.hyper_training()
    
    def RandomForest_hyperparameter(self,pred):
        self.sample=pred
        if 'RandomForestRegressor' not in self.results:
            self.model_name='RandomForestRegressor'
            self.single_hyper()
        self.model_data=RandomForestRegressor(**self.results['RandomForestRegressor']['best_params'])
        return self.hyper_training()
    
    def AdaBoost_hyperparameter(self,pred):
        self.sample=pred
        if 'AdaBoostRegressor' not in self.results:
            self.model_name='AdaBoostRegressor'
            self.single_hyper()
        self.model_data=AdaBoostRegressor(**self.results['AdaBoostRegressor']['best_params'])
        return self.hyper_training()
    
    def GradientBoosting_hyperparameter(self,pred):
        self.sample=pred
        if 'GradientBoostingRegressor' not in self.results:
            self.model_name='GradientBoostingRegressor'
            self.single_hyper()
        self.model_data=GradientBoostingRegressor(**self.results['GradientBoostingRegressor']['best_params'])
        return self.hyper_training()
    
    def Lasso_hyperparameter(self,pred):
        self.sample=pred
        if 'Lasso' not in self.results:
            self.model_name='Lasso'
            self.single_hyper()
        self.model_data=Lasso(**self.results['Lasso']['best_params'])
        return self.hyper_training()
    
    def ElasticNet_hyperparameter(self,pred):
        self.sample=pred
        if 'ElasticNet' not in self.results:
            self.model_name='ElasticNet'
            self.single_hyper()
        self.model_data=ElasticNet(**self.results['ElasticNet']['best_params'])
        return self.hyper_training()
    
    def TheilSen_hyperparameter(self,pred):
        self.sample=pred
        if 'TheilSenRegressor' not in self.results:
            self.model_name='TheilSenRegressor'
            self.single_hyper()
        self.model_data=TheilSenRegressor(**self.results['TheilSenRegressor']['best_params'])
        return self.hyper_training()
    
    def RANSAC_hyperparameter(self,pred):
        self.sample=pred
        if 'RANSACRegressor' not in self.results:
            self.model_name='RANSACRegressor'
            self.single_hyper()
        self.model_data=RANSACRegressor(**self.results['RANSACRegressor']['best_params'])
        return self.hyper_training()
    
    def ARD_hyperparameter(self,pred):
        self.sample=pred
        if 'ARDRegression' not in self.results:
            self.model_name='ARDRegression'
            self.single_hyper()
        self.model_data=ARDRegression(**self.results['ARDRegression']['best_params'])
        return self.hyper_training()
    
    def Bayesian_hyperparameter(self,pred):
        self.sample=pred
        if 'BayesianRidge' not in self.results:
            self.model_name='BayesianRidge'
            self.single_hyper()
        self.model_data=BayesianRidge(**self.results['BayesianRidge']['best_params'])
        return self.hyper_training()
    
    def Bagging_hyperparameter(self,pred):
        self.sample=pred
        if 'BaggingRegressor' not in self.results:
            self.model_name='BaggingRegressor'
            self.single_hyper()
        self.model_data=BaggingRegressor(**self.results['BaggingRegressor']['best_params'])
        return self.hyper_training()
    
    def ExtraTrees_hyperparameter(self,pred):
        self.sample=pred
        if 'ExtraTreesRegressor' not in self.results:
            self.model_name='ExtraTreesRegressor'
            self.single_hyper()
        self.model_data=ExtraTreesRegressor(**self.results['ExtraTreesRegressor']['best_params'])
        return self.hyper_training()
    
   