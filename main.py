import helpers.utils as helper
import pandas as pd
import os
import re

# assign path
path, dirs, files = next(os.walk("./ejemplo/"))
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
        print(f'dia {dirs[i]}')
        day_dir = os.listdir(path + dirs[i])
        day_count = len(day_dir)
        for j in range(day_count):
            print(f'temperatura {day_dir[j]}')
            temperature_dir = os.listdir(f'{path}{dirs[i]}/{day_dir[j]}')
            temperature_count = len(temperature_dir)
            for k in range(temperature_count):
                path_concentration_file = f'{path}{dirs[i]}/{day_dir[j]}/{temperature_dir[k]}'
                # print(f'path to file: {path_concentration_file}')
                print(f'file name {temperature_dir[k]}')

                concentration = temperature_dir[k].split()[0]

                print(f'concentracion {concentration}')
                if concentration == 'control':
                        concentration = '0'

                max_intensity = ''
                if helper.is_txt(temperature_dir[k]):
                    max_intensity = max_intensity_from_txt(path_concentration_file)
                if helper.is_csv(temperature_dir[k]):
                    max_intensity = max_intensity_from_csv(path_concentration_file)
                
                print(f'maxima intensidad {max_intensity}')
                if concentration == concentration_temp or concentration_temp == '':
                    concentration_list_temp.append(max_intensity)
                    concentration_temp = concentration

                if (concentration != concentration_temp and concentration_temp != '') or k == temperature_count-1:
                    mean = sum(concentration_list_temp)/float(len(concentration_list_temp))
                    temp_dicctionary = {
                        'day': dirs[i],
                        'temperature': day_dir[j],
                        'concentration[uM]': int(re.findall(r'\d+', concentration_temp)[0]),
                        'media[Fi]': mean
                    }
                    concentration_list_temp = []
                    concentration_list_temp.append(max_intensity)
                    concentration_temp = concentration
                    list_concentration_avg_intensity.append(temp_dicctionary)
            
    print(list_concentration_avg_intensity)


    # df = max_intensity_from_txt('3uM 1.1.txt')
    # print(df)

if __name__ == "__main__":
    main()