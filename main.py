from classes.statistics_data import StatisticsData
from classes.file_data import FileData
import helpers.fs as fs
import pandas as pd
import os

# assign path
path, days_directory, files = next(os.walk("./datos/"))
days_count = len(days_directory)

def main():
    file_data_list = []

    for i in range(days_count):
        temperature_directory = os.listdir(path + days_directory[i])
        temperature_count = len(temperature_directory)
        
        # # create excel writer object
        writer = pd.ExcelWriter(f'{days_directory[i]}.xlsx')

        for j in range(temperature_count):
            concentration_file = os.listdir(f'{path}{days_directory[i]}/{temperature_directory[j]}')
            temperature_count = len(concentration_file)
            concentration_aux = ''
            concentration_list = []

            for k in range(temperature_count):
                path_concentration_file = f'{path}{days_directory[i]}/{temperature_directory[j]}/{concentration_file[k]}'
                file_data = FileData(path_concentration_file, concentration_file[k])
                concentration = file_data.get_concentration()
                max_intensity = file_data.get_max_intensity()
                
                if (concentration == concentration_aux or concentration_aux == '') and max_intensity != '':
                    concentration_list.append(max_intensity)
                    concentration_aux = concentration

                if ((concentration != concentration_aux and concentration_aux != '') or k == temperature_count-1) and max_intensity != '':
                    statistics_data = StatisticsData(concentration_list)
                    statistics_dicctionary = statistics_data.get_organized_data(day=days_directory[i],temperature=temperature_directory[j],aux=concentration_aux)
                    
                    concentration_list = []
                    concentration_list.append(max_intensity)
                    file_data_list.append(statistics_dicctionary)
                    concentration_aux = concentration

            fs.create_excel_sheet(file_data_list, day=days_directory[i], temperature=temperature_directory[j], writer=writer)

        writer.save()
        print(f'{days_directory[i]}.xlsx succesfully created')

    # print(f'file_list {file_data_list}')
    

if __name__ == "__main__":
    main()