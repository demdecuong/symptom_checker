''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

from src.inference_engine import InferenceEngine
from src.knowledge_base import KnowledgeBase
from src.nlp import NLP

class Service:
    ''' A wrapper class handle KnowledgeBase and InferenceEngine
    '''
    def __init__(self,init_weight_method:str='random',do_filter:bool=False, topk:int=30) -> None:
        self.knowledge_base = KnowledgeBase(
            init_weight_method=init_weight_method,
            do_filter=do_filter,
            topk=topk
        )
        
        self.inference_engine = InferenceEngine()

        self.nlp = NLP()

    