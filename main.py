import helpers.utils as helper
import pandas as pd
import os
import re

# assign path
path, dirs, files = next(os.walk("./datos/"))
dirs_count = len(dirs)
file_count = len(files)

concentration_list_temp = []
list_concentration_avg_intensity = []
concentration_temp = ''

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

    df_intensities = pd.DataFrame(intensity_list)
    max_intensity = df_intensities["Intensity"].max()
    return max_intensity

def max_intensity_from_csv(file_path):  
  csv_data = pd.read_csv(file_path,delimiter=';',skiprows=36)
  csv_data['Intensity'] = csv_data['Intensity'].apply(lambda x: float(x.replace(',','.')))
  max_intensity = csv_data["Intensity"].max()
  return max_intensity


def main():
    concentration_list_temp = []
    list_concentration_avg_intensity = []
    concentration_temp = ''

    for i in range(dirs_count):
        # print(f'dia {dirs[i]}')
        day_dir = os.listdir(path + dirs[i])
        day_count = len(day_dir)
        
        # # create excel writer object
        writer = pd.ExcelWriter(f'{dirs[i]}.xlsx')

        for j in range(day_count):
            # print(f'temperatura {day_dir[j]}')
            temperature_dir = os.listdir(f'{path}{dirs[i]}/{day_dir[j]}')
            temperature_count = len(temperature_dir)
            concentration_temp = ''
            concentration_list_temp = []

            for k in range(temperature_count):
                path_concentration_file = f'{path}{dirs[i]}/{day_dir[j]}/{temperature_dir[k]}'

                concentration = temperature_dir[k].split()[0]

                if concentration.lower() == 'control':
                        concentration = '0'

                max_intensity = ''
                if helper.is_txt(temperature_dir[k]):
                    # print(f'path to file: {path_concentration_file}')
                    # print(f'file name {temperature_dir[k]}')
                    # print(f'concentracion {concentration}')
                    max_intensity = max_intensity_from_txt(path_concentration_file)
                if helper.is_csv(temperature_dir[k]):
                    max_intensity = max_intensity_from_csv(path_concentration_file)
                
                if (concentration == concentration_temp or concentration_temp == '') and max_intensity != '':
                    # print(f'maxima intensidad {max_intensity}')
                    concentration_list_temp.append(max_intensity)
                    concentration_temp = concentration

                if ((concentration != concentration_temp and concentration_temp != '') or k == temperature_count-1) and max_intensity != '':
                    mean = sum(concentration_list_temp)/float(len(concentration_list_temp))
                    if len(concentration_list_temp) == 3:
                        max_intensity_sample_one = concentration_list_temp[0]
                        max_intensity_sample_two = concentration_list_temp[1]
                        max_intensity_sample_three = concentration_list_temp[2]
                    if len(concentration_list_temp) == 2:
                        max_intensity_sample_one = concentration_list_temp[0]
                        max_intensity_sample_two = concentration_list_temp[1]
                        max_intensity_sample_three = ''

                    temp_dicctionary = {
                        "day": dirs[i],
                        "temperature": day_dir[j],
                        "concentration_uM": int(re.findall(r'\d+', concentration_temp)[0]),
                        "max_intensity_sample_one": max_intensity_sample_one,
                        "max_intensity_sample_two": max_intensity_sample_two,
                        "max_intensity_sample_three": max_intensity_sample_three,
                        "media_Fi": mean
                    }
                    concentration_list_temp = []
                    concentration_list_temp.append(max_intensity)
                    list_concentration_avg_intensity.append(temp_dicctionary)
                    concentration_temp = concentration

            #create a new dataframe for each new share read 
            df = pd.DataFrame(list_concentration_avg_intensity)
            df_filtered = df[(df["day"] == dirs[i]) & (df["temperature"] == day_dir[j]) & (df["concentration_uM"] != 0) ].copy(deep=True)
            df_filtered.sort_values(by=['concentration_uM'], inplace=True, ascending=True)

            # write dataframe to excel
            df_filtered.to_excel(writer, day_dir[j]) 

        writer.save()
        print(f'{dirs[i]}.xlsx succesfully created')

if __name__ == "__main__":
    main()