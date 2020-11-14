## This script create the tokenizers used by the model. One fitted for group selection and one for each group used to
## predict the segments in each group. And also, creates sequences_arrays and target arrays to 

import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle

from tensorflow.keras.preprocessing.sequence import pad_sequences


def words_per_row(X):
    pattern = r"[^\w]"
    X_words =  X.apply(lambda x : len(x))

    return X_words


print('enter segment')

segment = input()
segment = segment.upper()


if segment not in ['GROUPS','B','C','D','E','F']:
    raise Exception(segment, ' is not a valid segment')


#
# secop_word_processed is a data set that contains all descripcion de processo pre processed and extracted columns
# for group code and segment code, the last 2 are the targets of the models
df = pd.read_csv('data/secop_word_processed.csv',
                 usecols=['descripcion_del_proceso_prueba','codigo_grupo', 'codigo_segmento'])
#
if segment != 'GROUPS':
    df = df[df['codigo_grupo'] == segment]

    replace_dict = {'B':{'11':0,
                          '12':1,
                          '13':2,
                          '14':3,
                          '15':4},
                     'C':{'20':0,
                          '21':1,
                          '22':2,
                          '23':3,
                          '24':4,
                          '25':5,
                          '26':6,
                          '27':7},
                     'D':{'30':0,
                        '31':1,
                        '32':2,
                        '39':3,
                        '40':4,
                        '41':5},
                     'E':{'42':0,
                        '43':1,
                        '44':2,
                        '45':3,
                        '46':4,
                        '47':5,
                        '48':6,
                        '49':7,
                        '50':8,
                        '51':9,
                        '52':10,
                        '53':11,
                        '54':12,
                        '55':13,
                        '56':14,
                        '60':15},
                     'F':{'70':0,
                          '71':1,
                          '72':2,
                          '73':3,
                          '76':4,
                          '77':5,
                          '78':6,
                          '80':7,
                          '81':8,
                          '82':9,
                          '83':10,
                          '84':11,
                          '85':12,
                          '86':13,
                          '90':14,
                          '91':15,
                          '92':16,
                          '93':17,
                          '94':18}}
    df['target'] = df['codigo_segmento'].astype(str).replace(replace_dict[segment])
else:
    replace_dict = {'GROUPS':{'A':0,
                                'B':1,
                                'C':2,
                                'D':3,
                                'E':4,
                                'F':5,
                                'G':6,}}

    df['target'] = df['codigo_grupo'].astype(str).replace(replace_dict[segment])



df_modelo = df[['descripcion_del_proceso_prueba', 'target']]

#
#
X = df_modelo['descripcion_del_proceso_prueba'].astype(str)
y = df_modelo['target']
#
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_counted = words_per_row(X_train).to_frame().rename(columns={"Text": "cant_words"})

pad_words = math.ceil(X_train_counted.quantile(.95))

#
# # Instanciamos un tokenizador de keras con 20000 palabras
tokenizer = Tokenizer(num_words=120000)
tokenizer.fit_on_texts(X_train)
with open('data/tokenizer_{}.pickle'.format(segment), 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

X_train_seq = tokenizer.texts_to_sequences(X_train)
train_sequences = pad_sequences(X_train_seq, maxlen=pad_words)

X_test_seq = tokenizer.texts_to_sequences(X_test)
test_sequences = pad_sequences(X_test_seq, maxlen=pad_words)

np.save('data/train_sequences_{}.npy'.format(segment), train_sequences)
np.save('data/test_sequences_{}.npy'.format(segment), test_sequences)
y_train.to_csv('data/y_train_{}.csv'.format(segment), index=False)
y_test.to_csv('data/y_test_{}.csv'.format(segment), index=False)