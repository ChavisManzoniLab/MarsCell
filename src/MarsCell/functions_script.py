import pandas as pd
import time
import os

def initialisation(path_to_folder, name_extraction):
    '''
    Creates the directory of the project with the path specified and the name of the project.
    The ImageJ raw data from extraction will be saved in 4 folders : calibration, coordinates, volume and intensity (and distance from a line if chosen).
    '''
    path_name = os.path.join(path_to_folder,name_extraction)

    #Create a folder for the project
    try:
        os.makedirs(path_name)
    except FileExistsError as fe:
        print("The folder \"%s\" already exists"%name_extraction)
        return fe
    folders_name = ["calibration", "coordinates", "distance", "volume", "intensity", "combined_csv"]
    for folder in folders_name:
        os.mkdir(os.path.join(path_name,folder))

def change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement):
    """
    Changes a path in a TAPAS script.
    The function detects a line that start with the specified pattern, and then change the line below with the right path.
    """
    with open(os.path.join(path_to_tapas_scripts, tapas_file), "r") as file:
        lines = file.readlines()

    # Modify the lines that start with the specified pattern
    for i, line in enumerate(lines):
        if line.startswith(pattern):
            # Replace the line with the new content
            lines[i+1] = text_replacement

    # Write the modified lines back to the file
    with open(os.path.join(path_to_tapas_scripts, tapas_file), "w") as file:
        file.writelines(lines)


def initialise_project(path_to_tapas_scripts, specify_channel, scale_x, scale_y,zMin,zMax, path_to_folder, name_extraction, cellpose_name, path_model, dataset_name):
        try:
            initialisation(path_to_folder, name_extraction)
        except FileExistsError as fe:
            print("The folder \"%s\" already exists"%name_extraction)
        except Exception: pass

        change_channel(path_to_tapas_scripts, specify_channel)
        tapas_file = '01_tapas-preprocess.txt'
        pattern = 'process:scale'
        text_replacement = 'scalex:'+str(scale_x)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = 'scalex:'+str(scale_x)
        text_replacement = 'scaley:'+str(scale_y)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)
    
        pattern = 'process:cropZ'
        text_replacement = 'zMin:'+str(zMin)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = 'zMin:'
        text_replacement = 'zMax:'+str(zMax)+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = 'process:createDataset'
        text_replacement = 'datasetName:?dataset?-'dataset_name+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = 'process:output'
        text_replacement = 'dataset:?dataset?-'dataset_name+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


        tapas_file = '02a_tapas-cellpose.txt'
        pattern = "process:calibration"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\calibration\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


        pattern = "process:exe"
        text_replacement = 'dir:'+path_model + " \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = "//name"
        text_replacement = 'file:'+cellpose_name + " \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = 'process:input'
        text_replacement = 'dataset:?dataset?-'dataset_name+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = 'process:output'
        text_replacement = 'dataset:?dataset?-'dataset_name+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        tapas_file = 'all_measures_local.txt'
        pattern = "//distline"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\distance\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


        pattern = "//coord"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\coordinates\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


        pattern = "//volume"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\volume\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

  
        pattern = "//intensity"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\intensity\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


        pattern = "//calibration"
        text_replacement = 'dir:'+path_to_folder+"\\"+name_extraction+"\\calibration\ \n"
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


        pattern = 'process:input'
        text_replacement = 'dataset:?dataset?-'dataset_name+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = 'process:link'
        text_replacement = 'dataset:?dataset?-'dataset_name+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)

        pattern = '//second input'
        text_replacement = 'dataset:?dataset?-'dataset_name+'\n'
        change_path(path_to_tapas_scripts, tapas_file, pattern, text_replacement)


def change_channel(path_to_tapas_scripts, specify_channel):
    '''
    Selects the channel to be processed
    '''
    # Define the directory containing the files and the base string to find and replace
    directory_path = path_to_tapas_scripts

    # Get the list of files in the directory
    file_list = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    file_list = [f for f in file_list if ".txt" in f]
    print(file_list)
    # Create a list of possible channel strings : if you have more channels add them to the list
    channel_options = ['channel:1', 'channel:2', 'channel:3', 'channel:4']

    # Iterate over each file
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        
        # Step 1: Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Step 2: Replace the first found channel option with the specified channel
        updated_content = content
        for channel in channel_options:
            if channel in updated_content:
                updated_content = updated_content.replace(channel, specify_channel, 1)
                break

        # Step 3: Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)



def extract(path_to_folder, name_extraction, separator, structure, ROI, threshold = 500):
    """
    Combines the raw data from ImageJ to make a unique CSV per image.
    Then all the unique CSV are merged into the project CSV, with only the cells that are in the ROI.
    Some useful data is also computed: volumic density of cells and distance binning.
    """

    
    err_ROI = 0

    path_name = os.path.join(path_to_folder, name_extraction) #path to the project folder 
    print(path_name)


    #1. We start by accessing the calibration data

    calib_path = os.path.join(path_name, "calibration")
    if os.path.isdir(calib_path):
        calib_files = [f for f in os.listdir(calib_path) if f.endswith(".txt")]
        if not calib_files:
            print("No calibration files found. You may have run ImageJ extraction with wrong saving path.")
            return
    else:
        print("The path to the calibration files do not exist, the project's folder may have not been correctly created")
        return
    
    
    calib_df = pd.DataFrame(columns = ["imageLabel","Z-Section", "PixelSize_Z", "Height", "pix_to_micron"] )

  
    for n, calib_txt in enumerate(calib_files):
        txt_path=os.path.join(calib_path,calib_txt)
        try:
            
            with open(txt_path, "r") as file:
                calib_data = file.read()

            split1 = calib_data.split("\n")

            #Number of slices in the stack
            N_slices = int(split1[0].split(":")[-1])

            split2 = split1[1].split(":")

            #Z size of voxel
            Z_res = float(split2[-1].split(" ")[0])
            height = Z_res*N_slices

            #Pixel to micron conversion factor (X, Y)
            pix_to_micron = float(split2[0])

            #Saving the data in a dataframe
            calib_df.loc[n, "imageLabel"] = calib_txt.split('-')[0]+"-seg.tif"
            calib_df.loc[n, "Z-Section"] = N_slices
            calib_df.loc[n, "PixelSize_Z"] = Z_res
            calib_df.loc[n, "Height"] = height
            calib_df.loc[n, "pix_to_micron"] = pix_to_micron

        except FileNotFoundError:
            print(f"File not found: {txt_path}")
        except ValueError as ve:
            print(f"Value error for file {txt_path}: {ve}")
        except Exception as e:
            print(f"An error occurred while processing file {txt_path}: {e}")

    #saving the dataframe to a csv
    calib_df.to_csv(os.path.join(path_name, "calibration_data.csv"))

    #merging all the csv related to an image into one

    coord_path=os.path.join(path_name,'coordinates')
    
    if os.path.isdir(coord_path):
        coords_csv = [f for f in os.listdir(coord_path) if f.endswith(".csv")] 
        if not coords_csv:
            print("No coordinates files found. You may have run ImageJ extraction with wrong saving path.")
            return
    else:
        print("The path to the coordinates files do not exist, the project's folder may have not been correctly created")
        return
    for csv in coords_csv:
        
        name = csv.rsplit('-', 1)[0]

        print('Merging csv for the image %s'%name)
        
        coords = pd.read_csv(os.path.join(coord_path, csv))
        #merging the calibration data
        df = pd.merge(coords, calib_df, on = 'imageLabel')

        #merging the cells' volume data
        volume_path=os.path.join(path_name,"volume",name+'-volume.csv')
        if os.path.exists(volume_path):
            df_volume =  pd.read_csv(volume_path)
            df_volume=df_volume.drop(columns=['imageLabel'])
            df = pd.merge(df,df_volume, on = 'Label', how = 'left')
        elif os.path.exists(os.path.join(path_name,"volume",name+'-volumeReelin.csv')):
            volume_path=os.path.join(path_name,"volume",name+'-volumeReelin.csv')
            df_volume =  pd.read_csv(volume_path)
            df_volume=df_volume.drop(columns=['imageLabel'])
            df = pd.merge(df,df_volume, on = 'Label', how = 'left')
        else:
            print('There was a problem while accessing the volume data of %s'%name)

        #merging the cells' intensity data
        intensity_path=os.path.join(path_name, 'intensity',name+'-quantif.csv')
        if os.path.exists(intensity_path):
            df_intensity = pd.read_csv(intensity_path)
            df_intensity=df_intensity.drop(columns=['imageLabel'])
            df = pd.merge(df,df_intensity, on = 'Label', how = 'left')
        elif os.path.exists(os.path.join(path_name, 'intensity',name+'-quantifReelin.csv')):
            intensity_path=os.path.join(path_name, 'intensity',name+'-quantifReelin.csv')
            df_intensity = pd.read_csv(intensity_path)
            df_intensity=df_intensity.drop(columns=['imageLabel'])
            df = pd.merge(df,df_intensity, on = 'Label', how = 'left')
        else:
            print('There was a problem while accessing the intensity data of %s'%name)
        print(ROI)
        #Calculating the distances of the cells to a line
        if ROI=='line':
            distance_path = os.path.join(path_name, "distance", name+'-distanceLine.csv')
            if os.path.exists(distance_path):
                df_distance  = pd.read_csv(distance_path)
                df = pd.merge(df, df_distance, on='Label')
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
                    df = df.loc[df['pos']==-1.0].copy()
                else :
                    df = df.loc[df['pos']==1.0].copy()

                #converting the distannce from pixels to microns
                df['distUnit'] = df['distPix']*pix_to_micron

                #removing the cells outside the region of insterest
                df = df.drop(df[df['distUnit']>threshold].index)
                df = df.drop(df[df['Cy_Pix']<ymin].index)
                df = df.drop(df[df['Cy_Pix']>ymax].index)
                
                #volumic density calculation
                df['volume_roi'] = df['length']*threshold*df['Height']
                n = len(df)
                df['volumic_density'] = n/df['volume_roi']*1000000 #Unit : (100µm)^3

            else: 
                err_ROI = 1
                print('No distance file found for %s'%name)

        try:
            df = df.drop(columns=['imageLabel', 'imageSignal', 'imageLabel_y','pos', 'segment'])
        except: pass

        df.to_csv(path_name+"\combined_csv"+"\\%s.csv"%name)
        

    
    #access to the combined csv 
    path_to_results = path_name+"\combined_csv"
    analysed_csv = os.listdir(path_to_results)
    list_df = []

    #Retrieving the information that are in the title of the image
    for i, csv in enumerate(analysed_csv):
        try:
            infos = csv.split(separator)
        except: return "Cannot split %s with separator %s"%(analysed_csv, separator)
        results = pd.read_csv(path_to_results +"\\"+csv)
        for i, item in enumerate(structure):
            try:
                results[item.strip()] = infos[i]
            except:
                print("No %s in %s"%(item, csv))
                results[item] = 'NA'
        list_df.append(results)
        

    datafff = pd.concat(list_df)
    #binning step
    if ROI == 'line' and err_ROI==0:   
        bins = [0, 120, 200,300, 500]

        #binning the distance
        datafff['bins'] = pd.cut(datafff['distUnit'], bins)

    timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
    
    try:
        datafff.rename(columns={"Mean": "mean_intensity", "Min" : "min_intensity", "Max" : "max_intensity", "StdDev" : "intensity_sd", "Sum": "voxel_intensity_sum"}, inplace=True)
    except:pass
    datafff.to_csv(path_name+"\\extraction_"+timestr+".csv")
    print('Saved the csv with all the data')



