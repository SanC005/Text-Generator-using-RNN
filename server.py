from flask import Flask, jsonify,request,render_template
from keras.models import load_model
import numpy as np
import random

app = Flask(__name__)

model = load_model('model.hdf5')

with open('sherlock-holmes.txt', 'r') as file:
    text = file.read().lower()
#print('text length', len(text))
chars = sorted(list(set(text)))
#print('total chars: ', len(chars))

# %%
bad_chars = [';','½','£', 'à', 'â', 'è', 'é']
for i in range(len(bad_chars)):
  text = text.replace(bad_chars[i],"")
chars = sorted(list(set(text)))
textlen = len(text)
charlen = len(chars)
#print("length is " + str(textlen))
#print("length is " + str(charlen))
#print(chars)

# %%
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))
#print(chars)

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

@app.route('/')
def entry():
    response = jsonify({"data" : "hello "});

    response.headers.add('Access-Control-Allow-Origin', '*')
    return render_template('index.html')
    


@app.route('/generate',methods=["GET","POST"])
def generate_text():

    query = request.json['query'].lower()
    maxlen = 40
    length = 200
    temperature = 0.3
    generated = ''
    # sentence = text[start_index: start_index + maxlen]
    sentence = query
    flag=0
    # random_string = 'quick eye took in my occupation'
    if(len(sentence)<40):
        temperature= min(0.8,0.2 + 10/(len(sentence)+1))
        flag=1
    print("temperature is ",temperature)
    for i in range(len(sentence),40):
        sentence+=" "
    if(len(sentence)>40):
        sentence = sentence[:40]
    print(len(sentence),"this is sentence length")
    if(flag==0):
        generated += sentence
   # maxlen = len(query)


    for i in range(length):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

    response = jsonify({"data" : generated});

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)