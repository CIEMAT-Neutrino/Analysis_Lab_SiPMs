import sys; sys.path.insert(0, '../'); from lib import *

choices = ['HPK', 'FBK']
question = [inquirer.List('sipm', message="Choose your SiPMs", choices=choices)]
answers = inquirer.prompt(question)
chosen_sipm = answers['sipm']

show_plots = [inquirer.List('show_plots', message="Do you want to show the plots?",choices=['Yes', 'No'],default='No')]
answer = inquirer.prompt(show_plots)
show_plots = answer['show_plots'][0].lower() in ['true', '1', 't', 'y', 'yes']

write_xlsx = [inquirer.List('write_xlsx', message="Do you want to save the grouped outputs in a XLSX file?",choices=['Yes', 'No'],default='Yes')]
xlsx = inquirer.prompt(write_xlsx)
write_xlsx = xlsx['write_xlsx'][0].lower() in ['true', '1', 't', 'y', 'yes']

with open('folder_config.yml', 'r') as file: folder_config = yaml.safe_load(file)

# Find the folders that match the chosen sipm
chosen_folders = [folder for folder, config in folder_config.items() if config['sipm'] == chosen_sipm]

print("Chosen folders:", chosen_folders)
with open('format_config.yml', 'r') as file: format_config = yaml.safe_load(file)
format_config = format_config[chosen_sipm]

##### RUN THE ANALYSIS #####
# Labels for the columns
for f,folder in enumerate(chosen_folders):
    p, s, r, a, h = data2npy(folder="../data/"+folder+"/", pcbs_labels=format_config["pcbs_labels"], sipm_labels=format_config["sipm_labels"], 
                             pina_labels=format_config["pina_labels"],pinr_labels=format_config["pinr_labels"],
                            hlat_labels=format_config["hlat_labels"], mode=int(folder_config[folder]["mode"]), distances=format_config["distances"], debug=False)
    if f == 0: 
        pcbs = p; sipm = s; pinr = r; pina = a; 
        if format_config["hlat_labels"] != []: hlat = h
    else:
        pcbs = np.concatenate((pcbs,p),axis=0)
        sipm = np.concatenate((sipm,s),axis=0)
        pinr = np.concatenate((pinr,r),axis=0)
        pina = np.concatenate((pina,a),axis=0)
        if format_config["hlat_labels"] != []: hlat = np.concatenate((hlat,h),axis=0)

df_pcbs_ids = df_display(pcbs, labels=format_config["pcbs_labels"]+["IDs","DATE"], name="pcbs", terminal_output=True, save=True,save_path="../data/"+chosen_sipm+"/fit_data/",)
df_sipm_ids = df_display(sipm, labels=format_config["sipm_labels"]+["IDs","DATE"], name="sipm", terminal_output=True, save=True,save_path="../data/"+chosen_sipm+"/fit_data/", 
                        index=["SiPM #1","SiPM #2","SiPM #3","SiPM #4","SiPM #5","SiPM #6"]*len(df_pcbs_ids))
df_pina_ids = df_display(pina, labels=format_config["pina_labels"]+["IDs","DATE"], name="pina", terminal_output=True, save=True,save_path="../data/"+chosen_sipm+"/fit_data/",
                        index=["Pin #1","Pin #2","Pin #3","Pin #4","Pin #5","Pin #6","Pin #7","Pin #8"]*len(df_pcbs_ids))
df_pinr_ids = df_display(pinr, labels=format_config["pinr_labels"]+["IDs","DATE"], name="pinr", terminal_output=True, save=True,save_path="../data/"+chosen_sipm+"/fit_data/", 
                        index=["Pin #1","Pin #2","Pin #3","Pin #4","Pin #5","Pin #6","Pin #7","Pin #8"]*len(df_pcbs_ids))
if format_config["hlat_labels"] != []: df_hlat_ids = df_display(hlat, labels=format_config["hlat_labels"]+["IDs","DATE"], name="hlat", terminal_output=True, save=True,
                                                save_path="../data/"+chosen_sipm+"/fit_data/",
                                                index=["SiPM #1","SiPM #2","SiPM #3","SiPM #4","SiPM #5","SiPM #6"]*len(df_pcbs_ids))
    

# DataFrames with loaded data + IDs (caja, board, sipm, useful for identification)
df_pcbs = df_pcbs_ids[format_config["pcbs_labels"]] 
df_sipm = df_sipm_ids[format_config["sipm_labels"]]
df_pina = df_pina_ids[format_config["pina_labels"]]
df_pinr = df_pinr_ids[format_config["pinr_labels"]]
if format_config["hlat_labels"] != []:df_hlat = df_hlat_ids[format_config["hlat_labels"]]

pcbs_mean,pcbs_std,pcbs_max,pcbs_min = npy2df(df_pcbs[format_config["pcbs_labels"]], [])
sipm_mean,sipm_std,sipm_max,sipm_min = npy2df(df_sipm[format_config["sipm_labels"]], ["Posición Y"])
pina_mean,pina_std,pina_max,pina_min = npy2df(df_pina[format_config["pina_labels"]], ["Posición Y"])
pinr_mean,pinr_std,pinr_max,pinr_min = npy2df(df_pinr[format_config["pinr_labels"]], [])
if format_config["hlat_labels"] != []:hlat_mean,hlat_std,hlat_max,hlat_min = npy2df(df_hlat[format_config["hlat_labels"]])

df_pcbs_exp = pd.DataFrame(np.array((pcbs_mean,pcbs_max,pcbs_min)),columns=format_config["pcbs_labels"], index=["Experimental", "Max", "Min"])
df_sipm_exp = pd.DataFrame(np.array((sipm_mean,sipm_max,sipm_min)),columns=format_config["sipm_labels"], index=["Experimental", "Max", "Min"])
df_pina_exp = pd.DataFrame(np.array((pina_mean,pina_max,pina_min)),columns=format_config["pina_labels"], index=["Experimental", "Max", "Min"])
df_pinr_exp = pd.DataFrame(np.array((pinr_mean,pinr_max,pinr_min)),columns=format_config["pinr_labels"], index=["Experimental", "Max", "Min"])
if format_config["hlat_labels"] != []: df_hlat_exp = pd.DataFrame(np.array((hlat_mean,hlat_max,hlat_min)),columns=format_config["hlat_labels"], index=["Experimental", "Max", "Min"])

# Load the *_hpk.txt files as dataframes
df_pcbs_all = pd.read_csv('../Specifications/pcbs_%s.txt'%chosen_sipm.lower(), sep='\t')
df_sipm_all = pd.read_csv('../Specifications/sipm_%s.txt'%chosen_sipm.lower(), sep='\t')
df_pina_all = pd.read_csv('../Specifications/pina_%s.txt'%chosen_sipm.lower(), sep='\t')
df_pinr_all = pd.read_csv('../Specifications/pinr_%s.txt'%chosen_sipm.lower(), sep='\t')

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
print("\n---- PCBs %s ----"%chosen_sipm)
print(df_pcbs_all)
print("\n---- SiPM %s ----"%chosen_sipm)
print(df_sipm_all)
print("\n---- Pins_anv %s ----"%chosen_sipm)
print(df_pina_all)
print("\n---- Pins_rev %s ----"%chosen_sipm)
print(df_pinr_all)

if format_config["hlat_labels"] != []: 
    df_hlat_all = pd.read_csv('../Specifications/hlat_%s.txt'%chosen_sipm.lower(), sep='\t')
    df_hlat_all = pd.concat((df_hlat_all,df_hlat_exp.loc[["Experimental", "Max", "Min"]]))
    df_hlat_all = df_hlat_all.rename(index={0: "Theoretical", 1: "STD+", 2: "STD-"})
    print("\n---- HLAT %s ----"%chosen_sipm)
    print(df_hlat_all)


print("PCB")
check_especifications(df_pcbs_ids, df_pcbs_all, format_config["pcbs_labels"], "../data/"+chosen_sipm+"/fit_data/errors_pcb")

print("SiPMs")
check_especifications(df_sipm_ids, df_sipm_all, format_config["sipm_labels"], "../data/"+chosen_sipm+"/fit_data/errors_sipm")

if format_config["hlat_labels"] != []:
    print("HLAT")
    check_especifications(df_hlat_ids, df_hlat_all, format_config["hlat_labels"], "../data/"+chosen_sipm+"/fit_data/errors_hlat")

print("PIN_ANV")
check_especifications(df_pina_ids, df_pina_all, format_config["pina_labels"], "../data/"+chosen_sipm+"/fit_data/errors_pina")

print("PIN_REV")
check_especifications(df_pinr_ids, df_pinr_all, format_config["pinr_labels"], "../data/"+chosen_sipm+"/fit_data/errors_pinr")

##### TIME TO PLOT #####
if not os.path.exists("../data/"+chosen_sipm+"/images"):
    os.makedirs("../data/"+chosen_sipm+"/images")

print("PLOTTING")
# PCBS (ignoring the burrs here) ##
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
                    save=True,save_path="../data/"+chosen_sipm+"/images/")
    if show_plots: fig.show()
    fig.write_image("../data/"+chosen_sipm+"/images/"+str(titles[i])+".png")
    
titles = ['PCB - Diameter S1', 'PCB - Distance to Drill (D1)', 'PCB - Position X (S1)', 'PCB - Diameter S6', 'PCB - Distance to Drill (D2)', 'PCB - Position X (S6)', 'PCB - Width','PCB - Length', 'PCB - Distancia entre taladros']
xlabel = ['Diameter S1 [mm]', 'Position [mm]', 'Position [mm]', 'Diametro Taladro 2 (S6)', 'Position [mm]', 'Position [mm]', 'Width [mm]','Lenght [mm]', 'Distancia entre taladros']
ylabel = ['Nº PCBs'] * len(titles)
colums = ['Diametro Taladro 1 (S1)', 'Posición Y S1', 'Posición X S1', 'Diametro Taladro 2 (S6)', 'Posición Y TS6', 'Posición X TS6', 'Anchura (maxima)','Longitud (maxima)', 'Distancia entre taladros']
colors = ["purple","orange","red"]
df_raw = df_pcbs_ids
df_fin = df_pcbs_all

for i in range(len(titles)): 
    fig = plotlytos(titles[i], xlabel[i], ylabel[i], df_raw, df_fin, colums[i],colors=colors,decimales=3,text_auto=False,
                    save=True,save_path="../data/"+chosen_sipm+"/images/")
    if show_plots: fig.show()
    fig.write_image("../data/"+chosen_sipm+"/images/"+str(titles[i])+".png")


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
                    save=True,save_path="../data/"+chosen_sipm+"/images/")
    if show_plots: fig.show()
    fig.write_image("../data/"+chosen_sipm+"/images/"+str(titles[i])+".png")

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
                    save=True,save_path="../data/"+chosen_sipm+"/images/") 
    if show_plots: fig.show()
    fig.write_image("../data/"+chosen_sipm+"/images/"+str(titles[i])+".png")


if format_config["hlat_labels"] != []:
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
                        save=True,save_path="../data/"+chosen_sipm+"/images/")
        if show_plots: fig.show()
        fig.write_image("../data/"+chosen_sipm+"/images/"+str(titles[i])+".png")



if write_xlsx:
    print("\n------------------------------------------------------------\n")
    print("WRITING XLSX")
    from openpyxl import Workbook
    chosen_folder = "../data/" + chosen_sipm
    print("Chosen folder:", chosen_folder)

    excel_writer = pd.ExcelWriter(chosen_folder+'/summary_'+chosen_sipm+'.xlsx', engine='openpyxl')
    fit_data_folder = os.path.join(chosen_folder, 'fit_data')
    txt_files = [f for f in os.listdir(fit_data_folder) if f.endswith('.txt')]
    if chosen_sipm == 'HPK':
        config = {"df_pcbs":{
                            "headers":["Diameter_(S1)","Y_Position_(S1)","X_Position_(S1)","Diameter_(S2)","Y_Position_(S6)","X_Position_(S6)",
                            "Width","Length","Burr_length_(R1-rigth)","Burr_width_(R2-left)","Burr_length_(R1-rigth)","Burr_width_(R2-rigth)",
                            "Distance_drills","ID","DATE_END_ANALYSIS"],
                            "drop":[6,7,9]
                            },
                    "df_sipm":{
                            "headers":["Position","Width","Length","X_Position","Y_Position","Heigth","ID","DATE_END_ANALYSIS"],
                            "drop":[4]
                            },
                    "df_pina":{
                            "headers":["Position","X_Position","Y_Position","Heigth","ID","DATE_END_ANALYSIS"],
                            "drop":[]
                            },
                    "df_pinr":{
                            "headers":["Position","Heigth","ID","DATE_END_ANALYSIS"],
                            "drop":[]
                            }
                    }
        
    if chosen_sipm == 'FBK':
        config = {"df_pcbs":{
                            "headers":["Diameter_(S1)","Y_Position_(S1)","X_Position_(S1)","Diameter_(S2)","Y_Position_(S6)","X_Position_(S6)",
                            "Width","Length","Burr_length_(R1-rigth)","Burr_width_(R2-left)","Burr_length_(R1-rigth)","Burr_width_(R2-rigth)",
                            "Distance_drills","ID","DATE_END_ANALYSIS"],
                            "drop":[6,7,9]
                            },
                    "df_sipm":{
                            "headers":["Position","Width","Length","X_Position","Y_Position","Heigth",
                                        'Box_width', 'Box_length','Box_X_Position', 'Box_Y_Position',
                                        "ID","DATE_END_ANALYSIS"],
                            "drop":[4] # AQUI HAY MAS INFO 
                            },
                    "df_pina":{
                            "headers":["Position","X_Position","Y_Position","Heigth","ID","DATE_END_ANALYSIS"],
                            "drop":[]
                            },
                    "df_pinr":{
                            "headers":["Position","Heigth","ID","DATE_END_ANALYSIS"],
                            "drop":[]
                            },
                    "df_hlat":{
                            "headers":["Position","Front_height_(mean)","Front_height_(max)","Back_height_(mean)","Back_height_(max)",
                                        "ID","DATE_END_ANALYSIS"],
                            "drop":[]
                            }
                    }


    # Loop over each text file
    for txt_file in txt_files:
        if "errors" not in txt_file: 
            print("Processing", txt_file)
            name = str(txt_file.replace(".txt",""))
            df = pd.read_csv(os.path.join(fit_data_folder, txt_file),header=None,sep="\t")
            df = df.drop(df.index[0])
            if "df_pcbs" in name: df.drop(df.columns[0], axis=1, inplace=True)
            df = df.apply(pd.to_numeric, errors='ignore')
            # print("BEFORE\n",df)
            df = df.dropna(axis=1)
            if config[name]["drop"] != []:
                for col in config[name]["drop"]:
                    # print("DROPPING",col)
                    df = df.drop(df.columns[col], axis=1)
            # print("HEADERS",len(config[name]["headers"]))
            # print(len(df.columns))
            df.columns = config[name]["headers"]
            df = df.round(3)
            df = df.sort_values(by=[df.columns[-2], df.columns[-1]])
            # print("AFTER\n",df)
            df.to_excel(excel_writer, sheet_name=os.path.splitext(txt_file)[0], index=False)
    excel_writer.save()
    excel_writer.close()
    print('\033[92m'+"XLSX written in", chosen_folder+'/summary_'+chosen_sipm+'.xlsx'+'\033[0m')
    print("\n------------------------------------------------------------")