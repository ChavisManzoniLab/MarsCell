import os
import requests

def ensure_folder_exists():
    folder_path = "path/to/your/folder"  # Update this path as needed

    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist. Creating folder...")
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
        download_files_from_github(folder_path)
    else:
        print(f"Folder '{folder_path}' already exists.")

def download_files_from_github(folder_path):
    # Example GitHub URL - adjust to match your file structure
    file_url = "https://github.com/username/repo/raw/main/path/to/file"
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
    
def ho():
    print('hiiiii')