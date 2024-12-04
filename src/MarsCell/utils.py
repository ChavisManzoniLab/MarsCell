import os
import yaml
import sys

def initialisation():
    '''
    Creates a YAML file to store useful data for MarsCell: naming convention, path to TAPAS files, the Cellpose model to use
    '''

    root = os.path.dirname(__file__)
    marscell_data_path = os.path.join(root, "data","MarsCell_data.yaml")
    
    if not os.path.isfile(marscell_data_path):

        #function to save data file as yaml
        def save_project_data(data, filepath):
            with open(filepath, 'w') as file:
                yaml.dump(data, file, default_flow_style=False)

        print('No data file found. Creating one...')

        data_path = os.path.join(root, 'data')


        #setting the right paths to run cellpose
        runcellpose_path = os.path.join(data_path, "runCellpose.bat")
        venv_path = sys.prefix
        venv_path = os.path.join(venv_path, 'Scripts', 'python')
        model_path = os.path.join(data_path, 'Reelin_P40_advanced')
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
            "tapas_path": data_path,
            "cellpose_model": "runCellpose.bat",
        }
        save_project_data(project_info, marscell_data_path)
        print('Data file created')
    else:
        print('Launching ...')


    
