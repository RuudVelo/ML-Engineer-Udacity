import random
import matplotlib.pyplot as plt

def simple_ride_plots(df, number_of_ride_files = 4, nrows = 2, ncols = 2):
    '''
    Returns a plot with random ride(s) and power / heart rate / cadence development

            Parameters:
                    df : pandas DataFrame object
                    number_of_ride_files (int): number of random ride files to plot, default = 4
                    rows (int): number of rows in plot (rows * cols = number of files), default = 2 
                    cols (int): number of columns in plot (rows * cols = number of files), default = 2
            Returns:
                    plot: matplotlib object with heart rate and predicted heart rate
    '''
       
    lijst = random.sample(df.filename.unique().tolist(), number_of_ride_files)

    grouped = df[df['filename'].isin(lijst)][['filename','hr','watts','cad','secs']].groupby('filename',sort=False)
    
    ncols = ncols
    nrows = nrows
       
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20,12), sharey=False)
    for (key, ax) in zip(grouped.groups.keys(), axes.flatten()):
        grouped.get_group(key).plot(x='secs', y=['hr'],  ax=ax, color='r', alpha=0.8)
        grouped.get_group(key).plot(x='secs', y=['watts'], ax=ax.twinx(), color='b', alpha=0.3)
        grouped.get_group(key).plot(x='secs', y=['cad'], ax=ax, color='g', alpha=0.6)

        ax.set_title(grouped.get_group(key).filename.unique());
        ax.set_xlabel('secs')
        handles, labels = ax.get_legend_handles_labels()
        fig.suptitle('Plots of example rides', fontsize=16) 

    
    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    
    return plt.show()