import pandas as pd
import numpy as np

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