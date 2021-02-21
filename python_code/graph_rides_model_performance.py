import matplotlib.pyplot as plt

def graph_rides_model_performance(df, df_metrics, number_of_files, value_to_sort, high, rows, cols):
    '''
    Returns a plot with ride(s) and power / heart rate development

            Parameters:
                    df: pandas DataFrame object with filename ('filename'), secs ('secs'), heart rate ('hr') and predicted heart rate ('pred_hr')
                    df_metrics: pandas DataFrame object with filename and performance metrics
                    number of files (int): number of ride files to display
                    values to sort (str): 'rmse_test' or 'r2_test' 
                    high: Boolean True or False. If True returns metrics ranking on descending order
                    rows (int): number of rows in plot (rows * cols = number of files)
                    cols (int): number of columns in plot (rows * cols = number of files)
            Returns:
                    plot: matplotlib object with heart rate ('hr') and predicted heart rate ('pred_hr') development for rides in selection
    '''
    if high is True:
        lijst = df_metrics.sort_values(by=[value_to_sort], ascending = False).head(number_of_files).filename.tolist()
    else:
        lijst = df_metrics.sort_values(by=[value_to_sort], ascending = True).head(number_of_files).filename.tolist()
    
    grouped = df[df['filename'].isin(lijst)][['filename','hr','pred_hr','secs']].groupby('filename',sort=False)
    
    ncols = cols
    nrows = rows
       
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20,10), sharey=False)
    for (key, ax) in zip(grouped.groups.keys(), axes.flatten()):
        grouped.get_group(key).plot(x='secs', y=['hr','pred_hr'], ax=ax)
        ax.legend().set_visible(False)
        ax.set_title(grouped.get_group(key).filename.unique());
    
    fig.suptitle('Plots of example rides with {}'.format(value_to_sort) , fontsize=16) 
    
    #handles, labels = ax.get_legend_handles_labels()
    #fig.legend(handles, labels, loc='best', frameon=False, ncol=2, fontsize=14)
    
    handles, labels = ax.get_legend_handles_labels()
    #fig.legend(handles, labels, loc='best', frameon=False, ncol=2, fontsize=14)
    plt.legend(bbox_to_anchor=(1, -0.15), loc='best', ncol=2)
    
    #lower center    
    plt.tight_layout()
    fig.subplots_adjust(top=0.91)
    
    return plt.show()