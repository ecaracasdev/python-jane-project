import helpers.utils as helper
import pandas as pd
import re

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
    mean = sum(data)/float(len(data))
    max_intensity_sample_one = ''
    max_intensity_sample_two = ''
    max_intensity_sample_three = ''
    if len(data) == 3:
        max_intensity_sample_one = data[0]
        max_intensity_sample_two = data[1]
        max_intensity_sample_three = data[2]
    if len(data) == 2:
        max_intensity_sample_one = data[0]
        max_intensity_sample_two = data[1]
        max_intensity_sample_three = ''

    file_data_dicctionary = {
        "day": day,
        "temperature": temperature,
        "concentration_uM": int(re.findall(r'\d+', aux)[0]),
        "max_intensity_sample_one": max_intensity_sample_one,
        "max_intensity_sample_two": max_intensity_sample_two,
        "max_intensity_sample_three": max_intensity_sample_three,
        "media_Fi": mean
    }
    return file_data_dicctionary 

def create_excel_sheet(file_data_list, day, temperature, writer):
    #create a new dataframe for each new share read 
    file_df = pd.DataFrame(file_data_list)
    file_df_filtered = file_df[(file_df["day"] == day) & (file_df["temperature"] == temperature) & (file_df["concentration_uM"] != 0) ].copy(deep=True)
    file_df_filtered.sort_values(by=['concentration_uM'], inplace=True, ascending=True)

    # write dataframe to excel
    file_df_filtered.to_excel(writer, temperature) 