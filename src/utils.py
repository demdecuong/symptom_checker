''' 
Author: Nguyen Phuc Minh
Lastest update: 1/3/2022
'''

import pandas as pd
from scipy import spatial
from typing import List

def display(text:str):
    print(text)
    
def read_csv_data(path:str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data

def get_cosine_similarity(d1:List,d2:List) -> float:
    ''' Compute cosine similarity between 2 list
    ''' 
    result = 1 - spatial.distance.cosine(d1, d2)
    return result
