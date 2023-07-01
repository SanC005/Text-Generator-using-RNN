# %%
import numpy as np
from keras.models import Sequential,load_model
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import random

# %%
with open('/home/spswsl/rnn/rnnenv/code/Text-Generator-using-RNN/content/sherlock-holmes.txt', 'r') as file:
    text = file.read().lower()
print('text length', len(text))
chars = sorted(list(set(text)))
print('total chars: ', len(chars))

# %%
bad_chars = [';','½','£', 'à', 'â', 'è', 'é']
for i in range(len(bad_chars)):
  text = text.replace(bad_chars[i],"")
chars = sorted(list(set(text)))
textlen = len(text)
charlen = len(chars)
print("length is " + str(textlen))
print("length is " + str(charlen))
print(chars)

# %%
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))
print(chars)

# %%
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

x = np.zeros((len(sentences), maxlen, len(chars)), dtype=bool)
y = np.zeros((len(sentences), len(chars)), dtype=bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# %%
#Model building
#model = Sequential()
model = load_model('weights20.hdf5')
# model.add(LSTM(256, input_shape=(maxlen, len(chars))))
# model.add(Dense(len(chars)))
# model.add(Activation('softmax'))

# # %%
# model.compile(loss='categorical_crossentropy',optimizer='adam')

# # %%
# import random
def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

# # %%
# # Setting Checkpoints
# filepath = "weights20.hdf5"
# checkpoint = ModelCheckpoint(filepath, monitor='loss',
#                              verbose=1, save_best_only=True,
#                              mode='min')

# # %%
# from tensorflow.keras.callbacks import ReduceLROnPlateau
# reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2,
#                               patience=1, min_lr=0.001)

# callbacks = [checkpoint, reduce_lr]

# # %%
# model.fit(x, y, batch_size=128, epochs=20, callbacks=callbacks)

# %%
def generate_text(length, diversity):
    # Function to get random starting text and generate text for it
    start_index = random.randint(0, len(text) - maxlen - 1)
    print("start index shit here #########################")
    print(start_index,text[start_index] )
    generated = ''
    # sentence = text[start_index: start_index + maxlen]
    sentence = "r 22nd. twenty-four geese at 7s. 6d.'"
    for i in range(len(sentence),40):
        sentence+=" "
    print(len(sentence),"this is sentence length")
    generated += sentence
    print('THIS IS INPUT ')

    print(".********************************************************")
    print(generated)
    for i in range(length):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char
    return generated

# %%
print(generate_text(500, 0.3))


