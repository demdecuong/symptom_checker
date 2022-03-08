''' 
Author: Nguyen Phuc Minh
Lastest update: 8/3/2022
'''

from src.knowledge_base import KnowledgeBase
from src.nlp import NLP
from typing import List, Dict
from itertools import islice
from src.constants.config import (
    MAXIMUM_POSSIBLE_DISEASE,
    DISEASE_SEVERITY_CONFIDENCE,
    DISEASE_DEFAULT_CONFIDENCE
)
from src.constants.conditions import (
    APPLICATION_MODE
)
from data.symptom_category import SYMPTOM_CATEGORY

class InferenceEngine:
    ''' A wrapper class handle KnowledgeBase and InferenceEngine
    '''
    def __init__(self,
                init_weight_method:str='default',
                do_filter_symptom:bool=False, 
                do_filter_disease:bool=True, 
                topk_disease:int=60,
                topk_symptom:int=30) -> None:

        self.knowledge_base = KnowledgeBase(
            init_weight_method=init_weight_method,
            do_filter_symptom=do_filter_symptom,
            do_filter_disease=do_filter_disease,
            topk_symptom=topk_symptom,
            topk_disease=topk_disease
        )

        self.nlp = NLP()

        self.init_weight_method = init_weight_method

    def get_relevant_symptoms(self,given_symptom:str,method:str,threshold:float) -> List:
        ''' Get relevant symptoms from database
        '''
        assert method in ['fuzzy','semantic','edit']

        relevant_symptoms = []
        
        if self.knowledge_base.do_filter:
            symptoms = list(self.knowledge_base.common_symptoms.keys())
        else:
            symptoms = self.knowledge_base.symptoms['name'].tolist()

        for s in symptoms:
            compare_output = self.nlp.compare_string(
                str1=given_symptom,
                str2=s,
                method=method,
                threshold=threshold)

            if compare_output.result or self.nlp.is_included(s,given_symptom):
                relevant_symptoms.append(s)

        return relevant_symptoms

    def get_next_symptom(self,current_response:Dict,app_mode="horizontal") -> str:
        ''' Return next symptom should be asked based on current_response
        # TODO        
        '''
        assert app_mode in APPLICATION_MODE
        
        # get top possible disease
        possible_disease = current_response['possible_disease'] # dict
    
        # get relevant symptoms that not included in current_response
        # severity-based
        relevant_symptoms = {}
        for d in possible_disease:
            dname = d['name']
            symptoms = self.knowledge_base.get_symptoms_from_disease(dname) # dict
            
            for s in symptoms:
                if s['name'] not in current_response['asked_symptom']:
                    if s['name'] not in list(relevant_symptoms.keys()):
                        relevant_symptoms[s['name']] = s['confidence']
                    else:
                        relevant_symptoms[s['name']] += s['confidence']

        # re-ranking symptom
        N = 3
        next_symptom = dict(sorted(relevant_symptoms.items(), key=lambda x: x[1], reverse=True)[:3])
        next_symptom = list(next_symptom.keys())[0] # pick 1st one

        if app_mode == 'horizontal':
            pass
        elif app_mode == 'vertical':
            # get symptom category
            pass
            
        return next_symptom

    def get_possible_disease(self,symptoms:List) -> List[Dict]:
        '''
        Return:
            - result [{
                "name" (str),
                "confidence" (float)
            }]
        '''
        result = {}

        # get all relevant disease
        relevant_disease = self.knowledge_base.get_common_disease(symptoms)
        for d,conf in relevant_disease.items():
            if d not in list(result.keys()):
                result[d] = conf
            else:        
                result[d] += conf

        if self.init_weight_method == 'default':
            # scale confidence score
            result = {k:v/len(self.knowledge_base.get_symptoms_from_disease(k)) for k,v in result.items()}     
        
        # sorted 
        N = 5
        top_diseases = {k: v for k, v in sorted(result.items(), reverse=True, key=lambda item: item[1])[:N]}
        result = []
        for k,v in top_diseases.items():
            result.append({
                "name" : k,
                "confidence":v
            })

        return result
        
    def is_included_symptom_category(self,symptom:str) -> bool:
        ''' Check whether a symptom is supported in SYMPTOM_CATEGORY
        '''
        if symptom in list(SYMPTOM_CATEGORY.keys()):
            return True
        return False
    
    def get_symptom_category(self,symptom) -> dict:
        return SYMPTOM_CATEGORY[symptom]

    def get_disease_end_confidence(self):
        if self.init_weight_method == 'random':
            return DISEASE_SEVERITY_CONFIDENCE
        if self.init_weight_method == 'default':
            return DISEASE_DEFAULT_CONFIDENCE