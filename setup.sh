#!/bin/bash

if [ ! -d "../fit_data" ]; then
mkdir ../fit_data
fi

pip  install --upgrade pip
pip3 install xlrd==1.2.0
pip3 install plotly
pip3 install numpy
pip3 install matplotlib
pip3 install pandas
pip3 install kaleido