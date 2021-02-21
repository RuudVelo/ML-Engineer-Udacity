from numpy import mean
from numpy import std
from sklearn.model_selection import GroupKFold
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
import time
#import pickle
import pandas as pd
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform
from sklearn.metrics import mean_squared_error, r2_score

def lightgbm_hyperparam_nested_cv_proc(df, num_boost_round = 50, n_iter = 25, number_inner_splits = 5, number_outer_splits = 10, proc_results_name = "list_model_lgb"):
    
    '''
    Returns outer and inner cv results as lists for nested cross-validation in lightgbm with hyperparameter tuning based on RandomSearchCV

            Parameters:
                    df: pandas DataFrame object based on second by second data
                    number_boost_round (int): number of boosting rounds, default = 50
                    n_iter (int): number of iterations for RandomSearchCV
                    number_inner_splits (int): number of inner folds, default = 5
                    number_outer_splits (int): number of outer folds, default = 10
                    proc_results_name (str): prefix name for output file results of inner and outer fold
            Returns:
                    outer and inner cv results as lists for nested cross-validation in lightgbm with hyperparameter tuning based on RandomSearchCV
    '''        
    
    #Nested: This is where k-fold cross-validation is performed within each fold of cross-validation, often to perform hyperparameter tuning during model evaluation. 
    # define the name of the model and output
    import pickle
    
    groups = df['filename']

    X = df.drop(columns=['hr','filename'])
    y = df[['hr']]

# define the model
    num_boost_round = num_boost_round # number of estimators 50
    n_iter = n_iter # amount of candidates (combinations of xgb_reg_params) to run in inner folds 

    model_lgb = lgb.LGBMRegressor(random_state = 101, n_estimators = num_boost_round, objective = 'rmse')

    lgb_param_test ={'num_leaves': sp_randint(6, 50), 
             'min_child_samples': sp_randint(100, 500), 
             'min_child_weight': [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4],
             'subsample': sp_uniform(loc=0.2, scale=0.8), 
             'colsample_bytree': sp_uniform(loc=0.4, scale=0.6),
             'reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
             'reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100]}

    fit_params={"early_stopping_rounds":5, 
            "eval_metric" : 'rmse', 
            'eval_names': ['valid'],
            'verbose': 100,
            'categorical_feature': 'auto'}

# define the inner and outer folds
    inner_CV = GroupKFold(n_splits = number_inner_splits) 
    outer_CV = GroupKFold(n_splits = number_outer_splits) 

# save outer results
    outer_fold_results = list()

# save all cross validation results
    inner_fold_results = []

    start_time = time.time()

## loop through n_splits times createing index’s into the arrays for the allocated rows ##
    for train_index, test_index in outer_CV.split(X, y, groups=groups):

        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        clf = RandomizedSearchCV(estimator=model_lgb, param_distributions=lgb_param_test, n_iter=n_iter, cv=inner_CV, scoring = 'neg_root_mean_squared_error', random_state=101, verbose=True, n_jobs=3)
    
        lgb_est =clf.fit(X_train,y_train, groups.iloc[train_index], eval_set= [(X_test,y_test)],**fit_params)
    
        #Nested CV with parameter optimization
        res = lgb_est.cv_results_
        inner_fold_results.append(res)
    
        best_model = lgb_est.best_estimator_
    
        # evaluate model on the test dataset
        yhat = best_model.predict(X_test)
    
        # evaluate the model
        rmse = mean_squared_error(y_test, yhat, squared=False)
    
        # store the result
        outer_fold_results.append(rmse)
    
        # report progress
        print('>rmse=%.3f, est=%.3f, cfg=%s' % (rmse, -lgb_est.best_score_, lgb_est.best_params_))

    # summarize the estimated performance of the model
    print('RSME: %.3f (%.3f)' % (mean(outer_fold_results), std(outer_fold_results)))

    # dump the files
    with open(proc_results_name + "_inner" + ".pkl", 'wb') as f:
        pickle.dump(inner_fold_results, f)

    with open(proc_results_name + "_outer" + ".pkl", 'wb') as f:
        pickle.dump(outer_fold_results, f)

# end time
    end_time = time.time()

# total time taken
    print(f"Runtime of the program is {end_time - start_time} seconds")    