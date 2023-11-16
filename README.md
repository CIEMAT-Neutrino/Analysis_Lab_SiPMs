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

If you are looking to some data to test the code you can find some in:
- **/pnfs/ciemat.es/data/neutrinos/FD1_SiPMsTests_IR02/** there are two folder HPK and FBK with the data produced by the mechanical measurements performed in the IR02. Additional information may be found in the neutrino drive ANALISIS LAB/FD1_SiPMsTests (IR02) with summaries and presentations of the data.


## LICENSE
[MIT](https://choosealicense.com/licenses/mit/)

## Authors (alphabetical order, please insert your name here if you contribute to this project)

* [**Pérez-Molina, Laura**](https://github.com/rodralva)
