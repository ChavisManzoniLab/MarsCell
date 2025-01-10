# Methodology
📂 Project  
├── 📂 src  
│   ├── 📄 main.py  
│   ├── 📄 utils.py  
│   └── 📂 components
│       ├── 📄 component1.py
│       └── 📄 component2.py
├── 📂 tests
│   ├── 📄 test_main.py
│   └── 📄 test_utils.py
├── 📄 README.md
├── 📄 requirements.txt
└── 📂 data
    ├── 📂 raw
    │   ├── 📄 data1.csv
    │   └── 📄 data2.csv
    └── 📂 processed
        ├── 📄 clean_data1.csv
        └── 📄 clean_data2.csv
## Description (to change)
MarsCell is an AI-based workflow for automated cell detection and quantification on confocal images.
It is based on TAPAS, an ImageJ plugin, completed with Cellpose, an automatic cell-segmentation tool, and a Jupyter Notebook to ensure accessibility to everyone.

## 1. Set Up

### Downloads

First, make sure that the following softwares are installed:
- **Fiji**: [https://imagej.net/software/fiji/](https://imagej.net/software/fiji/)
- **TAPAS**: [https://imagej.net/plugins/tapas](https://imagej.net/plugins/tapas)
- **Python 3.9**: [https://www.python.org/downloads/release/python-3913/](https://www.python.org/downloads/release/python-3913/)

### 1.1 Create a virtual environment   

##### Using venv:

```bash
python -m venv MarsCell_env
```
Activate the virtual environment
```bash
MarsCell_env\Scripts\activate
```

##### Using conda:

```bash
conda create -n MarsCell_env python=3.9 anaconda
```
Activate the virtual environment
```bash
conda activate MarsCell_env
```

### 1.2 Install the packages:
```bash
pip install git+https://github.com/ChavisManzoniLab/MarsCell.git
```

If error :
```bash
ModuleNotFoundError: No module named 'distutils'
```
run 
```bash
pip install setuptools
pip install git+https://github.com/ChavisManzoniLab/MarsCell.git
```

## 2. Initialization

### 2.1 Launch MarsCell

To lauch MarsCell, type the command in your activated environment:
```bash
gui
```
You will be asked to chose a repository where a 'MarsCell' folder will be created. This folder will store the Cellpose models and the TAPAS files.
MarsCell is now ready to use!


### 2.2 Upload on OMERO

Upload your image stacks on OMERO, using OMERO.insight. Our image processing pipeline handles one dataset at a time, so ensure that all the images for a given project are included in the same dataset.

To obtain layer organization data (the distance of cells to a segment), you can draw a segment using the OMERO ROI interface. Please note that currently, the workflow only supports straight lines.




### 2.3 Create a MarsCell Project
Click on 'Create a project'

#### Image title structure
Specify the structure of the title of your images. Ensure that all your images follow the same naming convention to access information such as sex, age, condition. Indicate the separator used in your title to delimit the categories. Then, in the `structure` list, provide each category name in the order that they appear in the title.

Example:

```python
"""191001_B4_PPGI2_Naive_P35_M_C57_Rln_PFC1_FIG9_L.czi"""
separator = '_'
structure = ['Exp_Date', 'Batch', 'Ori', 'Condition', 'Age', 'Sex', 'Strain', 'Marker', 'Slide_Id', 'Atlas', 'Slide_side']
```

### 3. Image Processing with TAPAS and Cellpose

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

