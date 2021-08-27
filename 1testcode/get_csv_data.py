import os
import re
import pandas as pd
import numpy as np


# assign path
path, dirs, files = next(os.walk("./muestras/"))
file_count = len(files)

# declaring temp variables 
concentration_list_temp = []
list_concentration_avg_intensity = []
concentration_temp = ''

#declaring functions 
def get_max_intensity(filename):  
  csv_data = pd.read_csv(filename,delimiter=';',skiprows=36)
  csv_data['Intensity'] = csv_data['Intensity'].apply(lambda x: float(x.replace(',','.')))
  max_intensity = csv_data["Intensity"].max()
  return max_intensity

# proccesing data 
for i in range(file_count):
    concentration = files[i].split()[0]

    if concentration == 'control':
            concentration = '0'

    max_intensity = get_max_intensity("./muestras/"+files[i])

    if concentration == concentration_temp or concentration_temp == '':
        concentration_list_temp.append(max_intensity)
        concentration_temp = concentration

    if (concentration != concentration_temp and concentration_temp != '') or i == file_count-1:
        mean = sum(concentration_list_temp)/float(len(concentration_list_temp))
        temp_dicctionary = {
            'concentration[uM]': int(re.findall(r'\d+', concentration_temp)[0]),
            'media[Fi]': mean
        }
        concentration_list_temp = []
        concentration_list_temp.append(max_intensity)
        concentration_temp = concentration
        list_concentration_avg_intensity.append(temp_dicctionary)

# creating a new data frame
df_concentration_avg_intensity = pd.DataFrame(list_concentration_avg_intensity) 
df_concentration_avg_intensity.sort_values(by=['concentration[uM]'], inplace=True, ascending=True)
print(df_concentration_avg_intensity)