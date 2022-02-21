from src.inference_engine import InferenceEngine
from src.knowledge_base import KnowledgeBase

class Service:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.inference_engine = InferenceEngine()
    
            