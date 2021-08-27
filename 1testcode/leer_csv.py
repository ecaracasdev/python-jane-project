import pandas as pd
import os


abspath = os.path.abspath("mydir/myfile.txt")

def get_max_intensity(filename):  
  csv_data = pd.read_csv(filename,delimiter=';',skiprows=36)
  csv_data['Intensity'] = csv_data['Intensity'].apply(lambda x: float(x.replace(',','.')))
  max_intensity = csv_data["Intensity"].max()
  return max_intensity

max_intensity = get_max_intensity('3uM 1.csv')
print(max_intensity)