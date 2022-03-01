import pandas as pd
import numpy as np

from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from tqdm import tqdm
from scipy import spatial
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import torch
import torch.nn.functional as F
import phonlp

from sentence_transformers import SentenceTransformer

W2V_PATH = '../data/w2v/word2vec_vi_syllables_100dims.txt'
W2V_DIM = 100
THRESHOLD_W2V = 0.9
THRESHOLD_BERT = 0.8
model = KeyedVectors.load_word2vec_format(W2V_PATH)
bert_model = SentenceTransformer('vinai/phobert-base')
phonlp_model = phonlp.load(save_dir='./pretrained_phonlp')

def get_verb_term(noun:str) -> str:
    verb_terms = ''

    noun = noun.lower()

    result = phonlp_model.annotate(text=noun)

    result = result[1][0] # list    
    result = [item[0] for item in result]

    if result[0] in ['V']:
        verb_terms = noun.split(' ')[:1]
    if result[0]=='A':
        cnt = 1
        while cnt < len(result) and result[cnt] == 'N':
            cnt +=1
        
        if cnt != 0:
            verb_terms = noun.split(' ')[:cnt]
    
    return ' '.join(verb_terms)

def get_sentence_presentation(name,method='w2v'):
    ''' Return a list (d-dimention) represent given name
    '''
    assert method in ['w2v','bert']

    presentation_vector = []
    
    if method == 'w2v':
        for token in name.strip().lower().split(' '):
            try:
                w = model.wv[token] # (100,) np.ndarray
            except:
                w = np.ones(W2V_DIM) # not exists
            presentation_vector.append(w)

        result = [sum(sub_list) / len(sub_list) for sub_list in zip(*presentation_vector)]
    elif method == 'bert':
        result = bert_model.encode(name) # (768,)
    
    return result

def get_cosine_similarity(d1,d2):
    result = 1 - spatial.distance.cosine(d1, d2)
    return result

def is_included(str1:str,str2:str) -> bool:
    str1 = str1.lower()
    str2 = str2.lower()
    a = str1.split(' ')
    b = str2.split(' ')
    return bool(set(a) & set(b))

def get_same_category_symptoms(symptom_index:int, data:np.ndarray,method='w2v') -> List:
    ''' Get same category symptoms
    '''    
    if method == 'w2v':
        threshold = THRESHOLD_W2V
    else:
        threshold = THRESHOLD_BERT

    v = data[symptom_index] # vector
    v = np.tile(v,(len(data),1))
    
    cosine_score = F.cosine_similarity(torch.from_numpy(v),torch.from_numpy(data))
    # get index by top-score
    index = (cosine_score>=threshold).nonzero()
    index = [item[0] for item in index.tolist()]

    # from index to symptom name
    result = [SYMPTOM_NAMES[item] for item in index]

    # verb term
    # n_verb = get_verb_term(SYMPTOM_NAMES[symptom_index])

    for i, n in enumerate(SYMPTOM_NAMES):
        v = data[symptom_index] # vector
        v_ = data[i]
        v = np.expand_dims(v,axis=0)
        v_ = np.expand_dims(v_,axis=0)
        
        cosine = F.cosine_similarity(torch.from_numpy(v),torch.from_numpy(v_))
        cosine = cosine.numpy()[0]

        # candidate_verb = get_verb_term(n)

        # if n_verb != '' and candidate_verb != '' and is_included(candidate_verb,n_verb) and cosine >= 0.8:
        if is_included(SYMPTOM_NAMES[symptom_index],n) and cosine >= 0.8:
            if n not in result:
                result.append(n)

    return result

SYMPTOMS = pd.read_csv('../data/symptoms.csv')
SYMPTOM_NAMES = SYMPTOMS['name'].tolist()
SYMPTOM_ID = SYMPTOMS['id'].tolist()

EMBEDDED_DATA_W2V = []
EMBEDDED_DATA_BERT = []
for name in tqdm(SYMPTOM_NAMES):
    w = get_sentence_presentation(name,method='w2v')
    EMBEDDED_DATA_W2V.append(w) # (n,100)
    w = get_sentence_presentation(name,method='bert')
    EMBEDDED_DATA_BERT.append(w) # (n,100)

EMBEDDED_DATA_W2V = np.array(EMBEDDED_DATA_W2V)
EMBEDDED_DATA_BERT = np.array(EMBEDDED_DATA_BERT)

SYMPTOM_CATEGORY_DATA_W2V = []
SYMPTOM_CATEGORY_DATA_BERT = []

for index, name in tqdm(enumerate(SYMPTOM_NAMES)):
    # get same category symptoms 
    related_symptoms_w2v = get_same_category_symptoms(index,EMBEDDED_DATA_W2V,method='w2v')
    # related_symptoms_bert = get_same_category_symptoms(index,EMBEDDED_DATA_BERT,method='bert')
    
    SYMPTOM_CATEGORY_DATA_W2V.append(related_symptoms_w2v)
    # SYMPTOM_CATEGORY_DATA_BERT.append(related_symptoms_bert)

SYMPTOMS['related_symptom_w2v'] = SYMPTOM_CATEGORY_DATA_W2V
# SYMPTOMS['related_symptom_bert'] = SYMPTOM_CATEGORY_DATA_BERT
SYMPTOMS.to_csv("../data/symptoms_updated.csv", index=False)


