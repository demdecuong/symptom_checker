import pandas as pd
from tqdm import tqdm

data = pd.read_csv('../data/symptoms_category.csv')

related_symptoms = data['related_symptom_w2v'].tolist()

data['category'] = [-1] * len(related_symptoms)

category_index = -1
is_assign = False
for symptom_list in tqdm(related_symptoms):
    symptom_list = symptom_list.strip('][').replace('"','').replace("'","").split(', ')

    for name in symptom_list:
        val = data.loc[data['name']==name,'category']

        try:
            if val.item() == -1:
                data.loc[data['name']==name,'category'] = category_index
                is_assign = True
        except:
            continue
    
    if is_assign:
        category_index += 1
        is_assign = False

data.to_csv('../data/symptoms_category.csv')

print(category_index)

# Create category.json for question
