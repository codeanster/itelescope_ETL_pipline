#transform the data by unzipping and uploading data to google drive

import os
import glob as glob
import pandas as pd
from zipfile import ZipFile

stem_directory = r'C:\Users\Dell i71050ti\Downloads\\'
download_directory = glob.glob(r'C:\Users\Dell i71050ti\Downloads\Plan-20*')
file = download_directory[0]
z = file.split('\\')[-1].split('.')[0]


#get latest record from pandas
df = pd.read_csv('meta.csv')
latest_df = df.head(1)
name = df['name']
date = df['date']

#rename file
print(f'Current filename: {file}')
new_file = f'{stem_directory + name[0]}.zip'
print(f'Changed filename: {new_file}')
os.rename(file,new_file)
print('name changed')


# #I'm just going to be running this on my local pc for now
save_directory = r'D:\astrophotography\\'

print('Extracting file')
with ZipFile(new_file,'r') as zipObj:
    zipObj.extractall(save_directory)
    
print('Renaming')
#rename 
os.rename(save_directory + 'Plan-20',save_directory + name[0])

os.remove(new_file)