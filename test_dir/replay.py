"""
This module is made to replay data like real time from manufacture and received from sensors
"""
import pandas as pd
import pickle

# load the file path
path = "test.xlsx"

# function to load all the sheets from the excel file and create a dataframe
def load_df(link):
    data_frames = []
    excel_file = pd.ExcelFile(link)
    print(excel_file.sheet_names)
    sheets = excel_file.sheet_names[:len(excel_file.sheet_names)-2]
    print(f'Sheets : {sheets}')
    for i in range(len(sheets)-1, -1, -1):
        print(f'loading sheet {i} =====================>')
        data = excel_file.parse(sheets[i])
        data = data.drop(data.index[0])
        data_frames.append(data)
        merged_data = pd.concat(data_frames, ignore_index=True)
        merged_data["Time"] = merged_data["Time"].astype(float)
        merged_data["acc_broche"] = merged_data["acc_broche"].astype(float)
        merged_data["acc_table"] = merged_data["acc_table"].astype(float)
    print("*************file loaded**************")
    return merged_data

df = load_df(path)
df['Time'] = pd.to_datetime(df['Time'])

#Time to serialize the data
with open("replay.pkl", 'wb') as file:
    pickle.dump(df, file)
