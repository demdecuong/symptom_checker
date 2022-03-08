from src.inference_engine import InferenceEngine

if '__name__' == '__main__':
    infengine = InferenceEngine()

    init_symptom = 'sổ mũi'

    related_symptoms = infengine.get_relevant_symptoms(
        given_symptom=init_symptom,
        method='fuzzy',
        threshold=80
    )

    print(related_symptoms)