from flask import Flask, jsonify, request
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
import json
import sys
import pickle
import traceback
import numpy as np

app = Flask(__name__)

model_directory = 'model'
model_file_name = '%s/my_model.h5' % model_directory
tokenizer_file_name = '%s/tokenizer.pickle' % model_directory

model = keras.models.load_model(model_file_name)

with open(tokenizer_file_name, 'rb') as handle:
                tokenizer = pickle.load(handle)

@app.route('/<int:valor1>,<int:valor2>')
def dummy_api(valor1:int, valor2:int):
    return jsonify(date="suma "+str(valor1+valor2))
	
@app.route('/predict', methods=['POST'])
def predict_api():
   
    try:
        json_ = request.json
        if json_ == None:
            return 'Got None'
        else:
            sequence_predict = pad_sequences(tokenizer.texts_to_sequences([json_["texto"]]), maxlen=116)
            y_predict = model.predict(sequence_predict)
            result = np.argmax(y_predict,axis=1)[0]
            print(result)
            return jsonify(resultado = int(result))
    
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})
   
#@app.before_first_request
#def _run_on_start(a_string):
#    print ("doing something important with %s" % a_string)
    
def load_model():
    try:
        model = keras.models.load_model(model_file_name)
        print('model loaded')

    except Exception as e:
        print('No model here')
        print(str(e))
        model = None

if __name__ == '__main__':
    app.run()