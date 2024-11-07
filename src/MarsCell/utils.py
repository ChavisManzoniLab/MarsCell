import os
import requests
import yaml
from os.path import expanduser
import fsspec
import pathlib


def download_files_from_github(folder_path):
    destination = pathlib.Path(__file__).parent.resolve() / "test_folder_copy"
    destination.mkdir(exist_ok=True, parents=True)
    fs = fsspec.filesystem("github", org="ChavisManzoniLab", repo="MarCell")
    fs.get(fs.ls("TAPAS_scripts/"), destination.as_posix())

def initialisation():

    home = os.path.expanduser('~')
    folder_name='MarsCell'
    folder_path=os.path.join(home, folder_name)
    tapas_directory=os.path.join(folder_path, 'TAPAS_scripts')
    notebooks_directory = os.path.join(folder_path, 'Notebooks')
    if not os.path.isdir(folder_path):
        print('Creating MarCell folder')
        
        os.makedirs(tapas_directory)
        
        os.makedirs(notebooks_directory)

    tapas_directory = os.path.join(home, "..", "TAPAS_scripts")
    destination = tapas_directory
    """fs = fsspec.filesystem("github", org="ChavisManzoniLab", repo="MarCell")
    fs.get(fs.ls("TAPAS_scripts/"), destination)"""
    
    fs = fsspec.filesystem("github", org="ChavisManzoniLab", repo="MarCell")
    fs.get(fs.ls("TAPAS_scripts/"), destination.as_posix())
    
    def save_project_data(data, filename= os.path.join(home, "..","MarCell_data.yaml")):
        with open(filename, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
            

    def load_project_data(filename=os.path.join(home,"MarCell_data.yaml")):
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        return data

    # Example project data
    project_info = {
        "name": "MarCell_data",
        "description": "This is a storage file for data useful to MarCell.",
        "convention": {
        },
        "tapas_path": tapas_directory,
        "cellpose_model": "runCellpose2D-reelin-2023bat.bat",
    }

    # Save the data to YAML
    """if not os.path.isdir(os.path.join(script_directory, "..","MarCell_data.yaml")):
        print(not os.path.isdir(os.path.join(script_directory, "..","MarCell_data.yaml")))
        save_project_data(project_info)
        print('saved')
    else:
        print('already a doc')"""

    # Load the data from YAML
    save_project_data(project_info)
        
initialisation()
