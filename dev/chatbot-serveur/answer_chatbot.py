## 5- Interagir avec le chatbot

import sys

path = "/home/juliette/"
path = "/Users/juliettedebono/"
path += "pro3600-mon-test/dev/chatbot-serveur/"

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model(path+'chatbot_model.h5')
import json
import random

intents = json.loads(open(path+'intents.json').read())
words = pickle.load(open(path+'words.pkl','rb'))
classes = pickle.load(open(path+'classes.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for words that exist in sentence

def bag_of_words(sentence, words, show_details=True):
    """Renvoie si le mot exact a été trouvé"""
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    """Renvoie la classe dans laquelle on se trouve"""
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0] # donne la probabilité d'être dans chaque classe
    ERROR_THRESHOLD = 0.25 # Taux d'erreur au dela duquel il faut être pour être valide
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True) # Ordonner dans l'ordre des plus fortes probabilités
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])}) # Ajouter le nom des classes
    return return_list

def getResponse(ints, intents_json):
    """Renvoie la réponse à partir des possibilités de réponse"""
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return tag, result

def send(msg):
    """Répond au message"""
    if msg != '':
        ints = predict_class(msg) # Récupère les réponses possibles
        return getResponse(ints, intents) # Renvoie la réponse et la catégorie
    return "Error"