''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

from src.inference_engine import InferenceEngine
from src.constants.text import *
from src.constants.config import *
from src.utils import display
from string import Template
from typing import List, Dict

class Application:
    def __init__(self):
        self.service = InferenceEngine()

        self.current_response = {
            "symptom" : [],
            "triage": "",
            "possible_disease":[],
            "asked_symptom": []
        }

        self.personal_info = {
            "name": "",
            "sex" : "",
            "age" : ""  
        }

        self.COMPARE_METHOD = COMPARE_METHOD
        if COMPARE_METHOD == 'fuzzy':
            self.THRESHOLD = FUZZY_THRESHOLD
        if COMPARE_METHOD == 'semantic':
            self.THRESHOLD = SEMANTIC_THRESHOLD
        if COMPARE_METHOD == 'edit':
            self.THRESHOLD = EDIT_THRESHOLD

    def run(self):
        # clear history
        self.clear_history()

        # personal info
        # self.greeting()
        # self.get_personal_info()

        # first symptom
        self.get_user_symptom(mode="first")

        num_turn = 0
        while True:
            if self.is_end_run(num_turn):
                # if not too confidence, ask other 
                # TODO 
                # self.get_user_symptom(type="other")
               
                # show result then exit 
                self.show_result()
                break

            asked_symptom = self.service.get_next_symptom(self.current_response)
            self.get_user_symptom(asked_symptom=asked_symptom,mode="next")
            num_turn += 1

    def get_user_symptom(self,asked_symptom:str="",mode:str="first") -> dict:
        ''' Dealt with user symptoms
        Args:
            - first (bool): This is the first symptom from user 
        '''
        
        assert mode in ['first','other','verify','relevant','next']
        user_symptoms = []

        # user typing
        if mode in ['first', 'other']:
            symptom = self.asking_symptom(mode=mode)

            '''There are 3 situations for user's symptom:
            1. not included in the current database
            2. included with high fuzzy score
            3. included

            - For 1: ask another one
            - For 2: ask to verify final symptom -> 3
            - For 3; ask relevant symptoms
            '''
            situation = self.user_typing_dealer(symptom)

            # For 1: if symptom not in self.service.knowledge_base.symptoms
            if situation == 1:
                symptom = self.get_user_symptom(mode="other")
            
            # For 2: Verify final symptom
            if situation == 2:
                relevant_symptoms = self.service.get_relevant_symptoms(symptom,self.COMPARE_METHOD,self.THRESHOLD)
                # relevant_symptoms.remove(symptom) # remove itself
                for s in relevant_symptoms:
                    response = self.asking_symptom(symptom=s,mode="verify")
                    if response == 'Y':
                        user_symptoms.append(s)
                    self.update_asked_symptom(s)
                    
            # For 3: Get relevant symptom
            if situation == 3: 
                user_symptoms.append(symptom)
                self.update_asked_symptom(symptom)
                # List of relevant symptoms
                relevant_symptoms = self.service.get_relevant_symptoms(symptom,self.COMPARE_METHOD,self.THRESHOLD)
                relevant_symptoms.remove(symptom) # remove itself
                for s in relevant_symptoms:
                    response = self.asking_symptom(s,mode="relevant")
                    if response == 'Y':
                        user_symptoms.append(s)
                    self.update_asked_symptom(s)
                    

        # user multiple-choice
        if mode == 'next':
            response = self.asking_symptom(symptom=asked_symptom,mode=mode)
            if response == 'Y':
                user_symptoms.append(asked_symptom)
            self.update_asked_symptom(asked_symptom)

        self.update_current_response(symptoms=user_symptoms)
        print(self.current_response)

    def update_current_response(self,symptoms:List=[]) -> None:
        ''' Update self.current_response
        '''
        self.update_symptom(symptoms)
        self.update_possible_disease()
        self.update_triage()

    def update_symptom(self,symptoms:List) -> None:
        self.current_response["symptom"].extend(symptoms)

    def update_possible_disease(self) -> None:
        #TODO
        possible_diseases = self.service.get_possible_disease(self.current_response['symptom'])
        self.current_response['possible_disease'] = possible_diseases
    
    def update_triage(self):
        #TODO
        triage_confidence = 0
        for d in self.current_response['possible_disease']:
            triage_confidence += d['confidence']

        triage_confidence = triage_confidence / len(self.current_response['possible_disease'])

        if triage_confidence <= SELF_CARE_CONFIDENCE:
            self.current_response['triage'] = SELF_CARE
        elif triage_confidence <= GENERAL_PROCEDURE_CONFIDENCE:
            self.current_response['triage'] = GENERAL_PROCEDURE
        else:
            self.current_response['triage'] = EMERGENCE

    def update_asked_symptom(self,symptom):
        self.current_response['asked_symptom'].append(symptom)

    def greeting(self) -> None:
        display(GREETING) 

    def get_personal_info(self) -> None:
        name = input(NAME_INPUT)
        sex = input(SEX_INPUT)
        age = input(AGE_INPUT)
        self.update_personal_info(
            name=name,
            sex=sex,
            age=age
        )

    def update_personal_info(self,name:str="",sex:str="",age:str="") -> None:
        ''' Update self.personal_info
        '''
        if name != "":
            self.personal_info['name'] = name

        if sex != "":
            self.personal_info['sex'] = name

        if age != "":
            self.personal_info['age'] = name

    def clear_history(self) -> None:
        ''' Clear all previous information
        '''
        self.current_response = {
            "symptom" : [],
            "triage": "",
            "possible_disease":[],
            "asked_symptom": []
        }

        self.personal_info = {
            "name": "",
            "sex" : "",
            "age" : ""
        }

    def asking_symptom(self,symptom:str="",mode:str="first") -> str:
        ''' Solve asking template
        '''
        assert mode in ['first','other','verify','relevant','next']

        if mode == 'first':
            symptom = input(FIRST_SYMPTOM_INPUT)

        if mode == 'other':
            symptom = input(OTHER_SYMPTOM_INPUT)

        if mode in ['relevant','verify']:
            t = Template(RELEVANT_SYMPTOM_TEMPLATE)
            symptom = input(t.substitute(symptom=symptom))
            
        if mode == 'next':
            t = Template(ASK_SYMPTOM_TEMPLATE)
            symptom = input(t.substitute(symptom=symptom))

        return symptom.capitalize()

    def is_end_run(self,num_turn:int) -> bool:
        ''' End session conditions
        1. num turn 
        2. disease confidence
        '''
        if num_turn >= MAXIMUM_TURN or self.current_response['possible_disease'][0]['confidence'] >= DISEASE_CONFIDENCE:
            return True
        return False

    def show_result(self) -> None:
        ''' Show final result
        - possible disease
        - triage #TODO
        - treatment #TODO
        - suggested doctor #TODO
        '''

        display("Possible disease:")
        for disease in self.current_response['possible_disease']:
            display(disease['name'])

    def user_typing_dealer(self,symptom:str) -> int:
        ''' Divide into user typing into 1,2,3 situations:
        1. not included in the current database
        2. included with high fuzzy score
        3. included
        Args:
            - symptom (str) : entered symptom from user
        '''
        relevant_symptoms = self.service.get_relevant_symptoms(symptom,self.COMPARE_METHOD,self.THRESHOLD)        
        if symptom in relevant_symptoms:
            try:
                relevant_symptoms.remove(symptom)
                return 3
            except:
                return 2
        return 1