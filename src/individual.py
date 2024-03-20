import sys; sys.path.insert(0, '../'); from lib import *

show_plots = [inquirer.List('show_plots', message="Do you want to show the plots?",choices=['Yes', 'No'],default='No')]
answer = inquirer.prompt(show_plots)
show_plots = answer['show_plots'][0].lower() in ['true', '1', 't', 'y', 'yes']

##### CONFIGURE YOUR FILES #####
data_dir = "../data/"
folders = os.listdir(data_dir)

# Create a list of choices where each choice is a file in the data directory
chosen_folders = [inquirer.Checkbox('folder', message="Choose your folders", choices=sorted(folders))]

# Prompt the user to choose a file
answers = inquirer.prompt(chosen_folders)
chosen_folders = answers['folder']
print("Chosen folders:", chosen_folders)

# Create a dictionary to store the mode values for each file
folder_config = {}
# Load the existing data from the YAML file
try:
    with open('folder_config.yml', 'r') as file:
        folder_config = yaml.safe_load(file)
except FileNotFoundError:
    folder_config = {}

# Prompt the user for a mode value for each file
for file in chosen_folders:
    if file not in folder_config:
        print(folder_config.keys())
        if file in folder_config.keys(): 
            print(f"Mode for {file} is already set to {folder_config[file]['mode']}")
            mode_default = folder_config[file]["mode"]
        else: 
            mode_default = 10
            folder_config[file] = {}

            mode_question = [inquirer.Text('mode', message=f"Enter mode for {file}", default=mode_default)]
            sipm_question = [inquirer.List('sipm', message=f"Enter SiPM type for {file}", choices=['HPK', 'FBK'])]
            mode_answer = inquirer.prompt(mode_question)
            sipm_answer = inquirer.prompt(sipm_question)
            folder_config[file]["mode"] = mode_answer['mode']
            folder_config[file]["sipm"] = sipm_answer['sipm']

# Save the file modes to the YAML file
with open('folder_config.yml', 'w') as file:
    yaml.dump(folder_config, file)

##### RUN THE ANALYSIS #####
# Labels for the columns
for f,folder in enumerate(chosen_folders):
    if folder_config[folder]["sipm"] == "HPK":
        pcbs_labels = ['Diametro Taladro 1 (S1)', 'Posición Y S1', 'Posición X S1', 'Diametro Taladro 2 (S6)', 'Posición Y TS6',
                        'Posición X TS6', 'Planitud PCB','Anchura (media)', 'Anchura (maxima)', 'Longitud (media)',
                        'Longitud (maxima)', 'Longitud rebaje izquierdo', 'Anchura rebaje izquierdo', 'Longitud rebaje derecho',
                        'Anchura rebaje derecho', 'Distancia entre taladros']
        sipm_labels = ['Anchura', 'Longitud', 'Posición X', 'Posición Y', 'Planitud', 'Altura']
        pina_labels = ['Posición X', 'Posición Y', 'Altura Pin'] #pin anverso
        pinr_labels = ['Altura Pin'] #pin reverso
        hlat_labels = []
        distances   = {"pcb_header":3,"anv_header":2,"rev_header":2,"lat_header":2,
                        "row_pcbs":197,"row_sipm":197,"row_pina":197,"row_pinr":24,"row_hlat":24,
                        "col_pcbs":11, "col_sipm":14, "col_pina":17, "col_pinr":11,"col_hlat":10}
    elif folder_config[folder]["sipm"] == "FBK":
        pcbs_labels = ['Diametro Taladro 1 (S1)', 'Posición Y S1', 'Posición X S1', 'Diametro Taladro 2 (S6)', 'Posición Y TS6',
                        'Posición X TS6', 'Planitud PCB','Anchura (media)', 'Anchura (maxima)', 'Longitud (media)',
                        'Longitud (maxima)', 'Longitud rebaje izquierdo', 'Anchura rebaje izquierdo', 'Longitud rebaje derecho',
                        'Anchura rebaje derecho', 'Distancia entre taladros']
        sipm_labels = ['Anchura', 'Longitud', 'Posición X', 'Posición Y', 'Planitud', 'Altura','Anchura caja', 'Longitud caja',
                        'Posicion X caja', 'Posicion Y caja']
        pina_labels = ['Posición X', 'Posición Y', 'Altura Pin'] #pin anverso
        pinr_labels = ['Altura Pin'] #pin reverso
        hlat_labels = ['Altura superficie media','Altura superficie maxima','Altura reverso media','Altura reverso maxima']
        distances   = {"pcb_header":3,"anv_header":2,"rev_header":2,"lat_header":4,
                        "row_pcbs":257,"row_sipm":257,"row_pina":257,"row_pinr":24,"row_hlat":48,
                        "col_pcbs":11, "col_sipm":14, "col_pina":17, "col_pinr":11,"col_hlat":10}
    

    p, s, r, a, h = data2npy(folder="../data/"+folder+"/", pcbs_labels=pcbs_labels, sipm_labels=sipm_labels, pins_labels=pina_labels,
                            hlat_labels=hlat_labels, mode=int(folder_config[folder]["mode"]), distances=distances, debug=False)
    pcbs = p; sipm = s; pinr = r; pina = a; 
    if hlat_labels != []: hlat = h

    df_pcbs_ids = df_display(pcbs, labels=pcbs_labels+["IDs","DATE"], name="pcbs", terminal_output=True, save=True,save_path="../data/"+folder+"/fit_data/",)
    df_sipm_ids = df_display(sipm, labels=sipm_labels+["IDs","DATE"], name="sipm", terminal_output=True, save=True,save_path="../data/"+folder+"/fit_data/", 
                            index=["SiPM #1","SiPM #2","SiPM #3","SiPM #4","SiPM #5","SiPM #6"]*len(df_pcbs_ids))
    df_pina_ids = df_display(pina, labels=pina_labels+["IDs","DATE"], name="pina", terminal_output=True, save=True,save_path="../data/"+folder+"/fit_data/",
                            index=["Pin #1","Pin #2","Pin #3","Pin #4","Pin #5","Pin #6","Pin #7","Pin #8"]*len(df_pcbs_ids))
    df_pinr_ids = df_display(pinr, labels=pinr_labels+["IDs","DATE"], name="pinr", terminal_output=True, save=True,save_path="../data/"+folder+"/fit_data/", 
                            index=["Pin #1","Pin #2","Pin #3","Pin #4","Pin #5","Pin #6","Pin #7","Pin #8"]*len(df_pcbs_ids))
    if hlat_labels != []: df_hlat_ids = df_display(hlat, labels=hlat_labels+["IDs","DATE"], name="hlat", terminal_output=True, save=True,
                                                   save_path="../data/"+folder+"/fit_data/",
                                                   index=["SiPM #1","SiPM #2","SiPM #3","SiPM #4","SiPM #5","SiPM #6"]*len(df_pcbs_ids))
        

    # DataFrames with loaded data + IDs (caja, board, sipm, useful for identification)
    df_pcbs = df_pcbs_ids[pcbs_labels] 
    df_sipm = df_sipm_ids[sipm_labels]
    df_pina = df_pina_ids[pina_labels]
    df_pinr = df_pinr_ids[pinr_labels]
    if hlat_labels != []:df_hlat = df_hlat_ids[hlat_labels]

    pcbs_mean,pcbs_std,pcbs_max,pcbs_min = npy2df(df_pcbs[pcbs_labels], [])
    sipm_mean,sipm_std,sipm_max,sipm_min = npy2df(df_sipm[sipm_labels], ["Posición Y"])
    pina_mean,pina_std,pina_max,pina_min = npy2df(df_pina[pina_labels], ["Posición Y"])
    pinr_mean,pinr_std,pinr_max,pinr_min = npy2df(df_pinr[pinr_labels], [])
    if hlat_labels != []:hlat_mean,hlat_std,hlat_max,hlat_min = npy2df(df_hlat[hlat_labels])

    df_pcbs_exp = pd.DataFrame(np.array((pcbs_mean,pcbs_max,pcbs_min)),columns=pcbs_labels, index=["Experimental", "Max", "Min"])
    df_sipm_exp = pd.DataFrame(np.array((sipm_mean,sipm_max,sipm_min)),columns=sipm_labels, index=["Experimental", "Max", "Min"])
    df_pina_exp = pd.DataFrame(np.array((pina_mean,pina_max,pina_min)),columns=pina_labels, index=["Experimental", "Max", "Min"])
    df_pinr_exp = pd.DataFrame(np.array((pinr_mean,pinr_max,pinr_min)),columns=pinr_labels, index=["Experimental", "Max", "Min"])
    if hlat_labels != []: df_hlat_exp = pd.DataFrame(np.array((hlat_mean,hlat_max,hlat_min)),columns=hlat_labels, index=["Experimental", "Max", "Min"])

    # Load the *_hpk.txt files as dataframes
    df_pcbs_all = pd.read_csv('../Specifications/pcbs_%s.txt'%folder_config[folder]["sipm"].lower(), sep='\t')
    df_sipm_all = pd.read_csv('../Specifications/sipm_%s.txt'%folder_config[folder]["sipm"].lower(), sep='\t')
    df_pina_all = pd.read_csv('../Specifications/pina_%s.txt'%folder_config[folder]["sipm"].lower(), sep='\t')
    df_pinr_all = pd.read_csv('../Specifications/pinr_%s.txt'%folder_config[folder]["sipm"].lower(), sep='\t')

    # Add the "Experimental", "Max", and "Min" rows
    df_pcbs_all = pd.concat((df_pcbs_all,df_pcbs_exp.loc[["Experimental", "Max", "Min"]]))
    df_sipm_all = pd.concat((df_sipm_all,df_sipm_exp.loc[["Experimental", "Max", "Min"]]))
    df_pina_all = pd.concat((df_pina_all,df_pina_exp.loc[["Experimental", "Max", "Min"]]))
    df_pinr_all = pd.concat((df_pinr_all,df_pinr_exp.loc[["Experimental", "Max", "Min"]]))

    # Rename the row names
    df_pcbs_all = df_pcbs_all.rename(index={0: "Theoretical", 1: "STD+", 2: "STD-"})
    df_sipm_all = df_sipm_all.rename(index={0: "Theoretical", 1: "STD+", 2: "STD-"})
    df_pina_all = df_pina_all.rename(index={0: "Theoretical", 1: "STD+", 2: "STD-"})
    df_pinr_all = df_pinr_all.rename(index={0: "Theoretical", 1: "STD+", 2: "STD-"})

    # Display the dataframes
    pd.set_option('display.float_format', '{:.2f}'.format)
    print("\n---- PCBs %s ----"%folder_config[folder]["sipm"])
    print(df_pcbs_all)
    print("\n---- SiPM %s ----"%folder_config[folder]["sipm"])
    print(df_sipm_all)
    print("\n---- Pins_anv %s ----"%folder_config[folder]["sipm"])
    print(df_pina_all)
    print("\n---- Pins_rev %s ----"%folder_config[folder]["sipm"])
    print(df_pinr_all)

    if hlat_labels != []: 
        df_hlat_all = pd.read_csv('../Specifications/hlat_%s.txt'%folder_config[folder]["sipm"].lower(), sep='\t')
        df_hlat_all = pd.concat((df_hlat_all,df_hlat_exp.loc[["Experimental", "Max", "Min"]]))
        df_hlat_all = df_hlat_all.rename(index={0: "Theoretical", 1: "STD+", 2: "STD-"})
        print("\n---- HLAT %s ----"%folder_config[folder]["sipm"])
        print(df_hlat_all)


    print("PCB")
    check_especifications(df_pcbs_ids, df_pcbs_all, pcbs_labels, "../data/"+folder+"/fit_data/errors_pcb")

    print("SiPMs")
    check_especifications(df_sipm_ids, df_sipm_all, sipm_labels, "../data/"+folder+"/fit_data/errors_sipm")

    if hlat_labels != []:
        print("HLAT")
        check_especifications(df_hlat_ids, df_hlat_all, hlat_labels, "../data/"+folder+"/fit_data/errors_hlat")

    print("PIN_ANV")
    check_especifications(df_pina_ids, df_pina_all, pina_labels, "../data/"+folder+"/fit_data/errors_pina")

    print("PIN_REV")
    check_especifications(df_pinr_ids, df_pinr_all, pinr_labels, "../data/"+folder+"/fit_data/errors_pinr")

    ##### TIME TO PLOT #####
    if not os.path.exists("../data/"+folder+"/images"):
        os.makedirs("../data/"+folder+"/images")
    print("PLOTTING")
    
    # PCBS (ignoring the burrs here) ##
    titles = ['PCB - Diameter S1', 'PCB - Distance to Drill (D1)', 'PCB - Position X (S1)', 'PCB - Diameter S6', 'PCB - Distance to Drill (D2)', 'PCB - Position X (S6)', 'PCB - Width','PCB - Length', 'PCB - Distancia entre taladros']
    xlabel = ['Diameter S1 [mm]', 'Position [mm]', 'Position [mm]', 'Diametro Taladro 2 (S6)', 'Position [mm]', 'Position [mm]', 'Width [mm]','Lenght [mm]', 'Distancia entre taladros']
    ylabel = ['Nº PCBs'] * len(titles)
    colums = ['Diametro Taladro 1 (S1)', 'Posición Y S1', 'Posición X S1', 'Diametro Taladro 2 (S6)', 'Posición Y TS6', 'Posición X TS6', 'Anchura (maxima)','Longitud (maxima)', 'Distancia entre taladros']
    colors = ["purple","orange","red"]
    df_raw = df_pcbs_ids
    df_fin = df_pcbs_all

    for i in range(len(titles)): 
        fig = plotlytos(titles[i], xlabel[i], ylabel[i], df_raw, df_fin, colums[i],colors=colors,decimales=3,text_auto=False,
                        save=True,save_path="../data/"+folder+"/images/")
        if show_plots: fig.show()
        fig.write_image("../data/"+folder+"/images/"+str(titles[i])+".png")
    
    # ACCUMULATED BURRS ##
    aux_pcbs1 =  pd.concat([df_pcbs_ids['Longitud rebaje izquierdo'], df_pcbs_ids['Longitud rebaje derecho']], axis=0, ignore_index=True)
    aux_pcbs2 =  pd.concat([df_pcbs_ids['Anchura rebaje izquierdo'],  df_pcbs_ids['Anchura rebaje derecho']],  axis=0, ignore_index=True)
    aux_pcbs1 = pd.DataFrame(aux_pcbs1, columns=['Length']); aux_pcbs1["IDs"] = df_pcbs_ids["IDs"].to_list()*2
    aux_pcbs2 = pd.DataFrame(aux_pcbs2, columns=['Width']);  aux_pcbs2["IDs"] = df_pcbs_ids["IDs"].to_list()*2

    aux_mean1 = pd.DataFrame()
    aux_mean2 = pd.DataFrame()
    aux_mean1["Length"] = df_pcbs_all['Longitud rebaje derecho']
    aux_mean2["Width"]  = df_pcbs_all['Anchura rebaje derecho']

    titles = ['PCB - burr lenght (R1)', 'PCB - burr width (R2)']
    xlabel = ['Length [mm]', 'Width [mm]']
    ylabel = ['Nº PCBs'] * len(titles)
    colums = ['Length', 'Width']
    colors = ["purple","orange","red"]
    df_raw = [aux_pcbs1, aux_pcbs2]
    df_fin = [aux_mean1, aux_mean2]

    for i in range(len(titles)): 
        fig = plotlytos(titles[i], xlabel[i], ylabel[i], df_raw[i], df_fin[i], colums[i],colors=colors,decimales=3,text_auto=False,
                        save=True,save_path="../data/"+folder+"/images/")
        if show_plots: fig.show()
        fig.write_image("../data/"+folder+"/images/"+str(titles[i])+".png")
    ## SiPMs ##
    titles = ['SiPMs - Position X', 'Position Y', 'SiPMs - Height']
    xlabel = ['Position [mm]', 'Position [mm]', 'Height [mm]']
    ylabel = ['Nº SiPMs'] * len(titles)
    colums = ['Posición X', 'Posición Y', 'Altura']
    colors = ["purple","orange","red"]
    df_raw = df_sipm_ids
    df_fin = df_sipm_all

    for i in range(len(titles)): 
        fig = plotlytos(titles[i], xlabel[i], ylabel[i], df_raw, df_fin, colums[i],colors=colors,decimales=2,text_auto=False,
                        save=True,save_path="../data/"+folder+"/images/")
        if show_plots: fig.show()
        fig.write_image("../data/"+folder+"/images/"+str(titles[i])+".png")

    # Pins ##
    titles = ['Pins - Position X (front)', 'Position Y (front)', 'Pins - weld height', 'Pins - Height']
    xlabel = ['Position [mm]', 'Position [mm]', 'Height [mm]', 'Height [mm]']
    ylabel = ['Nº Pins'] * len(titles)
    colums = ['Posición X', 'Posición Y', 'Altura Pin', 'Altura Pin']
    colors = ["purple","orange","red"]
    df_raw = [df_pina_ids] * (len(titles)-1) + [df_pinr_ids]
    df_fin = [df_pina_all] * (len(titles)-1) + [df_pinr_all]

    for i in range(len(titles)): 
        fig = plotlytos(titles[i], xlabel[i], ylabel[i], df_raw[i], df_fin[i], colums[i],colors=colors,text_auto=False,
                        save=True,save_path="../data/"+folder+"/images/") 
        if show_plots: fig.show()
        fig.write_image("../data/"+folder+"/images/"+str(titles[i])+".png")


    if hlat_labels != []:
        ## Lateral heights ##
        titles = ['SiPMs - Height (mean front)', 'SiPMs - Height (max front)', 'SiPMs - Height (mean back)', 'SiPMs - Height (max back)']
        xlabel = ['Height [mm]', 'Height [mm]', 'Height [mm]', 'Height [mm]']
        ylabel = ['Nº SiPMs'] * len(titles)
        colums = ['Altura superficie media','Altura superficie maxima','Altura reverso media','Altura reverso maxima']
        colors = ["purple","orange","red"]
        df_raw = df_hlat_ids
        df_fin = df_hlat_all
        for i in range(len(titles)): 
            fig = plotlytos(titles[i], xlabel[i], ylabel[i], df_raw, df_fin, colums[i],colors=colors,decimales=2,text_auto=False,
                            save=True,save_path="../data/"+folder+"/images/")
            # if show_plots: fig.show()
            fig.write_image("../data/"+folder+"/images/"+str(titles[i])+".png")

    del pcbs, sipm, pinr, pina
    del df_pcbs_ids, df_sipm_ids, df_pina_ids, df_pinr_ids
    del df_pcbs, df_sipm, df_pina, df_pinr
    del df_pcbs_all, df_sipm_all, df_pina_all, df_pinr_all
    del df_pcbs_exp, df_sipm_exp, df_pina_exp, df_pinr_exp
    del pcbs_mean,pcbs_std,pcbs_max,pcbs_min
    del sipm_mean,sipm_std,sipm_max,sipm_min
    del pina_mean,pina_std,pina_max,pina_min
    del pinr_mean,pinr_std,pinr_max,pinr_min
    del df_raw, df_fin
    try: del hlat, df_hlat_ids, df_hlat, df_hlat_all, df_hlat_exp, hlat_mean, hlat_std, hlat_max, hlat_min
    except: pass
    gc.collect()
