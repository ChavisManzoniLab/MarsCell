import pandas as pd
import math as m
import numpy as np
from os import listdir, mkdir
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
from plotly.subplots import make_subplots
import time


def initialisation(path_to_folder, name_extraction):
    '''
    Creates the directory of the project with the path specified and the name of the project.
    The ImageJ raw data from extraction will be saved in 5 folders : calibration, coordinates, distance, volume and intensity.
    '''
    path_name = path_to_folder+"\\"+name_extraction+"\extraction_data"

    #Create a folder for the project
    try:
        mkdir(path_to_folder+"\\"+name_extraction)
    except:
        return "The folder \"%s\" already exists"%name_extraction
    mkdir(path_name)
    folders_name = ["calibration", "coordinates", "distance", "volume", "intensity", "combined_csv"]
    for folder in folders_name:
        mkdir(path_name+"\\"+folder)

def change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement):
    """
    This function allows to automatically change the path used by the TAPAS script.
    The function detects the line that start with the specified pattern, and then change the next line with the right path.
    """
    with open(path_to_tapas_scripts + "\\"+tapas_file, "r") as file:
        lines = file.readlines()

    # Modify the lines that start with the specified pattern
    for i, line in enumerate(lines):
        if line.startswith(pattern):
            # Replace the line with the new content
            lines[i+1] = text_replacement

    # Write the modified lines back to the file
    with open(path_to_tapas_scripts + "\\"+tapas_file, "w") as file:
        file.writelines(lines)

def extract(path_to_folder, name_extraction, separator, structure, threshold = 500):
    """
    Combines the raw data from ImageJ to make a unique CSV per image.
    Then all the unique CSV are merged into the project CSV, with only the cells that are in the ROI.
    Some useful data is also computed: volumic density of cells and distance binning.
    """

    path_name = path_to_folder+"\\"+name_extraction+"\extraction_data"

    #1. Access to the calibration data
    calib_path = path_name+"\calibration"
    calib_files = listdir(calib_path)
    calib_df = pd.DataFrame(columns = ["imageLabel_x","Z-Section", "PixelSize_Z", "Height", "pix_to_micron"] )
    
    for n, calib_txt in enumerate(calib_files):
        data = open(calib_path + "\\"+calib_txt, "r").read()
        split1 = data.split("\n")

        #Number of slices in the stack
        N_slices = int(split1[0].split(":")[-1])

        split2 = split1[1].split(":")

        #Z size of voxel
        Z_res = float(split2[-1].split(" ")[0])
        height = Z_res*N_slices

        #Pixel to micron conversion factor (X, Y)
        pix_to_micron = float(split2[0])

        #Saving the data in a dataframe
        calib_df.loc[n, "imageLabel_x"] = calib_txt.split('-')[0]+"-seg.tif"
        calib_df.loc[n, "Z-Section"] = N_slices
        calib_df.loc[n, "PixelSize_Z"] = Z_res
        calib_df.loc[n, "Height"] = height
        calib_df.loc[n, "pix_to_micron"] = pix_to_micron
        print(type(pix_to_micron), pix_to_micron)

    #saving the dataframe to a csv
    calib_df.to_csv(path_name+"\calibration_data.csv")
    
    distance_csv = listdir(path_name + "\distance")

    for csv in distance_csv:
        
        name = csv.split('-')[0]
        print(name)
        data  = pd.read_csv(path_name + "\\distance\\"+csv)
        coords = pd.read_csv(path_name + "\\coordinates\\"+name+'-centroid.csv')

        #merging the distance and coordinates data
        df = pd.merge(data, coords, on='Label')
        #merging the calibration data
        df = pd.merge(df, calib_df, on = 'imageLabel_x')


        #scaling coordinates of extremum of the line
        df['P1x'] = df['P1x']/2
        df['P1y'] = df['P1y']/2
        df['P2x'] = df['P2x']/2
        df['P2y'] = df['P2y']/2

        #storing coordinates of extremum of the line
        y1 = df.loc[0,'P1y']
        y2 = df.loc[0,'P2y']

        ymin = min(y1, y2) 
        ymax = y1+y2-ymin
        
        #Selection of the cell that are in the proper side of the segment
        if df.iloc[1]['side']==2:
            df_distance = df.loc[df['pos']==-1.0].copy()
        else :
            df_distance = df.loc[df['pos']==1.0].copy()

        #converting the distannce from pixels to microns
        df_distance['distUnit'] = df_distance['distPix']*pix_to_micron

        #removing the cells outside the region of insterest
        df_distance = df_distance.drop(df_distance[df_distance['distUnit']>threshold].index)
        df_distance = df_distance.drop(df_distance[df_distance['Cy_Pix']<ymin].index)
        df_distance = df_distance.drop(df_distance[df_distance['Cy_Pix']>ymax].index)
        
        #volumic density calculation
        df_distance['volume_roi'] = df_distance['length']*threshold*df_distance['Height']
        n = len(df_distance)
        df_distance['volumic_density'] = n/df_distance['volume_roi']*1000000 #Unit : (100µm)^3

        #merging the cells' volume data.
        df_volume =  pd.read_csv(path_name + "\\volume\\"+name+'-volumeReelin.csv')
        df3 = df_distance.merge(df_volume, on = 'Label', how = 'left')
        #merging the cells' intensity data
        df_intensity = pd.read_csv(path_name + "\\intensity\\"+name+'-quantifReelin.csv')
        df_intensity=df_intensity.drop(columns=['imageLabel'])
        df_final = df3.merge(df_intensity, on = 'Label', how = 'left')
        df_final = df_final.drop(columns=['imageLabel', 'imageSignal', 'imageLabel_y','pos', 'segment'])

        df_final.to_csv(path_name+"\combined_csv"+"\\%s.csv"%name)
        
#binning step
    #access to the combined csv 
    path_to_results = path_name+"\combined_csv"
    analysed_csv = listdir(path_to_results)
    list_df = []

    #Retrieving the information that are in the title of the image
    for i, csv in enumerate(analysed_csv):
        try:
            infos = csv.split(separator)
        except: return "Cannot split %s with separator %s"%(analysed_csv, separator)
        results = pd.read_csv(path_to_results +"\\"+csv)
        for i, item in enumerate(structure):
            try:
                results[item] = infos[i]
            except:
                print("No %s in %s"%(item, csv))
                results[item] = 'NA'
        list_df.append(results)
        

    datafff = pd.concat(list_df)
    
    #bins = [50*i for i in range(12)]
    bins = [0, 120, 270, 500]

    #binning the distance
    datafff['bins'] = pd.cut(datafff['distUnit'], bins)
    datafff['ID'] = datafff['Batch']+datafff['Ori']+datafff['Condition']
    timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
    

    datafff.rename(columns={"Mean": "mean_intensity", "Min" : "min_intensity", "Max" : "max_intensity", "StdDev" : "intensity_sd", "Sum": "voxel_intensity_sum"}, inplace=True)
    datafff.to_csv(path_name+"\\extraction_"+timestr+".csv")



def extract_sex(df): #returns a dataframe for each sex
    males = df.loc[df['Sex']=='M'].copy()
    females = df.loc[df['Sex']=='F'].copy()
    return males, females


def extract_conditions(df): #returns a dataframe for each condition
    naive = df.loc[df['Condition']=='Naive'].copy()
    #veh = df.loc[df['Condition']=='Veh'].copy()
    srwin = df.loc[df['Condition']=='SRWin'].copy()
    win = df.loc[df['Condition']=='Win'].copy()

    return naive, srwin, win


def extract_figures(df): #returns a dataframe for each figure
    fig9 =  df.loc[df['Figure']==9].copy()
    fig10 =  df.loc[df['Figure']==10].copy()
    fig11 =  df.loc[df['Figure']==11].copy()
    fig12 =  df.loc[df['Figure']==12].copy()
    fig13 =  df.loc[df['Figure']==13].copy()
    fig14 =  df.loc[df['Figure']==14].copy()
    fig15 =  df.loc[df['Figure']==15].copy()

    return fig9, fig10, fig11, fig12, fig13, fig14, fig15


def distribution_plot(df): 
    sns.displot(df, x="distUnit", hue="Condition", kind="kde", multiple="stack", common_norm=False, bw_adjust=0.4)
    plt.show()


def displot_3D(df, title): #create a 3D plot of cell density / distance to the line and along figures
    kde = gaussian_kde([df['distUnit'], df['Figure']], bw_method=0.3)
    x_grid, y_grid = np.meshgrid(np.linspace(df['distUnit'].min(), df['distUnit'].max(), 100),
                                np.linspace(df['Figure'].min(), df['Figure'].max(), 100))
    z = np.reshape(kde([x_grid.flatten(), y_grid.flatten()]), x_grid.shape)
    fig = go.Figure(data=[go.Surface(z=z, x=x_grid, y=y_grid)])
    fig.update_layout(scene=dict(xaxis_title='Distance (µm)', yaxis_title='Figure', zaxis_title='Density'), title=title)
    fig.show()