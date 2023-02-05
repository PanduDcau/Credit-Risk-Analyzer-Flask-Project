JupyterNotebook: SMEsCashflowModelling

1. Background
The purpose of this script is to explore the idea of creating a credit scoring model to identify the financial ability and responsibility of small and medium sized businesses (i.e. SMEs) in the Caribbean Netherlands. If successfully developed, this could make it easier for SMEs in the Caribbean Netherlands (Bonaire, St. Eustatius and Saba) to obtain business financing at better interest rates. 


2. File Contents
Within this zip folder you will find the following files:
a. README.txt 
b. SMEsBankTransPrep.ipynb
c. SMEsCashflowModelling.ipynb
d. Requirements.txt
e. annon_bank_trans.csv (contained within "data" folder)
f. sum_bank_trans.csv (contained within "data" folder)
g. feature_select_framework.png (contained within folder named "images")


3. Getting Started
a. Installing Python and Libraries
In-order to get started you will need to have Python 3 in addition to several libraries installed on your local machine. I would recommend that you install Python 3 using the Anaconda or Miniconda distributions. For information on this, please visit; https://docs.anaconda.com/anaconda/install/index.html OR https://docs.conda.io/en/latest/miniconda.html. 

b. Creating an Environment
I would also recommend that you create a special environment specifically for running the Python code contained in the Jupyter Notebook files. After you have installed anaconda or miniconda on your machine, you can create an environment using the requirements.txt file and the bash command line command;

$ conda create --name <yourenvname> --file requirements.txt

For more information on creating, activating and managing environment with anaconda or miniconda, I refer you to their documentation at https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands

c. Running Jupyter Notebook
Once the environment you have created is activated, navigate to the directory on your machine using the command line where the files mentioned in 2. Contents are located. From here, simply type the following command to run Jupyter Notebooks from your default web browser;

$ jupyter notebook

This should automatically open Jupyter Notebook using the default web browser on your machine. You should then click on the file called SMEsCashflowModelling.ipynb and run each cell block from top to bottom. 


4. Your Feedback is Welcome!
Please feel free to share any constructive feedback or questions you may have regarding this project. You can contact me at k.daniel@tactbv.com.




