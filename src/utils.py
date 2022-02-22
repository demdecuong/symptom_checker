''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

import pandas as pd

def display(text:str):
    print(text)
    
def read_csv_data(path:str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data
