### Symptom Mapper
```
from src.inference_engine import InferenceEngine

if __name__ == '__main__':
    infengine = InferenceEngine(
        init_weight_method='default'
    )

    init_symptom = 'sổ mũi'

    related_symptoms = infengine.get_relevant_symptoms(
        given_symptom=init_symptom,
        method='fuzzy',
        threshold=80
    )
```
Output will be like this:
```
['Nghẹt mũi', 'Chảy nước mũi', 'Viêm mũi xuất tiết', 'Sổ mũi', 'Dịch mũi vàng', 'Mũi xẹp xuống']
```

### Inference Engine
KnowledgeBase is inside Inference Engine
```
class KnowledgeBase:
    def __init__(self,
                init_weight_method:str="random",
                do_filter_symptom:bool=False, 
                do_filter_disease:bool=False,
                topk_symptom:int=30,
                topk_disease:int=120) -> None:
        '''
        Args:
            - init_weight_method (str)
            - do_filter_symptom (bool): filter to topk symptoms and its relevant disease
            - topk_symptom (int) : top common symptoms
            - do_filter_disease (bool): filter to topk disease and its relevant disease
            - topk_disease (int) : top common disease
        '''
```