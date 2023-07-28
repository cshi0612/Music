import pickle
import nltk

import ssl

try: 
  _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
  pass
else:
  ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
import pandas as pd
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re, collections
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import mean_squared_error, r2_score, cohen_kappa_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor

from nltk.tokenize import word_tokenize
import string
from sklearn.metrics import classification_report
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler

# average word length for text
def avg_word_len(text):
  clean_essay = re.sub(r'\W', ' ', text)
  words = nltk.word_tokenize(clean_essay)
  total = 0
  for word in words:
    total += len(word)
  average = total / len(words)

  return average


# word count in a given text
def word_count(text):
  clean_essay = re.sub(r'\W', ' ', text)
  return len(nltk.word_tokenize(clean_essay))


# char count in given text
def char_count(text):
  return len(re.sub(r'\s', '', str(text).lower()))


# sentence count in a given text
def sent_count(text):
  return len(nltk.sent_tokenize(text))


# tokenization of texts to sentences
def sent_tokenize(text):
  stripped_essay = text.strip()

  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  raw_sentences = tokenizer.tokenize(stripped_essay)

  tokenized_sentences = []
  for raw_sentence in raw_sentences:
    if len(raw_sentence) > 0:
      clean_sentence = re.sub("[^a-zA-Z0-9]", " ", raw_sentence)
      tokens = nltk.word_tokenize(clean_sentence)
      tokenized_sentences.append(tokens)
  return tokenized_sentences


# lemma, noun, adjective, verb, adverb, count for given text
def count_lemmas(text):
  noun_count = 0
  adj_count = 0
  verb_count = 0
  adv_count = 0
  lemmas = []
  lemmatizer = WordNetLemmatizer()
  tokenized_sentences = sent_tokenize(text)

  for sentence in tokenized_sentences:
    tagged_tokens = nltk.pos_tag(sentence)

    for token_tuple in tagged_tokens:
      pos_tag = token_tuple[1]

      if pos_tag.startswith('N'):
        noun_count += 1
        pos = wordnet.NOUN
        lemmas.append(lemmatizer.lemmatize(token_tuple[0], pos))
      elif pos_tag.startswith('J'):
        adj_count += 1
        pos = wordnet.ADJ
        lemmas.append(lemmatizer.lemmatize(token_tuple[0], pos))
      elif pos_tag.startswith('V'):
        verb_count += 1
        pos = wordnet.VERB
        lemmas.append(lemmatizer.lemmatize(token_tuple[0], pos))
      elif pos_tag.startswith('R'):
        adv_count += 1
        pos = wordnet.ADV
        lemmas.append(lemmatizer.lemmatize(token_tuple[0], pos))
      else:
        pos = wordnet.NOUN
        lemmas.append(lemmatizer.lemmatize(token_tuple[0], pos))
  lemma_count = len(set(lemmas))
  return noun_count, adj_count, verb_count, adv_count, lemma_count


def create_features(texts):
    data = pd.DataFrame(columns=(
        'Average_Word_Length', 'Sentence_Count', 'Word_Count',
        'Character_Count', 'Noun_Count', 'Adjective_Count',
        'Verb_Count', 'Adverb_Count', 'Lemma_Count'
    ))

    data['Average_Word_Length'] = texts.apply(avg_word_len)
    data['Sentence_Count'] = texts.apply(sent_count)
    data['Word_Count'] = texts.apply(word_count)
    data['Character_Count'] = texts.apply(char_count)
    temp = texts.apply(count_lemmas)
    noun_count, adj_count, verb_count, adverb_count, lemma_count = zip(*temp)
    data['Noun_Count'] = noun_count
    data['Adjective_Count'] = adj_count
    data['Verb_Count'] = verb_count
    data['Adverb_Count'] = adverb_count
    data['Lemma_Count'] = lemma_count
    return data


def load_model(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model


clf = load_model('grade_writing.sav')
labels = ['bad', 'average', 'good']


context = """The nation is days away from defaulting on its obligations. The Republican House speaker, pushed by conservatives in his party, demands deep spending cuts. The president, a Democrat, works on negotiating a package to avert a fiscal calamity.

No, it's not 2023.

It's 2011, when then-President Barack Obama agreed to a debt ceiling deal with then-House Speaker John Boehner that called for more than $900 billion in upfront spending cuts and deficit reduction, as well as the creation of a joint congressional committee that would find at least $1.2 trillion in additional belt tightening.
The situation is similar to the one President Joe Biden, who served as Obama's vice president, is facing today. He and House Speaker Kevin McCarthy, a Republican, are pushing their parties to swiftly approve their agreement to address the current debt limit drama before the US could start missing payments on June 5.

Today's House Republicans may want to look back at the results of their predecessors' hard-fought deal. Things didn't proceed as planned, and a chunk of the reductions was ultimately pared back through a subsequent series of bipartisan bills.

"Once Congress took a look at the programs and what was required, they realized they couldn't make cuts that deep," said Brian Riedl, a senior fellow at the right-leaning Manhattan Institute who was involved in the 2011 negotiations.
"""


def prediction(context):
    mydata = {'essay': [context]}
    df_context = pd.DataFrame(data = mydata)

    df_context = create_features(df_context['essay'])
    pred = clf.predict(df_context)[0]
    print(pred, labels[pred])
    return labels[pred]


prediction(context)