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
    print('Startup')


    
