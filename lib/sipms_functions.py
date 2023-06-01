import os
import numpy             as np
import matplotlib.pyplot as plt
import pandas            as pd
import xlrd, csv

plt.rcParams.update({'font.size': 2})
plt.rc('font',   size=26)        # controls default text sizes
plt.rc('axes',   titlesize=28)   # fontsize of the axes title
plt.rc('axes',   labelsize=26)   # fontsize of the x and y labels
plt.rc('xtick',  labelsize=26)   # fontsize of the tick labels
plt.rc('ytick',  labelsize=26)   # fontsize of the tick labels
plt.rc('legend', fontsize=23)    # legend fontsize
plt.rc('figure', titlesize=20)   # fontsize of the figure title
plt.rc('axes.formatter', useoffset=False)

###################################################################
############################## DATA ###############################
###################################################################

def df_display(values,labels, name,index="",terminal_output=False,save=False):
    if index == "":  index=np.arange(len(values))
    df = pd.DataFrame(values, columns=labels, index=index)
    if save: print("\n Saving file ../fit_data/df_"+name+".txt"); df.to_csv('../fit_data/df_'+name+'.txt', sep=" ", quoting=csv.QUOTE_NONE, escapechar=" ")
    if terminal_output: print("\n--------- %s ---------"%name); display(df)
    return df 

def npy2df(df, per_label=[]):
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

def data2npy(folder, pcbs_labels, sipm_labels, pins_labels, sipm_number=6, pins_number=8, mode=1, debug=False):
    print("\nWARNING: the configuration for the xlsx is hard-coded, any change in the naming or how information is distributed in the cells WILL NEED to be CHANGED in the function")
    
    names           = os.listdir(folder)
    pcbs_values     = np.empty([len(names)*mode,              len(pcbs_labels)+1], dtype=object) #solo anverso
    sipm_values     = np.empty([sipm_number*len(names)*mode,  len(sipm_labels)+1], dtype=object) #solo anverso
    pins_values_anv = np.empty([pins_number*len(names) *mode, len(pins_labels)+1], dtype=object) #solo anverso
    pins_values_rev = np.empty([pins_number*len(names) *mode, 2], dtype=object)                #solo reverso/solo altura pines
    
    names_sipms = []
    for i in range(sipm_number): names_sipms.append("SiPM #%i"%(i+1))
    if debug: print(names_sipms)

    names_pins = []
    for i in range(pins_number): names_pins.append("Pin #%i"%(i+1))
    if debug: print(names_pins)

    if mode == 1: print("\nYou have entered \"mode=1\", meaning that each bunch of 6xSiPMs is stored in ONE .xlsx")
    else:         print("\nYou have entered \"mode=%i\", meaning that in each .xlsx you stored %i bunches of 6xSiPMs"%(mode,mode))

    pcbs_ids = []; sipm_ids = []; pins_anv_ids = []; pins_rev_ids = []
    for n in np.arange(len(names)): # Distintos archivos --> Placas PCBs
        ##PREVIOUS CONFIGURATION##
        # workbook_anv  = xlrd.open_workbook(folder + names[n] + '/' + names[n].replace("Nº","") + '_anverso_1.xlsx')
        # workbook_rev  = xlrd.open_workbook(folder + names[n] + '/' + names[n].replace("Nº","") + '_reverso_1.xlsx')
        workbooks_anv  = xlrd.open_workbook(folder + names[n] + '/' + names[n] + '_anverso.xlsx')
        workbooks_rev  = xlrd.open_workbook(folder + names[n] + '/' + names[n] + '_reverso.xlsx')
        worksheet_anv = workbooks_anv.sheet_by_index(0)
        worksheet_rev = workbooks_rev.sheet_by_index(0)

        if debug: print("\n----- LOCATION:", folder + names[n] + '/' + names[n], "-----")


        serial_number = [];
        for m in range(mode): serial_number.append([int(worksheet_anv.cell(2+m,20).value)])
        serial_number = list(np.concatenate(serial_number).flat)


        # PCB #
        if debug: print("\nPCB")
        for l in np.arange(len(pcbs_labels)):    # Etiquetas x16
            for m in range(mode):                # Entries in each file
                pcbs_values[n*mode+m,l] = worksheet_anv.cell(3+l+m*197,11).value #cell allocation in xlsx file
                if debug: print("row: ", 3+l+m*197, "; value: ", worksheet_anv.cell(3+l+m*197,11).value)
               #pcbs_values[0-(names*mode*#LABELS),0-16] = cell(COLUMNA: 3+l(ETIQUETA(0-16))+m*197(SEPARACION ENTRE MEDIDAS), FILA: 11)
        pcbs_ids.append([str(names[n])+"_ID"+str(sn) for sn in serial_number])

        # SiPMs #
        if debug: print("\nSiPMs")
        for l in np.arange(len(sipm_labels)):    # Etiquetas x6
            for m in range(mode): 
                for j in np.arange(sipm_number): # SiPMs x6
                    sipm_values[j+m*sipm_number+n*(sipm_number*(mode-1)+sipm_number),l] = worksheet_anv.cell(3+l+j*8+m*197,14).value #cell allocation in xlsx file
                    if debug: print("row: ", 3+l+j*8+m*197, "; value: ", worksheet_anv.cell(3+l+j*8+m*197,14).value)
                   #sipm_values[0-(names*mode*#SIPMS*#LABELS),0-6] = cell(COLUMNA: 3+l(ETIQUETA(0-6))+j*8(DISTANCIA ENTRE SIPMS)+m*197(SEPARACION ENTRE MEDIDAS), FILA: 14)
        sipm_ids.append([str(names[n])+"_ID"+str(sn) for sn in [i for i in serial_number for j in range(sipm_number)]])

        # Pins anverso #
        if debug: print("\nPins anverso")
        for l in np.arange(len(pins_labels)):    # Etiquetas x3
            for m in range(mode):                # Entries in each file
                for j in np.arange(pins_number): # Pins x8
                    pins_values_anv[j+m*pins_number+n*(pins_number*(mode-1)+pins_number),l] = worksheet_anv.cell(3+l+j*5+m*197,17).value #cell allocation in xlsx file
                    if debug: print("row: ", 3+l+j*5+m*197, "; value: ", worksheet_anv.cell(3+l+j*5+m*197,17).value)
                   #pins_values_anv[0-(names*mode**#PINS*#LABELS),0-8] = cell(COLUMNA: 3+l(ETIQUETA(0-3))+j*5(DISTANCIA ENTRE PINS)+m*197(SEPARACION ENTRE MEDIDAS), FILA: 17)
        pins_anv_ids.append([str(names[n])+"_ID"+str(sn) for sn in [i for i in serial_number for j in range(pins_number)]])


        # Pins reverso #
        if debug: print("\nPins reverso")
        for m in range(mode):                    # Entries in each file
            for j in np.arange(pins_number):     # Pins x8
                pins_values_rev[j+m*pins_number+n*(pins_number*(mode-1)+pins_number),0] = worksheet_rev.cell(3+j+m*24,11).value # Etiqueta x1 (sin loop) REVERSO
                if debug: print("row: ", 3+j+m*24, "; value: ", worksheet_rev.cell(3+j+m*24,11).value)
               #pins_values_rev[0-(names*mode*#PINS)] = cell(COLUMNA: 3+l(ETIQUETA(0-6))+j(0-8 pins)+m*24(SEPARACION ENTRE MEDIDAS), FILA: 11)
        pins_rev_ids.append([str(names[n])+"_ID"+str(sn) for sn in [i for i in serial_number for j in range(pins_number)]])

    pcbs_values[:,-1] = list(np.concatenate(pcbs_ids).flat)
    sipm_values[:,-1] = list(np.concatenate(sipm_ids).flat)
    pins_values_anv[:,-1] = list(np.concatenate(pins_anv_ids).flat)
    pins_values_rev[:,-1] = list(np.concatenate(pins_rev_ids).flat)

    print("\nCHECK DIMENSIONS:")
    print("Files x Bunches:",len(pcbs_values))
    print("PCBs:",len(pcbs_values))
    print("SiPM:",len(sipm_values))
    print("PIN_ANV:",len(pins_values_anv))
    print("PIN_REV:",len(pins_values_rev))

    return pcbs_values, sipm_values, pins_values_rev, pins_values_anv

def sanity_check(df_values,values):
    if df_values.duplicated().any(): 
        print("You have repeated rows")
        aux = []
        for i, element in enumerate(np.where(df_values.duplicated())[0]):
                for j,y in enumerate(values):
                        where_array = np.where(values[element] == y)[0]
                        try: 
                                if len(where_array) == len(values[element]): 
                                        if j != element: aux.append((element,j)) 
                        except TypeError: 
                               if j != element: aux.append((element,j))
        resta = []
        for a in aux:
                resta.append(abs(a[0]-a[1]))
        resta.sort()
        # print(resta)
        plt.scatter(np.arange(len(resta)),resta)
        plt.show()

    else: print("Great! All your entries are unique :)")

def check_especifications(df_ids, df_mean, labels):
    for column in labels:
        if (df_mean[column].loc["Theoretical"]) != None and type(df_mean[column].loc["Theoretical"]) != list:
            limit1 = df_mean[column].loc["Theoretical"] - df_mean[column].loc["STD-"]
            limit2 = df_mean[column].loc["Theoretical"] + df_mean[column].loc["STD+"]
            df_weird = df_ids[[column,"IDs"]][(df_ids[column] < limit1) | (df_ids[column] > limit2)]
            print("\nLimits in column %s: (%0.2f-%0.2f) "%(column,limit1,limit2))
            if (len(df_weird) > 0):
                print("ERROR (x%i) "%(len(df_weird)))
                print(df_weird)
        if (df_mean[column].loc["Theoretical"]) != None and type(df_mean[column].loc["Theoretical"]) == list:
            print("Especifications differ for each index in column %s: "%(column))
            index = list(set(df_ids.index)); index.sort()
            for i, idx in enumerate(index):
                limit1 = df_mean[column].loc["Theoretical"][i] - df_mean[column].loc["STD-"][i]
                limit2 = df_mean[column].loc["Theoretical"][i] + df_mean[column].loc["STD+"][i]
                df_weird = df_ids.loc[idx][[column,"IDs"]][(df_ids.loc[idx][column] < limit1) | (df_ids.loc[idx][column] > limit2)]

                print("\nLimits in column %s for index %s: (%0.2f-%0.2f) "%(column,idx,limit1,limit2))
                if (len(df_weird) > 0):
                    print("ERROR (x%i) "%(len(df_weird)))
                    print(df_weird)
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

def plotlytos(title, xlabel, ylabel, df, df_mean, column, colors, decimales=2, vline=100):

    if type(df_mean[column]["Theoretical"]) != list:
        th  = df_mean[column]["Theoretical"];  stdp = df_mean[column]["STD+"]; stdm = df_mean[column]["STD-"]
        exp = df_mean[column]["Experimental"]; maxs = df_mean[column]["Max"];  mins = df_mean[column]["Min"]

        fig = px.histogram(df, template="presentation", x=column,width=900, height=600)
        fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Min: %s mm"%str(np.round(mins,decimales))))
        fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Max: %s mm"%str(np.round(maxs,decimales))))
        fig.add_trace(go.Scatter(x=[exp]*2,     y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[2]), name="EXP:  %s mm"%str(np.round(exp,decimales))))
        fig.add_trace(go.Scatter(x=[th+stdp]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1]), name="STD+: %s mm"%str(np.round(stdp,decimales))))
        fig.add_trace(go.Scatter(x=[th]*2,      y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[0]), name="TH:   %s mm"%str(np.round(th,decimales))))
        fig.add_trace(go.Scatter(x=[th-stdm]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1]), name="STD-: %s mm"%str(np.round(stdm,decimales))))
        custom_plotly_layout(fig, xaxis_title=xlabel, yaxis_title=ylabel, title=title)

    else:
        df2plot = df_mean.explode(column)
        index = list(set(df.index)); index.sort()
        for col in range(len((df_mean[column]["Theoretical"]))):
            th  = df2plot[column]["Theoretical"][col];  stdp = df2plot[column]["STD+"][col]; stdm = df2plot[column]["STD-"][col]
            exp = df2plot[column]["Experimental"][col]; maxs = df2plot[column]["Max"][col];  mins = df2plot[column]["Min"][col]

            fig = px.histogram(df.loc[index[col]], x=column, template="presentation",width=900, height=600)
            fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Max: %s mm"%str(np.round(maxs,decimales))))
            fig.add_trace(go.Scatter(x=[None],      y = [None],    mode="lines", line=dict(dash="dash",color="orange", width=0), name="Min: %s mm"%str(np.round(mins,decimales))))
            fig.add_trace(go.Scatter(x=[exp]*2,     y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[2]), name="EXP:  %s mm"%str(np.round(exp,decimales))))
            fig.add_trace(go.Scatter(x=[th+stdp]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1]), name="STD+: %s mm"%str(np.round(stdp,decimales))))
            fig.add_trace(go.Scatter(x=[th]*2,      y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[0]), name="TH:   %s mm"%str(np.round(th,decimales))))
            fig.add_trace(go.Scatter(x=[th-stdm]*2, y = [0,vline], mode="lines", line=dict(dash="dash",color=colors[1]), name="STD-: %s mm"%str(np.round(stdm,decimales))))
            custom_plotly_layout(fig, xaxis_title=xlabel, yaxis_title=ylabel, title=str(index[col])+ " - " +title + " (L%i)"%(col+1)).show()
    
    return fig

def custom_legend_name(fig_px,new_names):
    for i, new_name in enumerate(new_names):
        fig_px.data[i].name = new_name
    return fig_px

def custom_plotly_layout(fig_px, xaxis_title="", yaxis_title="", title="",barmode="stack"):
    # fig_px.update_layout( updatemenus=[ dict( buttons=list([ dict(args=[{"xaxis.type": "linear", "yaxis.type": "linear"}], label="LinearXY", method="relayout"),
    #                                                          dict(args=[{"xaxis.type": "log", "yaxis.type": "log"}],       label="LogXY",    method="relayout"),
    #                                                          dict(args=[{"xaxis.type": "linear", "yaxis.type": "log"}],    label="LogY",     method="relayout"),
    #                                                          dict( args=[{"xaxis.type": "log", "yaxis.type": "linear"}],   label="LogX",     method="relayout") ]),
    #                       direction="down", pad={"r": 10, "t": 10}, showactive=True, x=-0.1, xanchor="left", y=1.5, yanchor="top" ) ] )
    fig_px.update_layout( template="presentation", title=title, xaxis_title=xaxis_title, yaxis_title=yaxis_title, barmode=barmode,
                   font=dict(family="serif"), legend_title_text='', legend = dict(yanchor="top", xanchor="right", x = 0.99), showlegend=True)
    fig_px.update_xaxes(showline=True,mirror=True,zeroline=False)
    fig_px.update_yaxes(showline=True,mirror=True,zeroline=False)
    return fig_px

def show_html(fig_px):
    return pyoff.plot(fig_px, include_mathjax='cdn')

def save_html(fig_px,name):
    return fig_px.write_html(name, include_mathjax = 'cdn')