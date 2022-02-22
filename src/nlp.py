''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

import Levenshtein
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from typing import Any

class NLPOutput:
    def __init__(self,
        str1:str, 
        str2:str, 
        method:int, 
        threshold:float, 
        score:float, 
        result:bool) -> None:
    self.str1 = str1
    self.str2 = str2
    self.method = method
    self.threshold = threshold
    self.score = score
    self.result = result

    def update(self,score):
        self.score = score
        self.result = bool(self.score >= self.threshold)

class NLP:
    ''' A class handles NLP technique
    Supported features:
    - compare_string() compare string
    '''
    def __init__(self): -> None:
        pass

    def compare_string(self,str1:str,str2:str,method:str,threshold:float) -> Any:
        ''' Compute string distance between str1 & str2
        Args:
            - method (str)
            - threshold (float) : 
        '''
        assert method in ['fuzzy','semantic','edit']

        result = NLPOutput(
            str1 = str1,
            str2 = str2,
            method = method,
            threshold = threshold,
            score = 0,
            result = False
        )

        if method == 'fuzzy':
            score = self.compute_fuzzy(str1,str2)
        
        if method == 'edit':
            score = self.compute_edit(str1,str2)

        if method == 'semantic':
            score = self.compute_semantic(str1,str2)

        # Update result
        result.update(score)
        return result

    def compute_edit(str1:str,str2:str) -> int:
        return Levenshtein.distance(str1, str2)
    
    def compute_fuzzy(str1:str,str2:str) -> float:
        return fuzz.ratio(str1,str2)

    def compute_semantic(str1:str,str2:str) -> float:
        ''' Reference world data
        TODO
        '''
        return 0