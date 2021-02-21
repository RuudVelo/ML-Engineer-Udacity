import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

def rmse_r2_test(g):
    rmse_test = np.sqrt(mean_squared_error(g['hr'], g['pred_hr']))
    r2_test = r2_score(g['hr'], g['pred_hr'] )
    return pd.Series({'rmse_test':rmse_test, 'r2_test':r2_test})

def metrics_feat_sel(df_test_name, df_test_name_incl, y_test, model_name, name_output, scaled_test_set=True):
    '''
    Returns a pandas DataFrame with RMSE, R2 and modelname on ride level

            Parameters:
                    df_test_name: name of testset for calculations. Can be numpy array or pandas DataFrame
                    df_test_name_incl: name of the testset including filename
                    y_test: name of y testset
                    model_name: name given to fitted sklearn model object
                    name_output: (str) preferred modelname in DataFrame column output
                    scaled_test_set: (default) set to True if model based on scaled train and testset
            Returns:
                    DataFrame: pandas DataFrame with RMSE, R2 and modelname on ride level
    '''
    if scaled_test_set:
        X_tst = pd.DataFrame(df_test_name.copy())

        X_tst['pred_hr'] = model_name.predict(X_tst)
        X_tst['filename'] = df_test_name_incl['filename'
                ].reset_index(drop=True)
        X_tst['hr'] = pd.DataFrame(y_test).reset_index(drop=True)

        df_model_metrics = X_tst.groupby('filename'
                ).apply(rmse_r2_test).reset_index()
        df_model_metrics['name'] = 'metrics_' + name_output

        print ('Mean RMSE over files',
               np.mean(df_model_metrics.rmse_test))
        print ('Total RMSE', np.sqrt(mean_squared_error(X_tst['hr'],
               X_tst['pred_hr'])))
        print ('R2 test', model_name.score(df_test_name, y_test))
    else:

        X_tst = df_test_name.copy()

        X_tst['pred_hr'] = model_name.predict(X_tst)
        X_tst['filename'] = df_test_name_incl['filename']
        X_tst['hr'] = y_test
    
        df_model_metrics = X_tst.groupby('filename'
                ).apply(rmse_r2_test).reset_index()
        df_model_metrics['name'] = 'metrics_' + name_output
    
        print ('Mean RMSE over files', np.mean(df_model_metrics.rmse_test))
        print ('Total RMSE', np.sqrt(mean_squared_error(X_tst['hr'],
               X_tst['pred_hr'])))
        print ('R2 test', model_name.score(df_test_name, y_test))
    
    return df_model_metrics