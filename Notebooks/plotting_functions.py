import pandas as pd
import math as m
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

from statannot import add_stat_annotation
import matplotlib

pix_to_micron = 0.1559814453125*2 #conversion factor

colors = ['#000000','#FC8608','#0379F7']
customPalette = sns.set_palette(sns.color_palette(colors))

def letter_annotation(ax, xoffset, yoffset, letter):
        ax.text(xoffset, yoffset, letter, transform=ax.transAxes,
                size=12, weight='bold')
        
def custom_boxplot(data, x, y, ax, letter='', palette = customPalette, title = None, xlabel = None, ylabel = None, stat = True , pairs =[("Naive", "Win"), ("SRWin", "Naive"), ("SRWin", "Win")]):

        
    plot = sns.boxplot(data=data, 
                            x=x, 
                            y = y,
                            showfliers = False, 
                            width=0.4, 
                            palette=palette,
                            ax=ax,)
    sns.stripplot(data = data, 
                x = x,
                y = y,
                palette=sns.color_palette(),
                alpha = 0.3,
                ax=ax)
    ax.set(title = title, xlabel = xlabel, ylabel = ylabel)
    box_patches = [patch for patch in ax.patches if type(patch) == matplotlib.patches.PathPatch]
    if len(box_patches) == 0:  # in matplotlib older than 3.5, the boxes are stored in ax2.artists
        box_patches = ax.artists
    num_patches = len(box_patches)
    lines_per_boxplot = len(ax.lines) // num_patches
    for i, patch in enumerate(box_patches):
        # Set the linecolor on the patch to the facecolor, and set the facecolor to None
        col = patch.get_facecolor()
        patch.set_edgecolor(col)
        patch.set_facecolor('None')

        # Each box has associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same color as above
        for line in ax.lines[i * lines_per_boxplot: (i + 1) * lines_per_boxplot]:
            line.set_color(col)
            line.set_mfc(col)  # facecolor of fliers
            line.set_mec(col)  # edgecolor of fliers
    if stat:
        add_stat_annotation(plot, data=data, x=x, y=y, 
                            comparisons_correction = None,
                            box_pairs=pairs,
                            test='Mann-Whitney', 
                            text_format='star', 
                            loc='inside', 
                            verbose=2)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['bottom'].set_color('black')

    ax.spines['left'].set_linewidth(1.5)
    ax.spines['left'].set_color('black')
    sns.set_style("ticks")
    letter_annotation(ax, -0.09, 1.05, letter)


def displot_3D(df, title): #create a 3D plot of cell density / distance to the line and along Bregma_coords
    kde = gaussian_kde([df['distUnit'], df['Bregma_coord']], bw_method=0.3)
    x_grid, y_grid = np.meshgrid(np.linspace(df['distUnit'].min(), df['distUnit'].max(), 100),
                                np.linspace(df['Bregma_coord'].min(), df['Bregma_coord'].max(), 100))
    z = np.reshape(kde([x_grid.flatten(), y_grid.flatten()]), x_grid.shape)
    fig = go.Bregma_coord(data=[go.Surface(z=z, x=x_grid, y=y_grid)])
    fig.update_layout(scene=dict(xaxis_title='Distance (µm)', yaxis_title='Bregma_coord', zaxis_title='Density'), title=title)
    fig.show()


def bin_count_fn(dataframe):
    bin_count = {'Naive' : [], 'Win' : [], 'SRWin' : []}

    for temp in (pd.unique(dataframe['Condition'])):
        print(temp)
        bin_count[temp] = pd.DataFrame(dataframe[dataframe['Condition']==temp].groupby(['imageLabel_x','ID', 'Bregma_coord','Height', 'length','bins'])['bins'].count())

    bin_count['Win']['Condition']= 'Win'
    bin_count['Naive']['Condition']= 'Naive'
    bin_count['SRWin']['Condition']= 'SRWin'
    grouped_dataframe2 = pd.concat([bin_count['Naive'],bin_count['Win'], bin_count['SRWin']])
    grouped_dataframe2.to_csv(r"C:\Users\Thenzing\Julien\TAPAS-Thomas\data_allcells\groupey.csv")
    #passage en csv puis rechargement du fichier pour contourner pb de mise en forme
    bin_count = pd.read_csv(r"C:\Users\Thenzing\Julien\TAPAS-Thomas\data_allcells\groupey.csv")
    bin_count = bin_count.pivot_table(
        index = ['imageLabel_x','ID', 'Bregma_coord','Condition', 'Height', 'length'], 
        columns = 'bins', 
        values = 'bins').reset_index()
    bin_count['volumic_density_layer1'] = bin_count['(0, 120]']/(120*bin_count['length']*pix_to_micron*bin_count['Height'])*1000000 #unit is a 100µm cube
    bin_count['volumic_density_layer23'] = bin_count['(120, 270]']/(150*bin_count['length']*pix_to_micron*bin_count['Height'])*1000000 #unit is a 100µm cube
    bin_count['volumic_density_layer56'] = bin_count['(270, 500]']/(230*bin_count['length']*pix_to_micron*bin_count['Height'])*1000000 #unit is a 100µm cube
    bin_count['volumic_density_total'] = (bin_count['(270, 500]']+ bin_count['(120, 270]']+bin_count['(0, 120]'])/(500*bin_count['length']*pix_to_micron*bin_count['Height'])*1000000 #unit is a 100µm cube
    return bin_count

def mean_density_fn(dataframe):
    mean_density = pd.DataFrame(dataframe.groupby(['ID', 'Condition'])['volumic_density_layer1','volumic_density_layer23','volumic_density_layer56','volumic_density_total'].mean()).reset_index()
    mean_density['Condition'] = pd.Categorical(mean_density['Condition'], categories = ['Naive', 'Win', 'SRWin'], ordered=True)
    return mean_density

def figs(bin_count):
    fig910 = bin_count[(bin_count['Bregma_coord']==2.58) | (bin_count['Bregma_coord']==2.46)]
    fig910 = pd.DataFrame(fig910.groupby(['ID', 'Condition'])['volumic_density_total'].mean()).reset_index()
    fig910['Condition'] = pd.Categorical(fig910['Condition'], categories = ['Naive', 'Win', 'SRWin'], ordered=True)

    fig1112 = bin_count[(bin_count['Bregma_coord']==2.34) | (bin_count['Bregma_coord']==2.22)]
    fig1112 = pd.DataFrame(fig1112.groupby(['ID', 'Condition'])['volumic_density_total'].mean()).reset_index()
    fig1112['Condition'] = pd.Categorical(fig1112['Condition'], categories = ['Naive', 'Win', 'SRWin'], ordered=True)

    fig13 = bin_count[bin_count['Bregma_coord']==2.10]
    fig13 = pd.DataFrame(fig13.groupby(['ID', 'Condition'])['volumic_density_total'].mean()).reset_index()
    fig13['Condition'] = pd.Categorical(fig13['Condition'], categories = ['Naive', 'Win', 'SRWin'], ordered=True)

    fig1415 = bin_count[(bin_count['Bregma_coord']==1.98) | (bin_count['Bregma_coord']==1.94)]
    fig1415 = pd.DataFrame(fig1415.groupby(['ID', 'Condition'])['volumic_density_total'].mean()).reset_index()
    fig1415['Condition'] = pd.Categorical(fig1415['Condition'], categories = ['Naive', 'Win', 'SRWin'], ordered=True)
    return(fig910, fig1112, fig13, fig1415)