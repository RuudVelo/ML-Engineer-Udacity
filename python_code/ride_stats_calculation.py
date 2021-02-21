import numpy as np
import json

def ride_stats_calculation(df):
    '''
    Returns a pandas DataFrame with ride statistics

            Parameters:
                    df: pandas DataFrame object based on second by second data
                                        
            Returns:
                    df: pandas DataFrame with ride statistics
    '''        
    
    
    # imports the rider configuration. Define these in 'rider_config.json'
    

    with open('rider_config.json', 'r') as c:
        rider_params = json.load(c)["rider_params"]
    
        
    # calculate some overall statistics per ride
    df_stats = df.groupby('filename').agg(count_records = ('filename', 'size'), mean_hr = ('hr', 'mean'), 
                                                        mean_cad = ('cad', 'mean'), mean_power = ('watts', 'mean'), mean_temp = ('temp', 'mean'), 
                                                        mean_alt=('alt', 'mean'), mean_slope=('slope', 'mean'), min_hr = ('hr', 'min'), 
                                                        max_hr = ('hr', 'max'), min_cad = ('cad', 'min'), max_cad = ('cad', 'max'), 
                                                        min_power =('watts', 'min'),max_power =('watts', 'max'),min_temp =('temp', 'min'),
                                                        max_temp =('temp', 'max'), min_alt =('alt', 'min'),max_alt =('alt', 'max'), 
                                                        min_slope =('slope', 'min'),max_slope =('slope', 'max'), std_hr = ('hr', 'std'), 
                                                        std_power = ('watts', 'var')).reset_index();
    
    df_stats['cv_hr'] = np.round((df_stats['std_hr'] / df_stats['mean_hr']),2)
    df_stats['cv_power'] = np.round((df_stats['std_power'] / df_stats['mean_power']),2)
    
    # add extent of strange records
    
    df_stats['count_zero_hr'] = df.groupby('filename')['hr'].apply(lambda x: (x==0).sum()).reset_index().iloc[:,1]
    df_stats['count_zero_cad'] = df.groupby('filename')['cad'].apply(lambda x: (x==0).sum()).reset_index().iloc[:,1]
    df_stats['count_zero_power'] = df.groupby('filename')['watts'].apply(lambda x: (x==0).sum()).reset_index().iloc[:,1]
    
    df_stats['perc_count_zero_hr'] = np.round((df_stats['count_zero_hr'] / df_stats['count_records'])*100,0)
    df_stats['perc_count_zero_cad'] = np.round((df_stats['count_zero_cad'] / df_stats['count_records'])*100,0)
    df_stats['perc_count_zero_power'] = np.round((df_stats['count_zero_power'] / df_stats['count_records'])*100,0)
    
    df_stats['count_zero_hr_power'] = df.groupby('filename')['hr_power_zero'].apply(lambda x: (x==0).sum()).reset_index().iloc[:,1]
    df_stats['perc_count_zero_hr_power'] = np.round((df_stats['count_zero_hr_power'] / df_stats['count_records'])*100,0)
    
    # add variables which relates to longest period with no data (zeros)
    #https://stackoverflow.com/questions/51605651/find-longest-run-of-consecutive-zeros-for-each-user-in-dataframe
    from itertools import groupby
    
    def len_iter(items):
        return sum(1 for _ in items)
    
    def consecutive_zero(data):
        x = list((len_iter(run) for val, run in groupby(data) if val==0))
        if len(x)==0: return 0 
        else: return max(x)
    
    df_stats['hr_longest_zero_run'] = df.groupby('filename').apply(lambda x: consecutive_zero(x['hr'])).reset_index().iloc[:,1] #.to_frame(name='hr_longest_zero_run')
    df_stats['cad_longest_zero_run'] = df.groupby('filename').apply(lambda x: consecutive_zero(x['cad'])).reset_index().iloc[:,1] #.to_frame(name='cadence_longest_zero_run')
    df_stats['power_longest_zero_run'] = df.groupby('filename').apply(lambda x: consecutive_zero(x['watts'])).reset_index().iloc[:,1] #.to_frame(name='cadence_longest_zero_run')
    
    df_stats['perc_hr_longest_zero_run'] = np.round((df_stats['hr_longest_zero_run'] / df_stats['count_records'])*100,0)
    df_stats['perc_cad_longest_zero_run'] = np.round((df_stats['cad_longest_zero_run'] / df_stats['count_records'])*100,0)
    df_stats['perc_power_longest_zero_run'] = np.round((df_stats['power_longest_zero_run'] / df_stats['count_records'])*100,0)
    
    # rider specific
    #df_stats['count_hr_extremes'] = df.groupby('filename')['hr'].apply(lambda x: (x > rider_params['rider_max_hr']).sum()).reset_index().iloc[:,1]
    df_stats['count_power_extremes'] = df.groupby('filename')['watts'].apply(lambda x: (x > rider_params['rider_max_watts']).sum()).reset_index().iloc[:,1]
    df_stats['count_cad_extremes'] = df.groupby('filename')['cad'].apply(lambda x: (x > rider_params['rider_max_cad']).sum()).reset_index().iloc[:,1]
    
    #df_stats['perc_hr_extremes'] = np.round((df_stats['count_hr_extremes'] / df_stats['count_records'])*100,0)
    df_stats['perc_power_extremes'] = np.round((df_stats['count_power_extremes'] / df_stats['count_records'])*100,0)
    df_stats['perc_cad_extremes'] = np.round((df_stats['count_cad_extremes'] / df_stats['count_records'])*100,0)
    
    # add longest value of consequetive similar heart rate values. ugly but works for now
    
    df_stats['consecutive_hr_similar_values'] = df.groupby('filename').consecutive_hr_similar_values.max().reset_index().iloc[:,1]
    df_stats['perc_consecutive_hr_similar_values'] = np.round((df_stats['consecutive_hr_similar_values'] / df_stats['count_records'])*100,0)
    
    # add longest value of consequetive similar power values. ugly but works for now
    
    df_stats['consecutive_power_similar_values'] = df.groupby('filename').consecutive_power_similar_values.max().reset_index().iloc[:,1]
    df_stats['perc_consecutive_power_similar_values'] = np.round((df_stats['consecutive_power_similar_values'] / df_stats['count_records'])*100,0)
    
    # add longest value of consequetive similar power values. ugly but works for now
    
    df_stats['consecutive_cad_similar_values'] = df.groupby('filename').consecutive_cad_similar_values.max().reset_index().iloc[:,1]
    df_stats['perc_consecutive_cad_similar_values'] = np.round((df_stats['consecutive_cad_similar_values'] / df_stats['count_records'])*100,0)
    
    # add longest value of consequetive similar heart rate to power ratio values. ugly but works for now
    df_stats['consecutive_hr_power_ratio_similar_values'] = df.groupby('filename').consecutive_hr_power_ratio_similar_values.max().reset_index().iloc[:,1]
    df_stats['perc_consecutive_hr_power_ratio_similar_values'] = np.round((df_stats['consecutive_hr_power_ratio_similar_values'] / df_stats['count_records'])*100,0)
    
    return df_stats