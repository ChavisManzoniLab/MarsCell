import os
import yaml

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))
print(script_directory)
tapas_directory = os.path.join(script_directory, "..", "TAPAS_scripts")
def save_project_data(data, filename= os.path.join(script_directory, "..","MarCell_data.yaml")):
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def load_project_data(filename=os.path.join(script_directory, "..","MarCell_data.yaml")):
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
loaded_data = load_project_data()
keysList = list(loaded_data['convention']['test'])


print(keysList)
