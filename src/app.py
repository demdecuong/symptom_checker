''' 
Author: Nguyen Phuc Minh
Lastest update: 8/3/2022
'''

from src.inference_engine import InferenceEngine
from src.constants.text import *
from src.constants.config import *
from src.utils import display
from string import Template
from typing import List, Dict, Tuple
from src.constants.conditions import (
    APPLICATION_MODE,
    GET_SYMPTOM_MODE,
    TYPING_SYMPTOM_MODE,
    SYMPTOM_PERIOD,
    SYMPTOM_SEVERITY,
    SYMPTOM_RELATED 
)

class Application:
    def __init__(self,
                init_weight_method:str,
                do_filter_symptom=False,
                do_filter_disease=True,
                topk_symptom:int=30,
                topk_disease:int=60) -> None:
                    
        self.service = InferenceEngine(
            init_weight_method=init_weight_method,
            do_filter_symptom=do_filter_symptom,
            do_filter_disease=do_filter_disease,
            topk_symptom=topk_symptom,
            topk_disease=topk_disease
        )

        self.current_response = {
            "symptom" : [],
            "triage": "",
            "possible_disease":[],
            "asked_symptom": [],
            "asked category" : [],
            "disease_period" : ""
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

        # end condition
        self.DISEASE_CONFIDENCE = self.service.get_disease_end_confidence()
        self.MAXIMUM_TURN = MAXIMUM_TURN
        
    def run(self, app_mode='horizontal'):
        assert app_mode in APPLICATION_MODE

        # clear history
        self.clear_history()

        # personal info
        # self.greeting()
        # self.get_personal_info()

        # first symptom
        self.get_user_symptom(mode="first",app_mode=app_mode)

        num_turn = 0
        while True:
            if self.is_end_run(num_turn):
                # if not too confidence, ask other 
                # TODO 
                # self.get_user_symptom(type="other")
               
                # show result then exit 
                self.show_result()
                break

            asked_symptom = self.service.get_next_symptom(
                current_response=self.current_response,
                app_mode=app_mode
            )                
            self.get_user_symptom(asked_symptom=asked_symptom,mode="next",app_mode=app_mode)
            num_turn += 1

    def get_user_symptom(self,asked_symptom:str="",mode:str="first",app_mode="horizontal") -> dict:
        ''' Dealt with user symptoms
        Args:
            - first (bool): This is the first symptom from user 
        '''
        assert app_mode in APPLICATION_MODE
        assert mode in GET_SYMPTOM_MODE
        user_symptoms = []

        # user typing
        if mode in TYPING_SYMPTOM_MODE:
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

                if app_mode == 'horizontal':
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

                elif app_mode == 'vertical' and self.service.is_included_symptom_category(symptom):
                    symptom_category = self.service.get_symptom_category(symptom) # dict
                    
                    user_chosen_symptom, asked_symptom = self.asking_vertical_question(symptom_category)
                    
                    for s_ in user_chosen_symptom:
                        user_symptoms.append(s_)
                    
                    for s_ in asked_symptom:
                        self.update_asked_symptom(s_)
                        
        # user multiple-choice
        if mode == 'next':
            response = self.asking_symptom(symptom=asked_symptom,mode=mode)
            if response == 'Y':
                user_symptoms.append(asked_symptom)
                self.update_asked_symptom(asked_symptom)

                if app_mode == 'vertical' and self.service.is_included_symptom_category(asked_symptom):
                    symptom_category = self.service.get_symptom_category(asked_symptom) # dict
                    
                    user_chosen_symptom, asked_symptom = self.asking_vertical_question(symptom_category)
                    
                    for s_ in user_chosen_symptom:
                        user_symptoms.append(s_)
                    
                    for s_ in asked_symptom:
                        self.update_asked_symptom(s_)
            else:
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
            "asked_symptom": [],
            "asked category" : [],
            "disease_period" : ""
        }

        self.personal_info = {
            "name": "",
            "sex" : "",
            "age" : ""
        }

    def asking_symptom(self,symptom:str="",mode:str="first") -> str:
        ''' Solve asking template
        '''
        assert mode in GET_SYMPTOM_MODE

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
        if num_turn >= self.MAXIMUM_TURN or self.current_response['possible_disease'][0]['confidence'] >= self.DISEASE_CONFIDENCE:
            return True
        return False

    def show_result(self) -> None:
        ''' Show final result
        - possible disease
        - triage #TODO
        - treatment #TODO
        - suggested doctor #TODO
        '''
        display("=================================================================")
        display("Tóm tắt:")
        display(self.current_response["triage"])
        display("Các bệnh có khả năng:")
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
    
    def asking_vertical_question(self,symptom_category:str) -> Tuple[List]:
        ''' Resolve question related to symptom category
        Return:
            - user_chosen_symptom (list) 
            - asked_symptom (list)
        '''
        user_chosen_symptom = []
        asked_symptom = []

        question_types = symptom_category.keys()

        for qtype in question_types:
            print('=======================================================================')
            if (qtype in SYMPTOM_PERIOD) or (qtype in SYMPTOM_SEVERITY):
                for i, choice in enumerate(list(symptom_category[qtype]["choices"].keys())):
                    print(f"{choice} - {i}")
                response = input(f"{symptom_category[qtype]['question']} - (0-{len(symptom_category[qtype]['choices']) - 1}):")
                
                # update user chosen
                for i in range(len(symptom_category[qtype]["choices"])):
                    if response == i:
                        user_chosen_symptom.append(list(symptom_category[qtype]["choices"])[i])
                        break
            elif qtype in SYMPTOM_RELATED:
                for symptom in symptom_category[qtype]:
                    response = self.asking_symptom(symptom,mode="next")
                    if response == 'Y':
                        user_chosen_symptom.append(symptom)
                    asked_symptom.append(symptom)

        return user_chosen_symptom , asked_symptom