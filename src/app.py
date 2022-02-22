''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

from src.service import Service
from src.constants import (
    GREETING,
    NAME_INPUT,
    SEX_INPUT,
    AGE_INPUT,
    FIRST_SYMPTOM_INPUT,
    OTHER_SYMPTOM_INPUT
)
from src.utils import display
from string import Template

class Application:
    def __init__(self):
        self.service = Service()

        self.current_response = {
            "symptom" : [],
            "triage": "",
            "possible_disease":[],
        }
        self.personal_info = {
            "name": "",
            "sex" : "",
            "age" : ""
        }

    def run(self):
        # clear history
        self.clear_history()

        # personal info
        self.greeting()
        self.get_personal_info()

        # first symptom
        self.get_user_symptom(first=True)

    def get_user_symptom(self,relevant_symptoms:list=[],first:bool=False) -> dict:
        '''
        Args:
            - first (bool): This is the first symptom from user 
            - relevant_symptoms (list) : relevant symptoms if given symptom is not 
        '''
        user_symptoms = []

        if first:
            symptom = input(FIRST_SYMPTOM_INPUT)
        else:
            symptom = input(OTHER_SYMPTOM_INPUT) 

        '''There are 3 situations for user's symptom:
        1. not included in the current database
        2. included with high fuzzy score
        3. included

        - For 1: ask another one
        - For 2: ask to verify final symptom -> 3
        - For 3; ask relevant symptoms
        '''
        # if symptom not in self.service.knowledge_base.symptoms

        # get relevant symptom

    
        self.update_current_response(
            symptom=symptom
        )

    def update_current_response(self,symptom:str="") -> None:
        ''' Update self.current_response
        '''
        self.update_symptom(symptom)
        self.update_possible_disease(symptom)
        self.update_triage(symptom,possible_disease)

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
        }

        self.personal_info = {
            "name": "",
            "sex" : "",
            "age" : ""
        }