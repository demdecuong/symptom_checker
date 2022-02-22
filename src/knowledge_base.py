''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

import os
import random
import pandas as pd
from src.constants.kb import (
    DISEASE_PATH,
    SYMPTOM_PATH,
    DISEASE_SYMPTOM_PATH,
    SAVE_WEIGHT_PATH
)
from src.utils import read_csv_data
from typing import List, Dict

class KnowledgeBase:
    def __init__(self,
                init_weight_method:str="random",
                do_filter:bool=False, 
                topk:int=30) -> None:
        '''
        Args:
            - do_filter (bool): filter to topk symptoms and its relevant disease
        '''
        self.diseases = read_csv_data(DISEASE_PATH)
        self.symptoms = read_csv_data(SYMPTOM_PATH)
        self.diseases_symptoms = read_csv_data(DISEASE_SYMPTOM_PATH)

        self.topk = topk # number of common symptoms
        self.do_filter = do_filter
        self.init_weight_method = init_weight_method
        self.SAVE_WEIGHT_PATH = SAVE_WEIGHT_PATH

        if do_filter:
            self.common_diseases, self.common_symptoms = self.filter_data()
            print(f"From {self.topk} symptoms, database has {len(self.common_diseases)} disease")

        if os.listdir('data/weight/'):
            fname = os.path.join('data/weight/',os.listdir('data/weight/')[0])
            print(f'Reading weight from {fname}')
            self.weighted_data = read_csv_data(fname)
        else:
            self.weighted_data = self.init_weight(init_weight_method)
        
    def init_weight(self,method:str) -> pd.DataFrame:
        ''' Init severity weight for symptom->disease
        0 : not related
        1 : no problem 
        2 : mild
        3 : moderate
        4 : severe/dangerous
        reference: https://www.researchgate.net/publication/344898101_Fibromyalgia_Recent_Advances_in_Diagnosis_Classification_Pharmacotherapy_and_Alternative_Remedies/figures?lo=1&utm_source=google&utm_medium=organic
        '''
        assert method in ['random','frequency']
        print("Initialize weight. This will takes some minutes")

        weighted_data = []
        if self.do_filter:
            row_symptom = list(self.common_symptoms.keys())
            col_disease = list(self.common_diseases.keys())
        else:
            row_symptom = self.symptoms['name'].tolist()
            col_disease = self.diseases['name'].tolist()

        if method == 'random':
            SAVE_WEIGHT_PATH = self.SAVE_WEIGHT_PATH.replace('.csv','') + '_random.csv'
        elif method == 'frequency':
            SAVE_WEIGHT_PATH = self.SAVE_WEIGHT_PATH.replace('.csv','') + '_freq.csv'
        
        # Create list of lists
        for s in row_symptom:
            if method == 'random':
                w = [random.randint(0, 4) if self.is_symptom_disease_related(s,d) else 0 for d in col_disease]
            elif method == 'frequency':
                w = [self.calculate_symptom_disease_weight(s,d) if self.is_symptom_disease_related(s,d) else 0 for d in col_disease ]

            weighted_data.append(w)

        weighted_data = pd.DataFrame(weighted_data, columns = col_disease)
        weighted_data.insert(0, "symptom", row_symptom, True)        
        # Save
        weighted_data.to_csv(SAVE_WEIGHT_PATH)
        return weighted_data

    def from_symptom_id_to_name(self,id:int) -> str:
        symptom_name = self.symptoms.loc[self.symptoms['id'] == id]
        return symptom_name['name'].item()

    def from_disease_id_to_name(self,id:int) -> str:
        disease_name = self.diseases.loc[self.diseases['id'] == id]
        return disease_name['name'].item()

    def from_symptom_to_id(self,name:str) -> int:
        id = self.symptoms.loc[self.symptoms['name'] == name]
        return id['id'].item()

    def from_disease_to_id(self,name:str) -> int:
        id = self.diseases.loc[self.diseases['name'] == name]
        return id['id'].item()

    def filter_data(self) -> List[Dict]:
        ''' Get topk symptoms and its relevant disease
        '''
        # get topk symptoms 
        common_symptom = self.get_common_symptom()

        # get common disease
        common_disease = self.get_common_disease(list(common_symptom.keys()))
        
        return common_disease, common_symptom
        
    def get_common_symptom(self) -> Dict:
        symptom_freq = {}
        for id in self.diseases_symptoms['symptom_id']:
            if id not in symptom_freq:
                symptom_freq[id] = 1
            else:
                symptom_freq[id] += 1 
        name_symptom_freq = {}
        for k,v in symptom_freq.items():
            name_symptom_freq[self.from_symptom_id_to_name(k)] = v
        common_symptom = {k: v for k, v in sorted(name_symptom_freq.items(), reverse=True, key=lambda item: item[1])[:self.topk]}
        return common_symptom

    def get_common_disease(self,common_symptoms:List) -> Dict:
        ''' Get common disease from topk symptoms
        '''
        common_disease = {}

        for s in common_symptoms:
            try:
                symptom_id = self.from_symptom_to_id(s)
            except:
                symptom_id = self.from_symptom_to_id(s.capitalize())

            relevant_disease = self.diseases_symptoms.loc[self.diseases_symptoms['symptom_id'] == symptom_id]
            relevant_disease = relevant_disease['disease_id'].values
            relevant_disease = [self.from_disease_id_to_name(item) for item in relevant_disease]
            for d in relevant_disease:
                if d not in common_disease:
                    common_disease[d] = 1
                else: 
                    common_disease[d] += 1
        return common_disease

    def is_symptom_disease_related(self,symptom:str,disease:str) -> bool:
        symptom_id = self.from_symptom_to_id(symptom)
        disease_id = self.from_disease_to_id(disease)
        
        relevant_disease = self.diseases_symptoms.loc[self.diseases_symptoms['symptom_id'] == symptom_id]
        relevant_disease = relevant_disease['disease_id'].values
        if disease_id in relevant_disease:
            return True
        return False

    def calculate_symptom_disease_weight(self,symptom:str,disease:str) -> int:
        ''' Scale to range [0,4] based on ...
        TODO
        '''
        return random.randint(0, 4)
        
    def get_symptoms_from_disease(self,disease:str) -> List[Dict]:
        ''' Get symptom from given disease and its weight
        {
            "name" (str)
            "severity" (int)
        }
        '''
        result = []
        disease_id = self.from_disease_to_id(disease)

        symptoms = self.diseases_symptoms.loc[self.diseases_symptoms['disease_id']==disease_id]['symptom_id'].values
        symptoms = [self.from_symptom_id_to_name(item) for item in symptoms]

        for s in symptoms:
            severity = self.weighted_data[disease].iloc[0]
            result.append({
                "name" : s,
                "severity": severity
            })
        
        return result

if __name__ == '__main__':
    kb = KnowledgeBase(do_filter=True,topk=30)
