# Methodology

## Description (to change)
MarsCell is an AI-based workflow for automated cell detection and quantification on confocal images.
It is based on TAPAS, an ImageJ plugin, completed with Cellpose, an automatic cell-segmentation tool, and a Jupyter Notebook to ensure accessibility to everyone.

## Step by Step Process

### 1. Set Up

#### Downloads

First, make sure that the following softwares are installed:
- **Fiji**: [https://imagej.net/software/fiji/](https://imagej.net/software/fiji/)
- **TAPAS**: [https://imagej.net/plugins/tapas](https://imagej.net/plugins/tapas)
- **Python 3.9**: [https://www.python.org/downloads/release/python-3913/](https://www.python.org/downloads/release/python-3913/)

Create a virtual environment   

Using venv:

```bash
python -m venv ENV_NAME
```
Using conda:

```bash
conda create -n ENV_NAME python=3.9 anaconda
```
Then run:
```bash
pip install git+https://github.com/ChavisManzoniLab/MarsCell.git
```
This will install all the required packages to run the notebook.

If error :
```bash
ModuleNotFoundError: No module named 'distutils'
```
run 
```bash
pip install setuptools
pip install git+https://github.com/ChavisManzoniLab/MarsCell.git
```

If error :
```bash
CondaSSLError
```
run
The notebook will be used to help with the initialisation of the workflow and to format data. 

In the `TAPAS_scripts` folder, each text document is used to run a specific process in Fiji. 
The file `subprocess.txt` allows to run multiple processes at once, so that you do not have to manually launch each process one after the other.

The `run_cellpose.bat` file is used to launch Cellpose with the provided model. You must change the paths in this file. To proceed, right-click on the file, then “Show more options”, then “Edit”.
First, put the path to your Python environment that you just created. 
The second path is to the Cellpose model you are going to use. You can use the model available in the github directory, or create a model that suits better your analysis workflow.

### 2. Initialization

#### 2.1 Upload

Upload your image stacks on OMERO, using OMERO.insight. The image processing handles one dataset at a time, so ensure that all the image stacks for a given project are included in the same dataset.

To obtain layer organization data (the distance of cells to a segment), you can draw a segment using the OMERO ROI interface. Please note that currently, the workflow only supports straight lines.

#### 2.2 Imports

Open the notebook using the Jupyter app on Anaconda or with a code editor like Visual Studio Code. In the Import section of the notebook, run the cell to import all the functions that we will need.

#### 2.3 Naming Convention

Specify the structure of the title of your images. Ensure that all your images follow the same naming convention to access information such as sex, age, condition. Indicate the separator used in your title to delimit the categories. Then, in the `structure` list, provide each category name in the order that they appear in the title.

Example:

```python
"""191001_B4_PPGI2_Naive_P35_M_C57_Rln_PFC1_FIG9_L.czi"""
separator = '_'
structure = ['Exp_Date', 'Batch', 'Ori', 'Condition', 'Age', 'Sex', 'Strain', 'Marker', 'Slide_Id', 'Atlas', 'Slide_side']
```

## 2.4 Setting the Paths

Enter the path where your project will be saved, then enter the name of the project. Run the initialization function that will create the directory for the project. Enter the path where your TAPAS scripts are stored and the name of your batch file that runs Cellpose. Run the cell to change the paths in the TAPAS files.

## 3. Image Processing with TAPAS and Cellpose

Open Fiji, and connect to OMERO through TAPAS in `Plugins > TAPAS > TAPAS CONNECT`. Then, launch the OMERO interface in `Plugins > TAPAS > TAPAS OMERO`. You should now be able to select a project and a dataset.

In the processing section, select the TAPAS file `subprocesses.txt` that will automatically perform all the image processing on your dataset. Or select another file to run the process you want. You can then run the process.

For each image, 5 CSV files will be created and saved in their respective folders:
- Calibration data
- Coordinates of the centroids
- Distance of the centroid to the interhemisphere
- Volume of the cells
- Intensity of the cells

## 4. Data Formatting

Once the image processing step is finished, go back to the Jupyter Notebook. If the notebook has been closed, run all the cells from the import section to just before the `initialisation()` function. Then, run the `extract()` function. Now you have a CSV to run your analysis on!

## Installation

- **Cellpose**: [https://cellpose.readthedocs.io/en/latest/installation.html](https://cellpose.readthedocs.io/en/latest/installation.html)
- **Fiji**: [https://imagej.net/software/fiji/](https://imagej.net/software/fiji/)
- **TAPAS**: [https://imagej.net/plugins/tapas](https://imagej.net/plugins/tapas)

## Set Up

- Your images need to be uploaded on OMERO.
- You have to change the paths in the `run_cellpose.bat` file.
- Each TAPAS file runs a specific process. You can run them one by one, or have them run automatically by using a subprocess file.

