''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

from src.constants import (
    DISEASE_PATH,
    SYMPTOM_PATH,
    DISEASE_SYMPTOM_PATH
)
class KnowledgeBase:
    def __init__(self, do_filter:bool=False, topk:int=30) -> None:
        '''
        Args:
            - do_filter (bool): filter to topk symptoms and its relevant disease
        '''
        self.diseases = []
        self.symptoms = []
    
    def init_weight(self) -> None:
        ''' Init severity weight for symptom->disease
        1 : no problem 
        2 : mild
        3 : moderate
        4 : severe/dangerous
        reference: https://www.researchgate.net/publication/344898101_Fibromyalgia_Recent_Advances_in_Diagnosis_Classification_Pharmacotherapy_and_Alternative_Remedies/figures?lo=1&utm_source=google&utm_medium=organic
        '''
        pass