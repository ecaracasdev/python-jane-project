import helpers.utils as helper
import pandas as pd

class FileData():
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.max_intensity = ''
        self.set_concentration()
    
    def set_concentration(self):
        self.concentration = self.file_name.split()[0]
        if self.concentration.lower() == 'control':
                        self.concentration = '0'
    
    def get_concentration(self):
        return self.concentration
    
    def max_intensity_from_txt(self):
        intensity_list = [] 
        with open(self.file_path) as f:
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

    def max_intensity_from_csv(self):  
        csv_data = pd.read_csv(self.file_path,delimiter=';',skiprows=36)
        csv_data['Intensity'] = csv_data['Intensity'].apply(lambda x: float(x.replace(',','.')))
        max_intensity = csv_data["Intensity"].max()
        return max_intensity

    def get_max_intensity(self):
        if helper.is_txt(self.file_name):
            self.max_intensity = self.max_intensity_from_txt()
        if helper.is_csv(self.file_name):
            self.max_intensity = self.max_intensity_from_csv()
        
        return self.max_intensity