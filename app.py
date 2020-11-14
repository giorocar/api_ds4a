## Script that predicts 3 out of 7 possible class predictions and 3 segments per predicted class out of 56 possible
## segments

from flask import Flask, jsonify, request
from tensorflow.keras.preprocessing.sequence import pad_sequences
from collections import OrderedDict
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
from unidecode import unidecode
from tensorflow.keras.models import load_model
from numpy import load
import pickle5 as pickle
import traceback
import re
import sys

sys.path.append('data/')
from diccionario_group_seg import *  ##Dict for translating between group and segment numerical values to their actual

## text meaning


app = Flask(__name__)

## We make use of 6 different tokenizers, one for each step on classification. Next uploads tokenizers
with open('tokenizers/tokenizer_group.pickle', 'rb') as handle:
    tokenizer_group = pickle.load(handle)

with open('tokenizers/tokenizer_B.pickle', 'rb') as handle:
    tokenizer_b = pickle.load(handle)

with open('tokenizers/tokenizer_C.pickle', 'rb') as handle:
    tokenizer_c = pickle.load(handle)

with open('tokenizers/tokenizer_D.pickle', 'rb') as handle:
    tokenizer_d = pickle.load(handle)

with open('tokenizers/tokenizer_E.pickle', 'rb') as handle:
    tokenizer_e = pickle.load(handle)

with open('tokenizers/tokenizer_F.pickle', 'rb') as handle:
    tokenizer_f = pickle.load(handle)

ciudad = load('ciudad.npy')  # Stopwords array for complementing stopwords

# As with tokenizers we use 6 different models, one for each step
model_group = load_model('models_h5/group_weights.h5')
model_b = load_model('models_h5/group_B.h5')
model_c = load_model('models_h5/group_C.h5')
model_d = load_model('models_h5/group_D.h5')
model_e = load_model('models_h5/group_E.h5')
model_f = load_model('models_h5/group_F.h5')

## Creation of stopwords array
stopwords = unidecode(' '.join(stopwords.words("spanish")))
stopwords = stopwords.split()
stopwords = stopwords + ['y'] + ['o'] + ['s'] + ['b'] + ['c'] + ['i']
otras = ['s', 'asi', 'demas', 'p', 'x', 'ndeg', 'c', 'n', 'i', 'd', 'm', 'ii', 'pic', 'th', 'b', 'iv', 'np', 'ebi', 'u',
         'ml', 'l']

stopwords = stopwords + otras

stopwords = stopwords + list(ciudad)

pattern_1 = r"[^\w]"
pattern_2 = r"[^a-z ]"

token = 'group'

# Dictionary containing tokenizer, padding lenght and model for each step of preddiction
seq_lengh = {'group': [tokenizer_group, 214, model_group],
             1: [tokenizer_b, 242, model_b],
             2: [tokenizer_c, 247, model_c],
             3: [tokenizer_d, 259, model_d],
             4: [tokenizer_e, 232, model_e],
             5: [tokenizer_f, 351, model_f]}

## Dict for translating Neural network model output to segment number
seg_a = {0: '00'}
seg_b = {0: '11', 1: '12', 2: '13', 3: '14', 4: '15'}
seg_c = {0: '20', 1: '21', 2: '22', 3: '23', 4: '24', 5: '25', 6: '26', 7: '27'}
seg_d = {0: '30', 1: '31', 2: '32', 3: '39', 4: '40', 5: '41'}
seg_e = {0: '42', 1: '43', 2: '44', 3: '45', 4: '46', 5: '47', 6: '48', 7: '49', 8: '50', 9: '51', 10: '52', 11: '53',
         12: '54', 13: '55', 14: '56', 15: '60'}
seg_f = {0: '70', 1: '71', 2: '72', 3: '73', 4: '76', 5: '77', 6: '78', 7: '80', 8: '81', 9: '82', 10: '83', 11: '84',
         12: '85', 13: '86', 14: '90', 15: '91', 16: '92', 17: '93', 18: '94'}
seg_g = {0: '00'}

group_translate = {0: ['A', seg_a],
                   1: ['B', seg_b],
                   2: ['C', seg_c],
                   3: ['D', seg_d],
                   4: ['E', seg_e],
                   5: ['F', seg_f],
                   6: ['G', seg_a]}


def clean_text(text):
    ## Preprocessing of text, unify formats, lower strings, delete stop words
    text = unidecode(text)
    text = text.lower()
    text = re.sub(pattern_1, " ", text)
    text = re.sub(pattern_2, " ", text)
    text = text.replace('xx', '')
    text = ' '.join(word for word in text.split() if word not in stopwords)

    return text


# token means value for seq_lengh dict i.e. each step of modeling
def process_text(text, token):
    ## receives a string and step of modeling for converting the text into a numerical
    #  sequence necesary as model input
    clean = clean_text(text)
    return pad_sequences(seq_lengh[token][0].texts_to_sequences([clean]), maxlen=seq_lengh[token][1])


def get_group_orders(predictions):
    ## ordena mis predicciones de mayor a menor
    sorted_preds = sorted(predictions)[::-1]
    sorted_preds_index = []
    for pred in sorted_preds:
        sorted_preds_index.append(list(predictions).index(pred))
    return sorted_preds_index


@app.route('/predict', methods=['POST'])
def predict_api():
    ## prediction function, receives a text as input an returns most probable 3 clases with 3
    # most propable segments for each predicted clases in a OrderedDict format.
    try:
        json_ = request.get_json()

        text = json_["texto"]
        print(json_)
        if json_ == None:
            message = {
                "message": [
                    "Got None!"
                ]
            }
            response = jsonify(message)
            return response
        else:
            text_sequence = process_text(json_["texto"], 'group')
            if len(set(text_sequence[0])) >= 5:
                preds = seq_lengh['group'][2].predict(text_sequence)[0]
                sorted_preds = get_group_orders(preds)[:3]
                pred_dict = OrderedDict()
                for pred in sorted_preds:
                    if pred == 0:
                        segment = '10'
                        pred_dict[group_translate.get(pred)[0]] = [segment, segment, segment]
                    elif pred == 6:
                        segment = '95'
                        pred_dict[group_translate.get(pred)[0]] = [segment, segment, segment]
                    else:
                        text_sequence = process_text(text, pred)
                        preds = seq_lengh[pred][2].predict(text_sequence)[0]
                        sorted_preds = get_group_orders(preds)[:3]
                        pred_dict[group_translate.get(pred)[0]] = [group_translate.get(pred)[1].get(seg) for seg in
                                                                   sorted_preds]
                result = outputPredict(pred_dict)
            else:
                result = 'No es un texto suficiente para realizar una predicción'

            print(result)
            return jsonify(resultado=result)

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})


def outputPredict(pred_dict):
    grupo_1 = list(pred_dict.items())[0][0]
    segmento_11 = list(pred_dict.items())[0][1][0]
    segmento_12 = list(pred_dict.items())[0][1][1]
    segmento_13 = list(pred_dict.items())[0][1][2]
    grupo_2 = list(pred_dict.items())[1][0]
    segmento_21 = list(pred_dict.items())[1][1][0]
    segmento_22 = list(pred_dict.items())[1][1][1]
    segmento_23 = list(pred_dict.items())[1][1][2]
    grupo_3 = list(pred_dict.items())[2][0]
    segmento_31 = list(pred_dict.items())[2][1][0]
    segmento_32 = list(pred_dict.items())[2][1][1]
    segmento_33 = list(pred_dict.items())[2][1][2]

    result1 = 'Primer grupo sugerido \n' + \
              ''.join(grupo_1) + ': ' + ''.join(diccionario_group_seg[grupo_1][0]) + \
              '\nSegmentos con mayor probabilidad\n' \
              + ''.join(segmento_11) + ': ' + ''.join(diccionario_group_seg[grupo_1][1][int(segmento_11)]) + '\n' \
              + ''.join(segmento_12) + ': ' + ''.join(diccionario_group_seg[grupo_1][1][int(segmento_12)]) + '\n' \
              + ''.join(segmento_13) + ': ' + ''.join(diccionario_group_seg[grupo_1][1][int(segmento_13)])

    result2 = '\n\n\nSegundo grupo sugerido \n' + \
              ''.join(grupo_2) + ': ' + ''.join(diccionario_group_seg[grupo_2][0]) + \
              '\nSegmentos con mayor probabilidad\n' \
              + ''.join(segmento_21) + ': ' + ''.join(diccionario_group_seg[grupo_2][1][int(segmento_21)]) + '\n' \
              + ''.join(segmento_22) + ': ' + ''.join(diccionario_group_seg[grupo_2][1][int(segmento_22)]) + '\n' \
              + ''.join(segmento_23) + ': ' + ''.join(diccionario_group_seg[grupo_2][1][int(segmento_23)])

    result3 = '\n\n\nTercer grupo sugerido \n' + \
              ''.join(grupo_3) + ': ' + ''.join(diccionario_group_seg[grupo_3][0]) \
              + '\nSegmentos con mayor probabilidad\n' \
              + ''.join(segmento_31) + ': ' + ''.join(diccionario_group_seg[grupo_3][1][int(segmento_31)]) + '\n' \
              + ''.join(segmento_32) + ': ' + ''.join(diccionario_group_seg[grupo_3][1][int(segmento_32)]) + '\n' \
              + ''.join(segmento_33) + ': ' + ''.join(diccionario_group_seg[grupo_3][1][int(segmento_33)])

    return result1 + result2 + result3


if __name__ == '__main__':
    app.run()
