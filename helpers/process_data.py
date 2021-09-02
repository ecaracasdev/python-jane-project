import helpers.utils as helper
from helpers.statisticsClass import Intensity
import pandas as pd
import numpy as np

def max_intensity_from_txt(file_path):
    intensity_list = [] 
    with open(file_path) as f:
        line = f.readline()
        while line:
            line = helper.replacer(f.readline(),[','],';',2)
            if helper.is_valid_data(line):
                line = line.split(';')
                temp_line = {
                    'Intensity': float(line[1].replace(',','.'))
                }
                intensity_list.append(temp_line)

    file_df_intensities = pd.DataFrame(intensity_list)
    max_intensity = file_df_intensities["Intensity"].max()
    return max_intensity

def max_intensity_from_csv(file_path):  
  csv_data = pd.read_csv(file_path,delimiter=';',skiprows=36)
  csv_data['Intensity'] = csv_data['Intensity'].apply(lambda x: float(x.replace(',','.')))
  max_intensity = csv_data["Intensity"].max()
  return max_intensity

def set_dicctionary_data(data, day, temperature, aux):
    file_data = Intensity(data)
    #add a set concentration data for the file_data in the Intensity class
    return file_data.set_organized_data(day,temperature,aux)

def create_excel_sheet(file_data_list, day, temperature, writer):
    #create a new dataframe for each new share read 
    file_df = pd.DataFrame(file_data_list)

    # set the concentration y a local scope variable that will be used for alterate the columns of the file_df
    list_filtered = list(filter(lambda data: data['concentration_uM'] == 0, file_data_list))
    media_Fo = list_filtered[0]['media_Fi']

    file_df_filtered = file_df[(file_df["day"] == day) & (file_df["temperature"] == temperature) & (file_df["concentration_uM"] != 0) ].copy(deep=True)
    file_df_filtered['Fo/Fi'] = file_df_filtered.apply(lambda row: media_Fo/row.media_Fi, axis=1)
    file_df_filtered['log[M]'] = file_df_filtered.apply(lambda row: np.log(row.concentration_uM), axis=1)
    file_df_filtered['log[Fo-Fi/Fo]'] = file_df_filtered.apply(lambda row: np.log((media_Fo- row.media_Fi)/media_Fo), axis=1)
    file_df_filtered.sort_values(by=['concentration_uM'], inplace=True, ascending=True)

    # filter the file_df but this time for the concentration only an make a new row in the excel with this info
    concentration_df = file_df[(file_df["day"] == day) & (file_df["temperature"] == temperature) & (file_df["concentration_uM"] == 0) ].copy(deep=True)

    # write dataframe to excel
    file_df_filtered.to_excel(writer, temperature) 
    concentration_df.to_excel(writer, temperature, startrow= 13)