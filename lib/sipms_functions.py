import os, xlrd, csv
import numpy             as np
import matplotlib.pyplot as plt
import pandas            as pd

plt.rcParams.update({'font.size': 2})     # Global font size
plt.rc('font',           size=26)         # controls default text sizes
plt.rc('axes',           titlesize=28)    # fontsize of the axes title
plt.rc('axes',           labelsize=26)    # fontsize of the x and y labels
plt.rc('xtick',          labelsize=26)    # fontsize of the tick labels
plt.rc('ytick',          labelsize=26)    # fontsize of the tick labels
plt.rc('legend',         fontsize=23)     # legend fontsize
plt.rc('figure',         titlesize=20)    # fontsize of the figure title
plt.rc('axes.formatter', useoffset=False) # Scientific notation in axes ticks

###################################################################
############################## DATA ###############################
###################################################################

def df_display(values,labels, name,index="",terminal_output=False,save=False,save_path=None):
    '''
    Function to display the values in a dataframe.
    Args:
        - values: numpy array with the values
        - labels: list of the labels
        - name: name of the dataframe
        - index: list of the indexes
        - terminal_output: if True, it will print the dataframe
        - save: if True, it will save the dataframe in a .txt file
    Returns:
        - df: dataframe with the values
    '''
    
    if index == "":  index=np.arange(len(values))
    df = pd.DataFrame(values, columns=labels, index=index)
    if save: 
        if save_path == None: save_path = "../fit_data/"
        if not os.path.exists(save_path): os.makedirs(save_path)
        print('\033[92m'+"\n Saving file "+save_path+"df_"+name+".txt"+'\033[0m'); df.to_csv(save_path+'/df_'+name+'.txt', sep="\t")
    if terminal_output: 
        try: print("\n--------- %s ---------"%name); display(df)
        except NameError: print(df)
    return df 

def npy2df(df, per_label=[]):
    '''
    Function to convert a numpy array into a dataframe.
    Args:
        - df: numpy array with the values
        - per_label: list of the labels that have different values for each index
    Returns:
        - mean: numpy array with the mean of the values
        - stds: numpy array with the std of the values
    '''

    mean = []; stds = []; maxs = []; mins = []
    for label in df.columns:
        if label in per_label:
            print("Computing mean per index for label: ", label, "...")
            aux_mean = []; aux_stds = []; aux_maxs = []; aux_mins = []
            index = list(set(df.index)); index.sort()
            for idx in index:
                aux_mean.append(df[label].loc[idx].mean(axis=0))
                aux_stds.append(df[label].loc[idx].std(axis=0))
                aux_maxs.append(df[label].loc[idx].max(axis=0))
                aux_mins.append(df[label].loc[idx].min(axis=0))
            mean.append(aux_mean); stds.append(aux_stds); maxs.append(aux_maxs); mins.append(aux_mins)
        else:
            mean.append(df[label].mean(axis=0))
            stds.append(df[label].std(axis=0))
            maxs.append(df[label].max(axis=0))
            mins.append(df[label].min(axis=0))
    return mean, stds, maxs, mins

def data2npy(folder,pcbs_labels,sipm_labels,hlat_labels,pins_labels,sipm_number=6,pins_number=8,mode=1,
             distances={"pcb_header":3,"anv_header":2,"rev_header":2,"lat_header":4,
                        "row_pcbs":197,"row_sipm":197,"row_pina":197,"row_pinr":24,"row_hlat":24,
                        "col_pcbs":11, "col_sipm":14, "col_pina":17, "col_pinr":11,"col_hlat":10}, debug=False):
    '''
    Function to load the data from the .xlsx files into numpy arrays.
    Some configuration is hard-coded, so if you change the name of the files or the location of the data, you will need to change the function.
    Args:
        - folder: folder where the data is stored
        - pcbs_labels: list of the labels of the PCBs
        - sipm_labels: list of the labels of the SiPMs
        - hlat_labels: list of the labels of the lateral heights
        - pins_labels: list of the labels of the pins
        - sipm_number: number of SiPMs per PCB
        - pins_number: number of pins per PCB
        - mode: number of bunches of 6xSiPMs stored in each .xlsx file
        - distances: dictionary with the distances between the measurements:
            - pcb_header: distance between the header and the first measurement of the PCBs
            - anv_header: distance between the header and the first measurement of the SiPMs/pins in the front of the PCBs
            - rev_header: distance between the header and the first measurement of the pins in the back of the PCBs
            - lat_header: distance between the header and the first measurement of the lateral heights
            - row_pcbs: distance between the measurements of the PCBs
            - row_sipm: distance between the measurements of the SiPMs
            - row_pina: distance between the measurements of the pins in the front of the PCBs
            - row_pinr: distance between the measurements of the pins in the back of the PCBs
            - row_hlat: distance between the measurements of the lateral heights
            - col_pcbs: column where the measurements of the PCBs are stored
            - col_sipm: column where the measurements of the SiPMs are stored
            - col_pina: column where the measurements of the pins in the front of the PCBs are stored
            - col_pinr: column where the measurements of the pins in the back of the PCBs are stored
            - col_hlat: 1st column where the measurements of the lateral heights are stored
        - debug: if True, it will print the values of the cells in the .xlsx files
    Returns:
        5 arrays with columns for each variable and rows for each measurement:
        - pcbs_values: numpy array with the values of the PCBs
        - sipm_values: numpy array with the values of the SiPMs
        - pins_values_rev: numpy array with the values of the pins in the back of the PCBs
        - pins_values_anv: numpy array with the values of the pins in the front of the PCBs
        - hlat_values: numpy array with the values of the lateral heights
    '''

    print('\033[93m'+"\nWARNING: the configuration for the xlsx is hard-coded, any change in the naming or how information is distributed in the cells WILL NEED to be CHANGED in the function"+'\033[0m')
    
    names = os.listdir(folder)
    if 'fit_data' in names: names.remove('fit_data')
    if 'images'   in names: names.remove('images')
    
    pcbs_values     = np.empty([len(names)*mode,             len(pcbs_labels)+2], dtype=object) #solo anverso
    sipm_values     = np.empty([sipm_number*len(names)*mode, len(sipm_labels)+2], dtype=object) #solo anverso
    hlat_values     = np.empty([sipm_number*len(names)*mode, len(hlat_labels)+2], dtype=object) #solo altura pines ESPECIAL FBK
    pins_values_anv = np.empty([pins_number*len(names)*mode, len(pins_labels)+2], dtype=object) #solo anverso
    pins_values_rev = np.empty([pins_number*len(names)*mode, 3], dtype=object)                  #solo reverso/solo altura pines
    
    names_sipms = []
    for i in range(sipm_number): names_sipms.append("SiPM #%i"%(i+1))
    if debug: print(names_sipms)

    names_pins = []
    for i in range(pins_number): names_pins.append("Pin #%i"%(i+1))
    if debug: print(names_pins)

    if mode == 1: print("\n[INFO] You have entered \"mode=1\", meaning that each bunch of 6xSiPMs is stored in ONE .xlsx")
    else:         print("\n[INFO] You have entered \"mode=%i\", meaning that in each .xlsx you stored %i bunches of 6xSiPMs"%(mode,mode))

    pcbs_ids = []; sipm_ids = []; pins_anv_ids = []; pins_rev_ids = []; hlat_ids = []
    pcbs_dat = []; sipm_dat = []; pins_anv_dat = []; pins_rev_dat = []; hlat_dat = []
    for n in np.arange(len(names)): # Distintos archivos --> Placas PCBs
        if debug: print("\n----- LOCATION:", folder + names[n] + '/' + names[n], "-----")
        # Open the workbook and define the worksheet:
        workbooks_anv  = xlrd.open_workbook(folder + names[n] + '/' + names[n] + '_anverso.xlsx')
        workbooks_rev  = xlrd.open_workbook(folder + names[n] + '/' + names[n] + '_reverso.xlsx')
        worksheet_anv = workbooks_anv.sheet_by_index(0)
        worksheet_rev = workbooks_rev.sheet_by_index(0)
        try: 
            workbooks_lat = xlrd.open_workbook(folder + names[n] + '/' + names[n] + '_alturas.xlsx')
            worksheet_lat = workbooks_lat.sheet_by_index(0)
        except: print("No se ha encontrado el archivo de alturas para la placa %s"%names[n])

        # Serial number to identify each SiPM #
        serial_number = [];
        for m in range(mode): serial_number.append([int(worksheet_anv.cell(2+m,20).value)])
        serial_number = list(np.concatenate(serial_number).flat)

        # PCB #
        if debug: print('\033[96m'+"\nPCB"+'\033[0m')
        for l in np.arange(len(pcbs_labels)):    # Etiquetas x16
            for m in range(mode):                # Entries in each file
                row = distances["pcb_header"]+l+m*distances["row_pcbs"] # 3+l(ETIQUETA(0-16))+m*197(SEPARACION ENTRE MEDIDAS)
                col = distances["col_pcbs"] # default column 11
                val = float(worksheet_anv.cell(row,col).value) #cell allocation in xlsx file
                if debug: print("(row,col): (%i,%i) ;  value: %.2f"%(row,col,val))
                pcbs_values[n*mode+m,l] = val 
        pcbs_ids.append([str(names[n])+"_ID"+str(sn) for sn in serial_number])
        pcbs_dat.append([str(folder.split("/")[-2]) for sn in serial_number])

        # SiPMs #
        if debug: print('\033[96m'+"\nSiPMs"+'\033[0m')
        for l in np.arange(len(sipm_labels)):    # Etiquetas x6
            for m in range(mode):                # Entries in each file
                for j in np.arange(sipm_number): # SiPMs x6
                    row = distances["pcb_header"]+l+j*(distances["anv_header"]+len(sipm_labels))+m*distances["row_sipm"] # 3+l(ETIQUETA(0-6))+j*8(DISTANCIA ENTRE SIPMS)+m*197(SEPARACION ENTRE MEDIDAS)
                    col = distances["col_sipm"]  # default column 14
                    val = float(worksheet_anv.cell(row,col).value) #cell allocation in xlsx file
                    if debug: print("(row,col): (%i,%i) ;  value: %.2f"%(row,col,val))
                    sipm_values[j+m*sipm_number+n*(sipm_number*(mode-1)+sipm_number),l] = val
        sipm_ids.append([str(names[n])+"_ID"+str(sn) for sn in [i for i in serial_number for j in range(sipm_number)]])
        sipm_dat.append([str(folder.split("/")[-2]) for sn in [i for i in serial_number for j in range(sipm_number)]])

        # Alturas laterales #
        if "workbooks_lat" in locals() and hlat_labels != []: # Si hay alturas laterales
            print('\033[96m'+"\nLateral heights found! Storing them to plot"+'\033[0m')
            for l in np.arange(len(hlat_labels)):    # Etiquetas x4
                r = n*(sipm_number*mode)             # Counter for flatten rows
                for m in range(mode):                # Entries in each file
                    for j in np.arange(sipm_number): # SiPMs x6
                        row = distances["lat_header"]+m*distances["row_hlat"]+j
                        col = distances["col_hlat"] + l
                        val = float(worksheet_lat.cell(row,col).value) #cell allocation in xlsx file
                        if debug: print("(row,col): (%i,%i) ;  value: %.2f"%(row,col,val))
                        hlat_values[r,l] = val
                        r += 1
            hlat_ids.append([str(names[n])+"_ID"+str(sn) for sn in [i for i in serial_number for j in range(sipm_number)]])
            hlat_dat.append([str(folder.split("/")[-2]) for sn in [i for i in serial_number for j in range(sipm_number)]])

        if "workbooks_lat" in locals() and hlat_labels == []: print('\033[91m'+"ERROR: You have entered a file with lateral heights but you have not specified the labels"+'\033[0m')
        
        # Pins anverso #
        if debug: print('\033[96m'+"\nPins anverso"+'\033[0m')
        for l in np.arange(len(pins_labels)):    # Etiquetas x3
            for m in range(mode):                # Entries in each file
                for j in np.arange(pins_number): # Pins x8
                    row = distances["pcb_header"]+l+j*(distances["anv_header"]+len(pins_labels))+m*distances["row_pina"] # 3+l(ETIQUETA(0-3))+j*5(DISTANCIA ENTRE PINS)+m*197(SEPARACION ENTRE MEDIDAS)
                    col = distances["col_pina"]  # default column 17
                    val = float(worksheet_anv.cell(row,col).value) #cell allocation in xlsx file
                    if debug: print("(row,col): (%i,%i) ;  value: %.2f"%(row,col,val))
                    pins_values_anv[j+m*pins_number+n*(pins_number*(mode-1)+pins_number),l] = val
        pins_anv_ids.append([str(names[n])+"_ID"+str(sn) for sn in [i for i in serial_number for j in range(pins_number)]])
        pins_anv_dat.append([str(folder.split("/")[-2]) for sn in [i for i in serial_number for j in range(pins_number)]])

        # Pins reverso #
        if debug: print('\033[96m'+"\nPins reverso"+'\033[0m')
        for m in range(mode):                    # Entries in each file
            for j in np.arange(pins_number):     # Pins x8
                row = distances["pcb_header"]+j+m*distances["row_pinr"] # 3+l(ETIQUETA(0-3))+j*5(DISTANCIA ENTRE PINS)+m*197(SEPARACION ENTRE MEDIDAS)
                col = distances["col_pinr"] # default column 11
                val = float(worksheet_rev.cell(row,col).value) #cell allocation in xlsx file # Etiqueta x1 (sin loop) REVERSO
                if debug: print("(row,col): (%i,%i) ;  value: %.2f"%(row,col,val))
                pins_values_rev[j+m*pins_number+n*(pins_number*(mode-1)+pins_number),0] = val
        pins_rev_ids.append([str(names[n])+"_ID"+str(sn) for sn in [i for i in serial_number for j in range(pins_number)]])
        pins_rev_dat.append([str(folder.split("/")[-2]) for sn in [i for i in serial_number for j in range(pins_number)]])

    pcbs_values[:,-2]     = list(np.concatenate(pcbs_ids).flat)
    pcbs_values[:,-1]     = list(np.concatenate(pcbs_dat).flat)
    sipm_values[:,-2]     = list(np.concatenate(sipm_ids).flat)
    sipm_values[:,-1]     = list(np.concatenate(sipm_dat).flat)
    pins_values_anv[:,-2] = list(np.concatenate(pins_anv_ids).flat)
    pins_values_anv[:,-1] = list(np.concatenate(pins_anv_dat).flat)
    pins_values_rev[:,-2] = list(np.concatenate(pins_rev_ids).flat)
    pins_values_rev[:,-1] = list(np.concatenate(pins_rev_dat).flat)
    if hlat_labels != []: hlat_values[:,-2] = list(np.concatenate(hlat_ids).flat)
    if hlat_labels != []: hlat_values[:,-1] = list(np.concatenate(hlat_dat).flat)

    print('\033[96m'+"\nCHECK DIMENSIONS:"+'\033[0m')
    print("Files x Bunches:",len(pcbs_values))
    print("PCBs:",len(pcbs_values))
    print("SiPM:",len(sipm_values))
    if hlat_labels != []: print("HLAT:",len(hlat_values))
    print("PIN_ANV:",len(pins_values_anv))
    print("PIN_REV:",len(pins_values_rev))
   
    return pcbs_values, sipm_values, pins_values_rev, pins_values_anv, hlat_values

def sanity_check(df_values,values):
    '''
    Sanity check to see if there are repeated rows in the dataframe.
    If there are, it will print the indexes of the repeated rows and the difference between them.
    (Useful to check if your configuration to load the data is correct)
    '''
    if df_values.duplicated().any(): 
        print("You have repeated rows")
        aux = []; resta = []
        for i, element in enumerate(np.where(df_values.duplicated())[0]):
            for j,y in enumerate(values):
                where_array = np.where(values[element] == y)[0]
                try: 
                    if len(where_array) == len(values[element]): 
                            if j != element: aux.append((element,j)) 
                except TypeError: 
                    if j != element: aux.append((element,j))

        for a in aux: resta.append(abs(a[0]-a[1]))
        resta.sort()
        plt.scatter(np.arange(len(resta)),resta)
        plt.show()
    else: print('\033[92m'+"Great! All your entries are unique :)"+'\033[0m')

def check_especifications(df_ids, df_mean, labels, filename=""):
    '''
    Check if the values of the dataframe are within the specifications.
    If they are not, it will print the indexes of the rows that are not within the specifications.
    Args:
        - df_ids: dataframe with the values to check
        - df_mean: dataframe with the mean and std of the specifications
        - labels: list of the labels to check
        - filename: if you want to save the output in a file, give a name to the file
    Returns:
        - prints the indexes of the rows that are not within the specifications
    '''
    if filename != "": f = open(filename+'.txt', 'w')
    for column in labels:
        if (df_mean[column].loc["Theoretical"]) != None  and type(df_mean[column].loc["Theoretical"]) != str and type(df_mean[column].loc["Theoretical"]) != list:
            limit1   = df_mean[column].loc["Theoretical"] - df_mean[column].loc["STD-"]
            limit2   = df_mean[column].loc["Theoretical"] + df_mean[column].loc["STD+"]
            df_weird = df_ids[[column,"IDs"]][(df_ids[column] < limit1) | (df_ids[column] > limit2)]
            print("\nLimits in column %s: (%0.2f-%0.2f) "%(column,limit1,limit2))
            if filename != "": print("\nLimits in column %s: (%0.2f-%0.2f) "%(column,limit1,limit2), file = f)
            if (len(df_weird) > 0):
                print('\033[91m'+"ERROR (x%i) "%(len(df_weird))+'\033[0m')
                print('\033[91m'+"ERROR (x%i) "%(len(df_weird))+'\033[0m', file = f)
                print(df_weird)
                print(df_weird, file = f)
        if (df_mean[column].loc["Theoretical"]) != None and type(df_mean[column].loc["Theoretical"]) == list or type(df_mean[column].loc["Theoretical"]) == str:
            print("Especifications differ for each index in column %s: "%(column))
            #transform this list of string into a list of floats removing the brackets and using the commas as separators
            df_mean[column].loc["Theoretical"] = [float(x) for x in df_mean[column].loc["Theoretical"].replace("[","").replace("]","").split(",")]
            df_mean[column].loc["STD-"] = [float(x) for x in df_mean[column].loc["STD-"].replace("[","").replace("]","").split(",")]
            df_mean[column].loc["STD+"] = [float(x) for x in df_mean[column].loc["STD+"].replace("[","").replace("]","").split(",")]

            if filename != "": print("Especifications differ for each index in column %s: "%(column), file = f)
            index = list(set(df_ids.index)); index.sort()
            for i, idx in enumerate(index):
                limit1   = float(df_mean[column].loc["Theoretical"][i]) - float(df_mean[column].loc["STD-"][i])
                limit2   = float(df_mean[column].loc["Theoretical"][i]) + float(df_mean[column].loc["STD+"][i])
                df_weird = df_ids.loc[idx][[column,"IDs"]][(df_ids.loc[idx][column] < limit1) | (df_ids.loc[idx][column] > limit2)]

                print("\nLimits in column %s for index %s: (%0.2f-%0.2f) "%(column,idx,limit1,limit2))
                if filename != "": print("\nLimits in column %s for index %s: (%0.2f-%0.2f) "%(column,idx,limit1,limit2), file = f)
                if (len(df_weird) > 0):
                    print('\033[91m'+"ERROR (x%i) "%(len(df_weird))+'\033[0m')
                    if filename != "": print('\033[91m'+"ERROR (x%i) "%(len(df_weird))+'\033[0m', file = f)
                    print(df_weird)
                    if filename != "": print(df_weird, file = f)
    print("------------------------------------------------------------------------------------")       


###################################################################
########################### VISUALIZATION #########################
###################################################################

def plotitos(title, xlabel, ylabel, df, df_mean, columns, colors, bars =[], decimales=2):
    '''
    Histogram given two df one with the values to plot an the other with the Mean and STD to be shown with vertical lines.
    You can give as input variables the title, x/ylabels, the color and the decimals to round the mean/std.
    '''
    left, width = .25, .23
    bottom, height = .25, .6
    right = left + width
    top = bottom + height
    decimales = decimales
    # if bars == []:
    
    if bars == []: 
        fig, ax = plt.subplots(1,1, figsize = (12,10), sharey=True)
        fig.tight_layout()
        
        ax.hist(df[columns], color = colors[0]) #, density=True
        media_std_1 = str(np.round(df_mean[columns]['Mean'],decimales))+ r"$\pm$" +str(np.round(df_mean[columns]['STD'],decimales))
        ax.axvline(np.round(df_mean[columns]['Mean'],decimales), color=colors[1])
        ax.axvline(np.round(df_mean[columns]['Mean'],decimales)-np.round(df_mean[columns]['STD'],decimales), color=colors[2], linestyle='dashed')
        ax.axvline(np.round(df_mean[columns]['Mean'],decimales)+np.round(df_mean[columns]['STD'],decimales), color=colors[2], linestyle='dashed')
        ax.text(right, top, 'Mean = ' + media_std_1, horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes)

    else: 
        fig, ax = plt.subplots(2,int(len(bars)/2), figsize = (40,15), sharey=True)
        fig.tight_layout(pad=2.5)

        x = [0] * int(len(bars)/2) + [1] * int(len(bars)/2)
        y = list(np.arange(int(len(bars)/2))) * 2
        for i, b in enumerate(bars):
            mean, std = npy2df(df.loc[b])
            df_mean = df_display(np.array((mean,std)),labels = list(df.columns),index=["Mean","STD"],name="")
            media_std_1 = str(np.round(df_mean[columns]['Mean'],decimales))+ r"$\pm$" +str(np.round(df_mean[columns]['STD'],decimales))
            ax[x[i],y[i]].set_title(b)
            ax[x[i],y[i]].hist(df.loc[b][columns])
            if colors[1] != None: ax[x[i],y[i]].axvline(np.round(df_mean[columns]['Mean'],decimales), color=colors[1])
            if colors[2] != None: ax[x[i],y[i]].axvline(np.round(df_mean[columns]['Mean'],decimales)-np.round(df_mean[columns]['STD'],decimales), color=colors[2], linestyle='dashed')
            if colors[2] != None: ax[x[i],y[i]].axvline(np.round(df_mean[columns]['Mean'],decimales)+np.round(df_mean[columns]['STD'],decimales), color=colors[2], linestyle='dashed')
            ax[x[i],y[i]].text(right, top, 'Mean = ' + media_std_1, horizontalalignment='right', verticalalignment='bottom', transform=ax[x[i],y[i]].transAxes)
    
    fig.suptitle(title)
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)

    plt.show()

import plotly.express       as px
import plotly.offline       as pyoff
import plotly.graph_objects as go

def plotlytos(title, xlabel, ylabel, df, df_mean, column, colors, decimales=2, text_auto=True,save=False,save_path=None):

    if type(df_mean[column]["Theoretical"]) != list or type(df_mean[column]["Theoretical"]) == str:
        th  = df_mean[column]["Theoretical"];  stdp = df_mean[column]["STD+"]; stdm = df_mean[column]["STD-"]
        exp = df_mean[column]["Experimental"]; maxs = df_mean[column]["Max"];  mins = df_mean[column]["Min"]

        # Compute the histogram
        hist_values, bin_edges = np.histogram(df[column], bins=10)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        max_height = np.max(hist_values)
        vline = 1.5*max_height

        # Create the histogram using go.Bar
        fig = go.Figure(data=[go.Bar(x=bin_centers, y=hist_values,name="Data",showlegend=False)])
        fig.update_layout(barmode="overlay",template="presentation", width=900, height=600,bargap=0)

        if text_auto: fig.update_traces(hovertemplate = str(column) + ': %{x}' + '<br>' + "IDs: "+ df["IDs"] + '<extra></extra>')
        fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Min: %s mm"%str(np.round(mins,decimales))))
        fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Max: %s mm"%str(np.round(maxs,decimales))))
        fig.add_trace(go.Scatter(x=[exp]*2,     y = [0,vline], mode="lines", line=dict(color=colors[2],width=4), name="EXP:  %s mm"%str(np.round(exp,decimales))))
        fig.add_trace(go.Scatter(x=[th+stdp]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1],width=4), name="TOL+: %s mm"%str(np.round(stdp,decimales))))
        if "weld" not in title: fig.add_trace(go.Scatter(x=[th]*2,      y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[0],width=4), name="TH:   %s mm"%str(np.round(th,decimales))))
        if "weld" not in title: fig.add_trace(go.Scatter(x=[th-stdm]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1],width=4), name="TOL-: %s mm"%str(np.round(stdm,decimales))))
        custom_plotly_layout(fig, xaxis_title=xlabel, yaxis_title=ylabel, title=title)

        low=min(df[column])/np.mean(df[column])
        hig=max(df[column])/np.mean(df[column])

        xmin = abs(low)*min(df[column])
        xmax = abs(hig)*max(df[column])
        if abs(xmin) > abs(th-stdp): xmin = abs(low)*(th-stdp)
        if abs(xmax) < abs(th+stdp): xmax = abs(hig)*(th+stdp)
        fig.update_layout(xaxis_range=[xmin, xmax])
        fig.update_layout(yaxis_range=[0, vline])
        if save: 
            if save_path == None: save_path = "../images/"
            if not os.path.exists(save_path): os.makedirs(save_path)
            print('\033[92m'+"\n Saving file "+save_path+title+".png"+'\033[0m'); 
            fig.write_image(save_path+str(title)+".png")
            # pyoff.plot(fig, filename=save_path+"/df_"+title+".html", auto_open=False)
    
    else:
        print("Especifications differ for each index in column %s: "%(column))
        df2plot = df_mean.explode([column])
        index = list(set(df.index)); index.sort()
        for col in range(len((df_mean[column]["Theoretical"]))):
            th  = df2plot[column]["Theoretical"][col];  stdp = df2plot[column]["STD+"][col]; stdm = df2plot[column]["STD-"][col]
            exp = df2plot[column]["Experimental"][col]; maxs = df2plot[column]["Max"][col];  mins = df2plot[column]["Min"][col]

            # Compute the histogram
            hist_values, bin_edges = np.histogram(df.loc[index[col]][column])
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            max_height = np.max(hist_values)
            vline = 1.5*max_height

            # Create the histogram using go.Bar
            fig = go.Figure(data=[go.Bar(x=bin_centers, y=hist_values,name="Data",showlegend=False)]) #hover_data=[column, "IDs"], text_auto=text_auto
            fig.update_layout(barmode="overlay",template="presentation", width=900, height=600,bargap=0)

            if text_auto: fig.update_traces(hovertemplate = str(column) + ': %{x}' + '<br>' + "IDs: "+ df.loc[index[col]]["IDs"] + '<extra></extra>')
            fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Max: %s mm"%str(np.round(maxs,decimales))))
            fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Min: %s mm"%str(np.round(mins,decimales))))
            fig.add_trace(go.Scatter(x=[exp]*2,     y = [0,vline], mode="lines", line=dict(color=colors[2],width=4), name="EXP:  %s mm"%str(np.round(exp,decimales))))
            fig.add_trace(go.Scatter(x=[th+stdp]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1],width=4), name="TOL+: %s mm"%str(np.round(stdp,decimales))))
            fig.add_trace(go.Scatter(x=[th]*2,      y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[0],width=4), name="TH:   %s mm"%str(np.round(th,decimales))))
            fig.add_trace(go.Scatter(x=[th-stdm]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1],width=4), name="TOL-: %s mm"%str(np.round(stdm,decimales))))
            custom_plotly_layout(fig, xaxis_title=xlabel, yaxis_title=ylabel, title=str(index[col])+ " - " +title + " (L%i)"%(col+1))
            
            low=min(df.loc[index[col]][column])/np.mean(df.loc[index[col]][column])
            hig=max(df.loc[index[col]][column])/np.mean(df.loc[index[col]][column])

            xmin = abs(low)*min(df.loc[index[col]][column])
            xmax = abs(hig)*max(df.loc[index[col]][column])
            if abs(xmin) > abs(th-stdp): xmin = abs(low)*(th-stdp)
            if abs(xmax) < abs(th+stdp): xmax = abs(hig)*(th+stdp)
            fig.update_layout(xaxis_range=[xmin, xmax])
            fig.update_layout(yaxis_range=[0, vline])

            if save: 
                if save_path == None: save_path = "../images/"
                if not os.path.exists(save_path): os.makedirs(save_path)
                print('\033[92m'+"\n Saving file "+save_path+str(index[col])+ " - " +title + " (L%i)"%(col+1)+".png"+'\033[0m'); 
                fig.write_image(save_path+str(index[col])+ " - " +title + " (L%i)"%(col+1)+".png")

    return fig

def custom_legend_name(fig_px,new_names):
    for i, new_name in enumerate(new_names):
        fig_px.data[i].name = new_name
    return fig_px

def custom_plotly_layout(fig_px, xaxis_title="", yaxis_title="", title="",barmode="stack"):
    fig_px.update_layout( template="presentation", title=title, xaxis_title=xaxis_title, yaxis_title=yaxis_title, barmode=barmode,
                   font=dict(family="serif"), legend_title_text='', legend = dict(yanchor="top", xanchor="right", x = 0.99), showlegend=True)
    fig_px.update_xaxes(showline=True,mirror=True,zeroline=False)
    fig_px.update_yaxes(showline=True,mirror=True,zeroline=False)
    return fig_px

def show_html(fig_px):
    return pyoff.plot(fig_px, include_mathjax='cdn')

def save_html(fig_px,name):
    return fig_px.write_html(name, include_mathjax = 'cdn')