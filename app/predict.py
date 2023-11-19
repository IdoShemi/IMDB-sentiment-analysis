import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
import tensorflow_hub as hub
MODEL_PATH = 'IMDB_model.h5'

# Load the saved model
model = load_model(MODEL_PATH, custom_objects={'KerasLayer':hub.KerasLayer})

# Load the tokenizer
# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)


def predict_sentiments(text_list):
    predictions = np.argmax(model.predict(text_list), axis=1)
    sentiments = []
    for prediction in predictions:
        if prediction == 0:
            sentiments.append("Negative")
        else:
            sentiments.append("Positive")
    return sentiments
