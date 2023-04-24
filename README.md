# Analysis_Lab_SiPMs
Repository with the notebooks used to analyse the data extracted from the SiPMs dimensions. Also some tips on how to plot IR02 control parameters.

Expected structure of the repository:
  * data: data extracted from the SiPMs (i.e .xlsx files)                  [included in the .gitignore you will only see your local files]
  * fit_data: grouped data from the SiPMs + statistics (i.e .txt files)    [included in the .gitignore you will only see your local files]
  * notebooks: notebooks used to analyse the data
  * lib: libraries with the used functions


RUN:

```
sh setup.sh
```
to install packages and create fit_data (data folder is assumed to exist, if not create it)

Open the notebooks and run the cells. You can save the output in the fit_data folder and you will get histograms at the end of the notebook with the information.
