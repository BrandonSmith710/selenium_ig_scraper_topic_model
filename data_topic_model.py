!python -m spacy download en_core_web_md

!pip install pyLDAvis==3.3.1

from google.colab import files
import io
import pandas as pd

# Commented out IPython magic to ensure Python compatibility.
import bs4
import requests
from google.colab import files
import io
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import spacy, en_core_web_md

import pyLDAvis
import pyLDAvis.gensim_models 

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# %matplotlib inline

import warnings
warnings.filterwarnings("ignore")

up = files.upload()

df = pd.read_csv(io.BytesIO(up['brandon_ig_scrape2.csv']), encoding='latin1')

nlp = spacy.load('en_core_web_md')



def cleaner(text):

  text = text.replace('\n', ' ')
  text = re.sub('[^a-z A-Z0-9]', '', text)

  text = re.sub('[ ]{2, }', ' ', text)

  return text.lower().strip()

def tokenizer(text):

  lemmas = []

  for c in nlp(text):

    if not sum([c.is_space, c.is_stop, c.is_punct]):

      lemmas += [c.lemma_]

  return lemmas


df_good = df.copy()
df_good = df_good[df_good['likes'] != '1 like']

df_good['caption'] = df_good['caption'].apply(cleaner)

df_good.head()

df_good['lemmas'] = df_good['caption'].apply(tokenizer)

df_good.head()

id2word = corpora.Dictionary(df_good['lemmas'])

corpus = [id2word.doc2bow(x) for x in df_good['lemmas']]

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics
    Parameters:
    ----------
    dictionary : Gensim dictionary ex. corpora.Dictionary(df_good['lemmas']) i.e. id2word
    corpus : Gensim corpus i.e. [id2word.doc2bow(doc) for doc in df_good['lemmas']]
    texts : List of input texts  ex. df_good['lemmas']
    limit : Max num of topics
    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.ldamulticore.LdaMulticore(corpus=corpus,
                                                        id2word=id2word,
                                                        num_topics=num_topics, 
                                                        chunksize=100,   # number of docs used in each training chunk
                                                        passes=10,
                                                        random_state=1234,
                                                        per_word_topics=True,
                                                        workers=2)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

model_list, coherence_values = compute_coherence_values(id2word, corpus, df['lemmas'], 16, step=2)

best = np.argmax(coherence_values)

lda_trained_model = model_list[best]

pyLDAvis.enable_notebook()

vis = pyLDAvis.gensim_models.prepare(lda_trained_model, corpus, id2word)

vis
