import numpy as np
import re

class StatisticsData():
    def __init__(self, data):
        self.data = data
        self.max_intensity_one = 0
        self.max_intensity_two = 0
        self.max_intensity_three = 0
        self.set_statistics()
        self.set_max_intensities()
    
    def set_statistics(self):
        self.mean = np.mean(self.data)
        self.standard_deviation = np.std(self.data)
        self.percentage_error = (self.standard_deviation/self.mean)*100
    
    def set_max_intensities(self):
        if len(self.data) >= 3:
            self.max_intensity_one = self.data[0]
            self.max_intensity_two = self.data[1]
            self.max_intensity_three = self.data[2]
        if len(self.data) == 2:
            self.max_intensity_one = self.data[0]
            self.max_intensity_two = self.data[1]
            self.max_intensity_three = ''
            
    
    def get_organized_data(self, day, temperature, aux):
        organized_data = {
                "day": day,
                "temperature": temperature,
                "concentration_uM": int(re.findall(r'\d+', aux)[0]),
                "max_intensity_sample_one": self.max_intensity_one,
                "max_intensity_sample_two": self.max_intensity_two,
                "max_intensity_sample_three": self.max_intensity_three,
                "media_Fi": self.mean,
                "standard_deviation": self.standard_deviation,
                "percentage_error": self.percentage_error
            }
        return organized_data