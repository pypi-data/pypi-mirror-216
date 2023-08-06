import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.naive_bayes import GaussianNB, BernoulliNB
import numpy as np
from heapq import nlargest
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
class Classifier:   
    def __init__(self, X, Y, test_size=0.2, random_state=42):
        self.X = X
        self.Y = Y
        self.sample= None
        self.results={}
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=test_size, stratify=Y, random_state=random_state)
        self.model = [
            LogisticRegression(), KNeighborsClassifier(), GaussianNB(),
            BaggingClassifier(), ExtraTreesClassifier(),
            RidgeClassifier(), SGDClassifier(), RandomForestClassifier(),
            xgb.XGBClassifier(), AdaBoostClassifier(), BernoulliNB(),
            GradientBoostingClassifier(), DecisionTreeClassifier(), SVC()
        ]
        self.model_name = [
            'Logistic Regression', 'KNeighborsClassifier', 'GaussianNB',
            'BaggingClassifier', 'ExtraTreesClassifier', 'RidgeClassifier', 'SGDClassifier',
            'RandomForestClassifier', 'XGBClassifier', 'AdaBoostClassifier',
            'BernoulliNB', 'GradientBoostingClassifier', 'DecisionTreeClassifier', 'SVC'
        ]
        self.model_table = pd.DataFrame(columns=['model name', 'accuracy', 'confusion', 'roc', 'f1', 'recall', 'precision'])
        self.models={
            'LogisticRegression':{
                'model':LogisticRegression(),
                'params':{
                    'C': [0.1, 1, 10, 100, 1000],
                    'penalty': ['l2'],
                    'tol': [1e-3, 1e-4, 1e-5, 1e-6],
                    'fit_intercept': [True, False],
                    'intercept_scaling': [1, 10, 100, 1000],
                    'class_weight': ['balanced', None],
                    'solver': ['newton-cg', 'lbfgs', 'sag', 'saga'],
                    'n_jobs': [-1],
                    'random_state': [10, 11, 12, 20, 30, 40, 42],
                    'warm_start': [True, False],
                    'multi_class': ['ovr', 'multinomial', 'auto'],
                    'max_iter': [10000,20000,30000]  # Increase max_iter values
                }
            },
            'KNeighborsClassifier':{
                'model':KNeighborsClassifier(),
                'params':{
                    'n_neighbors':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                    'weights':['uniform','distance'],
                    'algorithm':['auto','ball_tree','kd_tree','brute'],
                    'leaf_size':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                    'p':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                    'metric':['euclidean','manhattan','chebyshev','minkowski'],
                    'n_jobs':[-1],
                } 
            }, 
            'GaussianNB':{
                'model':GaussianNB(),
                'params':{
                    'var_smoothing':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000],
                }
            },
            'BernoulliNB':{
                'model':BernoulliNB(),
                'params':{
                    'alpha':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2],
                    'binarize':[0,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000],
                }
            },
            'BaggingClassifier':{
                'model':BaggingClassifier(),
                'params':{
                    'max_samples':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                    'max_features':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                }
            },
            'ExtraTreesClassifier':{
                'model':ExtraTreesClassifier(),
                'params':{
                    'max_depth':[None,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                    'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                    'min_weight_fraction_leaf':[0.0,0.1,0.2,0.3,0.4,0.5],
                    'max_features':['sqrt','log2',None],
                    'min_impurity_decrease':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'min_samples_split':[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                    'ccp_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                }
            },
            'RidgeClassifier':{
                'model':RidgeClassifier(),
                'params':{
                    'alpha':[1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2],
                    'fit_intercept':[True,False],
                    'copy_X':[True,False],
                    'tol':[0.0001,0.001,0.01,0.1,1.0,10.0,100.0,1000.0],
                    'random_state':[None,10,11,12,20,30,40,42],
                    'positive':[True,False],
                    'class_weight':['balanced',None],
                }
            },
            'SGDClassifier':{
                'model':SGDClassifier(),   
                'params':{
                    'penalty':['l2','l1','elasticnet'],
                    'alpha':[0.0001,0.001,0.01,0.1,1.0],
                    'tol':[0.0001,0.001,0.01,0.1,1.0],
                    'epsilon':[0.0001,0.001,0.01,0.1,1.0,10.0,100.0,1000.0],
                    'learning_rate':['optimal','constant','invscaling','adaptive'],
                    'eta0':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'power_t':[0.5,0.6,0.7,0.8,0.9,1.0],
                    'n_iter_no_change':[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
                    'class_weight':['balanced',None],
                }
            },
            'RandomForestClassifier': {
                'model': RandomForestClassifier(),
                'params' : {
                    'n_estimators':[10,20,30,40,50,60,70,80,90,100],
                    'criterion':['gini','entropy','log_loss'],
                    'max_depth':[None,10,20,30,40,50,60,70,80,90,100],
                    'min_samples_split':[2,3,4,5,6,7,8,9,10],
                    'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
                    'min_weight_fraction_leaf':[0.0,0.1,0.2,0.3,0.4,0.5],
                    'max_features':['sqrt','log2'],
                    'max_leaf_nodes':[None,10,20,30,40,50,60,70,80,90,100],
                    'ccp_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'max_samples':[None,10,20,30,40,50,60,70,80,90,100],
                }
            },
            'XGBClassifier':{
                'model':xgb.XGBClassifier(),
                'params':{
                    'max_depth':[3,4,5,6,7,8,9,10],
                    'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'subsample':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'colsample_bytree':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'colsample_bylevel':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'reg_alpha':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'reg_lambda':[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                }
            },
            'AdaBoostClassifier':{
                'model':AdaBoostClassifier(),
                'params':{
                    'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'algorithm':['SAMME.R'],
                    'random_state':[None,10,11,12,20,30,40,42],
                }
            },
            'GradientBoostingClassifier':{
                'model':GradientBoostingClassifier(),
                'params':{
                    'learning_rate':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'n_estimators':[10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000],
                    'subsample':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'min_samples_split':[2,3,4,5,6,7,8,9,10],
                    'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
                    'max_depth':[3,4,5,6,7,8,9,10],
                }
            },
            'SVC':{
                'model':SVC(),
                'params':{
                    'C':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                    'kernel':['rbf'],
                    'degree':[3,4,5,6,7,8,9,10],
                    'gamma':['scale','auto'],
                    'random_state':[None,10,11,12,20,30,40,42],
                }
            },
            'DecisionTreeClassifier':{
                'model':DecisionTreeClassifier(),
                'params':{
                    'min_samples_split':[2,3,4,5,6,7,8,9,10],
                    'min_samples_leaf':[1,2,3,4,5,6,7,8,9,10],
                    'min_weight_fraction_leaf':[0.0],
                    'random_state':[None,10,11,12,20,30,40,42],
                    'min_impurity_decrease':[0.0],
                    'ccp_alpha':[0.0],
                }
            }
        }
    def format_input_data(self):
        if isinstance(self.sample, np.ndarray):
            if self.sample.ndim == 2 and self.sample.shape[0] == 1:
                return self.sample
            else:
                return self.sample.reshape(1, -1)
        else:
            return np.asarray(self.sample).reshape(1, -1)
    def model_accuracy(self, y_test_f, y_pred_f, model_name):
        acc = accuracy_score(y_test_f, y_pred_f)
        confusion = confusion_matrix(y_test_f, y_pred_f)
        roc = roc_auc_score(y_test_f, y_pred_f)
        f1 = f1_score(y_test_f, y_pred_f)
        recall = recall_score(y_test_f, y_pred_f)
        precision = precision_score(y_test_f, y_pred_f)
        return {'model name': model_name, 'accuracy': acc, 'confusion': confusion, 'roc': roc, 'f1': f1, 'recall': recall, 'precision': precision}
    def model_training(self):
        model_results = []
        for model, model_name in zip(self.model, self.model_name):
            model.fit(self.X_train, self.Y_train)
            y_pred = model.predict(self.X_test)
            model_result = pd.DataFrame([self.model_accuracy(self.Y_test, y_pred, model_name)])
            model_results.append(model_result)
        self.model_table = pd.concat(model_results, ignore_index=True)
        self.model_table = self.model_table.sort_values('accuracy', ascending=False)
        self.model_table.reset_index(drop=True, inplace=True)
        return self.model_table
    def ensemble_prediction(self, count):
        top_models = nlargest(count, self.model_table.iterrows(), key=lambda x: x[1]['accuracy'])
        ensemble_predictions = []
        ensemble_algorithms = []
        for _, model_row in top_models:
            model_index = self.model_name.index(model_row['model name'])
            model = self.model[model_index]
            y_pred = model.predict(self.X_test)
            ensemble_predictions.append((model_index, y_pred))
            ensemble_algorithms.append(model_row['model name'])
        majority_vote = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=np.array([y_pred for _, y_pred in ensemble_predictions]))
        ensemble_name = ', '.join(ensemble_algorithms)
        return self.model_accuracy(self.Y_test, majority_vote, f'Algorithms used for Ensemble [{ensemble_name}]')
    def training(self, model, model_name):
        self.sample = self.format_input_data()
        model.fit(self.X_train, self.Y_train)
        y_pred = model.predict(self.X_test)
        y_predict = model.predict(self.sample)
        return y_predict, self.model_accuracy(self.Y_test, y_pred, model_name)
    def logistic_test(self, pred):
        self.sample = pred
        model = LogisticRegression()
        return self.training(model, 'Logistic Regression')
    def KNeighbors_test(self, pred):
        self.sample=pred
        model = KNeighborsClassifier()
        return self.training(model, 'KNeighborsClassifier')
    def GaussianNB_test(self, pred):
        self.sample=pred
        model = GaussianNB()
        return self.training(model, 'GaussianNB')
    def Bagging_test(self, pred):
        self.sample=pred
        model = BaggingClassifier()
        return self.training(model, 'BaggingClassifier') 
    def ExtraTrees_test(self,pred):
        self.sample=pred
        model = ExtraTreesClassifier()
        return self.training(model, 'ExtraTreesClassifier')
    def Ridge_test(self, pred):
        self.sample=pred
        model = RidgeClassifier()
        return self.training(model, 'RidgeClassifier')
    def SGD_test(self,pred):
        self.sample=pred
        model = SGDClassifier()
        return self.training(model, 'SGDClassifier')   
    def RandomForest_test(self,pred):
        self.sample=pred
        model = RandomForestClassifier()
        return self.training(model, 'RandomForestClassifier')
    def XGBoost_test(self,pred):
        self.sample=pred
        model = xgb.XGBClassifier()
        return self.training(model, 'XGBClassifier')
    def AdaBoost_test(self, pred):
        self.sample=pred
        model = AdaBoostClassifier()
        return self.training(model, 'AdaBoostClassifier')
    def BernoulliNB_test(self,pred):
        self.sample=pred
        model = BernoulliNB()
        return self.training(model, 'BernoulliNB')
    def GradientBoosting_test(self, pred):
        self.sample=pred
        model = GradientBoostingClassifier()
        return self.training(model, 'GradientBoostingClassifier')
    def DecisionTree_test(self,pred):
        self.sample=pred
        model = DecisionTreeClassifier()
        return self.training(model, 'DecisionTreeClassifier')
    def SVC_test(self,pred):
        self.sample=pred
        model = SVC()
        return self.training(model, 'SVC')
    def hyperparameter_tuning(self):
        
        self.results = {}
        cv_sets = 5  # Set the number of cross-validation folds
        for model_name, model_data in self.models.items():
            model = model_data['model']
            param_grid = model_data['params']
            grid_search = RandomizedSearchCV(
                    estimator=model,
                    param_distributions=param_grid,
                    n_iter=5,
                    scoring='accuracy',
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
        self.model_data.fit(self.X_train,self.Y_train)
        self.ypred=self.model_data.predict(self.sample)
        return self.ypred
        
    def single_hyper(self):
        self.results={}
        grid_search=RandomizedSearchCV(
            estimator=self.models[self.model_name]['model'],
            param_distributions=self.models[self.model_name]['params'],
            n_iter=5,
            scoring='accuracy',
            cv=5,
            n_jobs=-1
        )
        grid_search.fit(self.X_train,self.Y_train)
        self.results[self.model_name]={
            'best_score':grid_search.best_score_,
            'best_params':grid_search.best_params_,
            'test_score':grid_search.score(self.X_test,self.Y_test)
        }

    def logistic_hyperparameter(self,pred):
        self.sample = pred
        if 'LogisticRegression' not in self.results:
            self.model_name='LogisticRegression'
            self.single_hyper()
        self.model_data=LogisticRegression(**self.results['LogisticRegression']['best_params'])
        return self.hyper_training()

    def KNeighbors_hyperparameter(self,pred):
        self.sample=pred
        if 'KNeighborsClassifier' not in self.results:
            self.model_name='KNeighborsClassifier'
            self.single_hyper()
        self.model_data=KNeighborsClassifier(**self.results['KNeighborsClassifier']['best_params'])
        return self.hyper_training()
    
    def GaussianNB_hyperparameter(self,pred):
        self.sample=pred
        if 'GaussianNB' not in self.results:
            self.model_name='GaussianNB'
            self.single_hyper()
        self.model_data=GaussianNB(**self.results['GaussianNB']['best_params'])
        return self.hyper_training()
            
    def BernoulliNB_hyperparameter(self,pred):
        self.sample=pred
        if 'BernoulliNB' not in self.results:
            self.model_name='BernoulliNB'
            self.single_hyper()
        self.model_data=BernoulliNB(**self.results['BernoulliNB']['best_params'])
        return self.hyper_training()
            
    def Bagging_hyperparameter(self,pred):
        self.sample=pred
        if 'BaggingClassifier' not in self.results:
            self.model_name='BaggingClassifier'
            self.single_hyper()
        self.model_data=BaggingClassifier(**self.results['BaggingClassifier']['best_params'])
        return self.hyper_training()
            
    def ExtraTrees_hyperparameter(self,pred):
        self.sample=pred
        if 'ExtraTreesClassifier' not in self.results:
            self.model_name='ExtraTreesClassifier'
            self.single_hyper()
        self.model_data=ExtraTreesClassifier(**self.results['ExtraTreesClassifier']['best_params'])
        return self.hyper_training()
            
    def Ridge_hyperparameter(self,pred):
        self.sample=pred
        if 'RidgeClassifier' not in self.results:
            self.model_name='RidgeClassifier'
            self.single_hyper()
        self.model_data=RidgeClassifier(**self.results['RidgeClassifier']['best_params'])
        return self.hyper_training()
            
    def SGD_hyperparameter(self,pred):
        self.sample=pred
        if 'SGDClassifier' not in self.results:
            self.model_name='SGDClassifier'
            self.single_hyper()
        self.model_data=SGDClassifier(**self.results['SGDClassifier']['best_params'])
        return self.hyper_training()
        
    def RandomForest_hyperparameter(self,pred):
        self.sample=pred
        if 'RandomForestClassifier' not in self.results:
            self.model_name='RandomForestClassifier'
            self.single_hyper()
        self.model_data=RandomForestClassifier(**self.results['RandomForestClassifier']['best_params'])
        return self.hyper_training()
            
    def XGBoost_hyperparameter(self,pred):
        self.sample=pred
        if 'XGBClassifier' not in self.results:
            self.model_name='XGBClassifier'
            self.single_hyper()
        self.model_data=xgb.XGBClassifier(**self.results['XGBClassifier']['best_params'])
        return self.hyper_training()
            
    def AdaBoost_hyperparameter(self,pred):
        self.sample=pred
        if 'AdaBoostClassifier' not in self.results:
            self.model_name='AdaBoostClassifier'
            self.single_hyper()
        self.model_data=AdaBoostClassifier(**self.results['AdaBoostClassifier']['best_params'])
            
    def GradientBoosting_hyperparameter(self,pred):
        self.sample=pred
        if 'GradientBoostingClassifier' not in self.results:
            self.model_name='GradientBoostingClassifier'
            self.single_hyper()
        self.model_data=GradientBoostingClassifier(**self.results['GradientBoostingClassifier']['best_params'])
        return self.hyper_training()
            
    def SVC_hyperparameter(self,pred):
        self.sample=pred
        if 'SVC' not in self.results:
            self.model_name='SVC'
            self.single_hyper()
        self.model_data=SVC(**self.results['SVC']['best_params'])
        return self.hyper_training()
            
    def DecisionTree_hyperparameter(self,pred):
        self.sample=pred
        if 'DecisionTreeClassifier' not in self.results:
            self.model_name='DecisionTreeClassifier'
            self.single_hyper()
        self.model_data=DecisionTreeClassifier(**self.results['DecisionTreeClassifier']['best_params'])
        return self.hyper_training()
        
  