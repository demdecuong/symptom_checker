''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

from pandas import pandas

def display(text:str):
    print(text)
    
def read_csv_data(path:str) -> pandas.DataFrame:
    data = pd.read_csv(path)
    return data
