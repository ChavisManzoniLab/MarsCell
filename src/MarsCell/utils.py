import os
import yaml

def initialisation():

    def save_project_data(data, filename):
        with open(filename, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

    root = os.path.expanduser('~')

    marscell_data_path = os.path.join(root, "data","MarCell_data.yaml")

    # Save the data to YAML
    if not os.path.isdir(marscell_data_path):
        print(not os.path.isdir(marscell_data_path))
        tapas_path = os.path.join(root, 'data')

        project_info = {
            "name": "MarsCell",
            "description": "This is a storage file for data useful to MarsCell.",
            "convention": {
            },
            "tapas_path": tapas_path,
            "cellpose_model": "runCellpose2D-reelin-2023bat.bat",
        }
        save_project_data(project_info)
        print('Data file created')
    else:
        print('...')


    
