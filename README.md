# Analysis_Lab_SiPMs
Repository with the notebooks used to analyze the data extracted from the SiPMs dimensions. Also some tips on how to plot IR02 control parameters.

Expected structure of the repository:
  * data: data extracted from the SiPMs (i.e .xlsx files)                  [included in the .gitignore you will only see your local files]
  * src: code to be executed:
    - notebooks: notebooks used to analyze the data
    - *.py macros to run the analysis from the terminal (individual.py runs on a selected folder and grouped.py runs on all HPK/FBK labeled folders)
    - folder_config*: yml file is use to load/classify easily the folders inside the macros (txt have additional information of unused folders)
  * lib: libraries with the used functions

When your data is analyzed you will get two new folders:
  * fit_data: grouped data from the SiPMs + statistics (i.e .txt files)    [included in the .gitignore you will only see your local files] 
  * images: all the variables plots 


RUN:

```
sh setup.sh
```
to install packages and create fit_data (data folder is assumed to exist, if not create it)

Option 1) Open the notebooks and run the cells. You can save the output in the fit_data folder and you will get histograms at the end of the notebook with the information.

Option 2) [from src folder] Run `python3 individual.py` to get the results on an individual set of data (errors and images will be generated on its own folder) and `python3 grouped.py` to get all HPK/FBK errors and plots of all the SiPMs classified as HPK/FBK.

If you are looking for some data to test the code you can find some in the:
- **/pnfs/ciemat.es/data/neutrinos/LAB/2023_03_08_DUNE-HD_SiPM_MECHANICAL_MEASUREMENTS/**: there are two folders HPK and FBK with the data produced by the mechanical measurements performed in the IR02. The files used with the Specifications for both SiPMs are also here. Additional information may be found in the neutrino drive `LAB/2023_03_08_DUNE-HD_SiPM_MECHANICAL_MEASUREMENTS` with summaries and presentations of the data.


## LICENSE
[MIT](https://choosealicense.com/licenses/mit/)

## Authors (alphabetical order, please insert your name here if you contribute to this project)

* [**Pérez-Molina, Laura**](https://github.com/LauPM)
