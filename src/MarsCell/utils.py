import os
import yaml
import sys
from tkinter import filedialog
import tkinter as tk
from shutil import copy2

def initialisation():
    '''
    Creates a YAML file to store useful data for MarsCell: naming convention, path to TAPAS files, the Cellpose model to use
    '''

    #function to save data file as yaml
    def save_project_data(data, filepath):
            with open(filepath, 'w') as file:
                yaml.dump(data, file, default_flow_style=False)


    root = os.path.dirname(__file__) #location where github data is 
    data_path = os.path.join(root, "data")
    tapas_install_path = os.path.join(root, "TAPAS_intallation")   

    
    user_folder_created = os.path.join(root, "data","created.yaml")
    print(user_folder_created)
    if not os.path.isfile(user_folder_created):
        def filepath_btn():
            file_path = filedialog.askdirectory(title="Select a Folder to Save Project")
            user_folder_path=file_path #creation of a folder for more convenient access to TAPAS files
            user_marscell_folder=os.path.join(user_folder_path, 'MarsCell')
            os.makedirs(user_marscell_folder)
            tapas_path=os.path.join(user_marscell_folder, "TAPAS")
            os.makedirs(tapas_path)
            models_path=os.path.join(user_marscell_folder, "Models")
            os.makedirs(models_path)
            install_path=os.path.join(user_marscell_folder, "TAPAS_installation")
            os.makedirs(install_path)

            print('TAPAS files tranfer...')
            for file in os.listdir(data_path):
                filetype=os.path.splitext(file)[1]
                if filetype=='.txt':
                    copy2(os.path.join(data_path, file), tapas_path)
                elif filetype=='.yaml':
                    copy2(os.path.join(data_path, file), user_marscell_folder)
                else:
                    copy2(os.path.join(data_path, file), models_path)
                
            print('TAPAS files transfered')

            print("TAPAS installation files transfer...")
            for file in os.listdir(tapas_install_path):
                if ".jar" in file:
                    copy2(os.path.join(tapas_install_path, file), install_path)
                elif file=="tapas":
                    tapas_plugin_path=os.path.join(install_path, "tapas")
                    os.makedirs(tapas_plugin_path)
                    for plugin_file in os.listdir(os.path.join(tapas_install_path,file)):
                        copy2(os.path.join(tapas_install_path, file, plugin_file), tapas_plugin_path)
                elif file=="mcib3d-suite":
                    suite3d_plugin_path=os.path.join(install_path, "mcib3d-suite")
                    os.makedirs(suite3d_plugin_path)
                    for plugin_file in os.listdir(os.path.join(tapas_install_path,file)):
                        copy2(os.path.join(tapas_install_path, file, plugin_file), suite3d_plugin_path)


            print('Setting paths for Cellpose...')
            #setting the right paths to run cellpose
            runcellpose_path = os.path.join(models_path, "runCellpose.bat")
            venv_path = sys.prefix
            venv_path = os.path.join(venv_path, 'Scripts', 'python')
            model_path = os.path.join(models_path, 'Reelin_P40_advanced')
            try:
                with open(runcellpose_path, 'r') as file:
                    filedata = file.read()
                if ('path_cellpose_env' and 'path_model_Reelin_P40_advanced') or (venv_path and model_path) in filedata:
                    filedata = filedata.replace('path_cellpose_env', venv_path)
                    filedata = filedata.replace('path_model_Reelin_P40_advanced', model_path)
                else:
                    print(f'Could not set paths automatically for Cellpose. Set the paths at {runcellpose_path}')

                with open(runcellpose_path, 'w') as file:
                    file.write(filedata)
            except Exception as e:
                print(e)

            #creating a data file to store title conventions, path to tapas files, name of the Cellpose model to run
            project_info = {
                "name": "MarsCell",
                "description": "This is a storage file for data useful to MarsCell.",
                "convention": {
                },
                "tapas_path": tapas_path,
                "cellpose_model": "runCellpose.bat",
            }
            marscell_data_path=os.path.join(user_marscell_folder, "MarsCell_data.yaml")
            save_project_data(project_info, marscell_data_path)
            print('Data file created')
            created = {"User folder created": "True",
                    "file_path":marscell_data_path}
            save_project_data(created, user_folder_created)
            window.destroy()

        print('First initalisation: creating a folder to store TAPAS files...')
        window = tk.Tk()
        window.geometry('400x200')
        window.title("MarsCell")
        welcome_label = tk.Label(window, text="Select a folder to initalise MarsCell", font=("ComicSansMS", 12))
        welcome_label.pack(pady=20)
        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)  # Add some padding above the frame
        path_button = tk.Button(button_frame, text="Initialize", command=filepath_btn)
        path_button.pack()
        window.mainloop()


    else:
        def load_project_data(filename):
            with open(filename, 'r') as file:
                data = yaml.safe_load(file)
            return data
        print('Launching ...')
        global data
        root = os.path.dirname(__file__)
        created_path=os.path.join(root,'data', 'created.yaml')#access the path of the MarsCell folder
        created = load_project_data(filename=created_path)
        data_path=created['file_path']


