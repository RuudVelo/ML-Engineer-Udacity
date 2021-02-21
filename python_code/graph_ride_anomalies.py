import matplotlib.pyplot as plt

def graph_ride_anomalies(df, df_stats, number_of_ride_files, value_to_sort, rows,cols):
    '''
    Returns a plot with ride(s) and power / heart rate development

            Parameters:
                    df: pandas DataFrame object
                    df_stats: df_stats (ride level statistics) pandas DataFrame object
                    number of files (int): number of ride files to display
                    values to sort (int): variable name plot top number of files
                    rows (int): number of rows in plot (rows * cols = number of files)
                    cols (int): number of columns in plot (rows * cols = number of files)
            Returns:
                    plot: matplotlib object with heart rate and power
    '''
            
    lijst = df_stats.sort_values(by=[value_to_sort], ascending = False).head(number_of_ride_files).filename.tolist()
    
    grouped = df[df['filename'].isin(lijst)][['filename','hr','watts','secs']].groupby('filename',sort=False)
    
    ncols = cols
    nrows = rows
       
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20,8), sharey=False)
    for (key, ax) in zip(grouped.groups.keys(), axes.flatten()):
        grouped.get_group(key).plot(x='secs', y=['watts','hr'],  ax=ax)
        #grouped.get_group(key).plot(x='secs', y=['watts'], ax=ax.twinx(), color='b', alpha=0.3)
        ax.legend().set_visible(False)
        ax.set_title(grouped.get_group(key).filename.unique());
    
    fig.suptitle('Plots of example rides with {}'.format(value_to_sort) , fontsize=16) 
    
    handles, labels = ax.get_legend_handles_labels()
    #fig.legend(handles, labels, loc='best', frameon=False, ncol=2, fontsize=14)
    plt.legend(bbox_to_anchor=(1, -0.15), loc='best', ncol=2)
    #lower center    
    plt.tight_layout()
    fig.subplots_adjust(top=0.91)
    
    return plt.show()