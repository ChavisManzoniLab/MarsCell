# Methodology

## Description

This workflow is based on TAPAS, an ImageJ plugin, completed with Cellpose, an automatic cell-segmentation tool, and a Jupyter Notebook to ensure accessibility. TAPAS allows the user to create a personalized image analysis pipeline by linking modules. Each module performs a simple process and is assembled in a simple text file.

## Step by Step Process

### 1. Set Up

#### Downloads

Please download the folder from our repository [xxxx](URL).

Make sure that the following are installed:
- **Fiji**: [https://imagej.net/software/fiji/](https://imagej.net/software/fiji/)
- **TAPAS**: [https://imagej.net/plugins/tapas](https://imagej.net/plugins/tapas)
- **A Python environment** with the packages in `requirements.txt` installed.

Save the Jupyter notebook and the `functions_script.py` file in the same folder. The notebook will be used to help with the initialization of the workflow and to format data. The `functions_script.py` file contains all the functions used in the notebook.

In the `TAPAS_scripts` folder, each text document is used to run a specific process in Fiji. The file `subprocess.txt` allows you to run multiple processes at once, so that you do not have to manually launch each process one after the other.

The `run_cellpose.bat` file is used to launch Cellpose with the provided model. You must change the paths in this file. To proceed, right-click on the file, then “Show more options”, then “Edit”.

First, put the path to your Python environment where Cellpose is installed. If you used Anaconda to install Cellpose, it should look like this:
