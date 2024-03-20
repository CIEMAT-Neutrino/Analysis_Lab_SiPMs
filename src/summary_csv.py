import sys; sys.path.insert(0, '../'); from lib import *

choices = ['HPK', 'FBK']
question = [inquirer.List('sipm', message="Choose your SiPMs", choices=choices)]
answers = inquirer.prompt(question)
chosen_sipm = answers['sipm']

chosen_folder = "../data/" + chosen_sipm

print("Chosen folders:", chosen_folder)

from openpyxl import Workbook

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
    print("Processing", txt_file)
    name = str(txt_file.replace(".txt",""))
    if "errors" not in txt_file: 
        df = pd.read_csv(os.path.join(fit_data_folder, txt_file),header=None,sep="\t")
        df = df.drop(df.index[0])
        if "df_pcbs" in name: df.drop(df.columns[0], axis=1, inplace=True)
        df = df.apply(pd.to_numeric, errors='ignore')
        print("BEFORE\n",df)
        df = df.dropna(axis=1)
        if config[name]["drop"] != []:
            for col in config[name]["drop"]:
                print("DROPPING",col)
                df = df.drop(df.columns[col], axis=1)
        print("HEADERS",len(config[name]["headers"]))
        print(len(df.columns))
        df.columns = config[name]["headers"]
        df = df.round(3)
        df = df.sort_values(by=[df.columns[-2], df.columns[-1]])
        print("AFTER\n",df)
        df.to_excel(excel_writer, sheet_name=os.path.splitext(txt_file)[0], index=False)
excel_writer.save()
excel_writer.close()
