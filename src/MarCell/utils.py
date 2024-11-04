import os
import requests
import yaml
from os.path import expanduser

def download_files_from_github(folder_path):
    # Example GitHub URL - adjust to match your file structure
    file_url = "https://github.com/ChavisManzoniLab/MarCell/tree/main/TAPAS_scripts"
    file_name = "downloaded_file.ext"  # Adjust filename and extension
    file_path = os.path.join(folder_path, file_name)
    
    print(f"Downloading file from {file_url}...")
    response = requests.get(file_url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"File '{file_name}' downloaded successfully.")
    else:
        print("Failed to download file. Status code:", response.status_code)
        raise Exception("Failed to download files from GitHub.")

def initialisation():
    
    home = expanduser("~")
    folder_name='MarCell'
    folder_path=os.path.join(home, folder_name)
    if not os.path.isdir(folder_path):
        print('Creating MarCell folder')
        os.makedirs(os.path.join(folder_path, 'TAPAS_scripts'))
        os.makedirs(os.path.join(folder_path, 'Notebooks'))
        

def ensure_folder_exists():
    print('a')


    
def ho():
    print('hiiiii')