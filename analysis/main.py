''' 
Author: Nguyen Phuc Minh
Lastest update: 22/2/2022
'''

import pandas as pd
import matplotlib.pylab as plt

from collections import Counter
from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def from_symptom_id_to_name(id):
    symptom_name = symptoms.loc[symptoms['id'] == id]
    return symptom_name['name'].item()

def from_disease_id_to_name(id):
    disease_name = disease.loc[disease['id'] == id]
    return disease_name['name'].item()

def from_symptom_to_id(name):
    id = symptoms.loc[symptoms['name'] == name]
    return id['id'].item()

def plot_freq(data, N=30):
    plot_data = {k: v for k, v in sorted(data.items(), reverse=True, key=lambda item: item[1])[:N]}
    names = list(plot_data .keys())
    values = list(plot_data .values())
    plt.rcParams['font.size'] = '4'
    plt.xticks(rotation='vertical')
    plt.bar(range(len(plot_data )), values, tick_label=names)
    plt.ylabel("Frequency")
    plt.xlabel("Disease")
    plt.suptitle(f"Top N have highest frequency")
    plt.show()

disease = pd.read_csv('../data/diseases.csv')
symptoms = pd.read_csv('../data/symptoms.csv')
disease_symptom = pd.read_csv('../data/diseases_has_symptoms.csv')

# count freq of symptom
symptom_freq = {}
for id in disease_symptom['symptom_id']:
    if id not in symptom_freq:
        symptom_freq[id] = 1
    else:
        symptom_freq[id] += 1 
name_symptom_freq = {}
for k,v in symptom_freq.items():
    name_symptom_freq[from_symptom_id_to_name(k)] = v

symptom_freq = pd.DataFrame.from_dict(name_symptom_freq,orient='index', columns=['mention'])
print(symptom_freq.describe())

print(symptom_freq.head(3))


# plot common 
N = 30
plot_freq(name_symptom_freq,N)

# given N symptoms, which diseases ?
M = 20
plot_name_symptom_freq= {k: v for k, v in sorted(name_symptom_freq.items(), reverse=True, key=lambda item: item[1])[:N]}
common_disease = {}
common_symptoms = list(plot_name_symptom_freq.keys())
for s in common_symptoms:
    symptom_id = from_symptom_to_id(s)
    relevant_disease = disease_symptom.loc[disease_symptom['symptom_id'] == symptom_id]
    relevant_disease = relevant_disease['disease_id'].values
    relevant_disease = [from_disease_id_to_name(item) for item in relevant_disease]
    for d in relevant_disease:
        if d not in common_disease:
            common_disease[d] = 1
        else: 
            common_disease[d] += 1
print(len(common_disease))
plot_freq(common_disease,M)
print(list(common_disease.keys())[:M])