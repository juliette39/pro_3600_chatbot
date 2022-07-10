## 1- Importer des bibliothèques et charger les données
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

path = "/home/juliette/"
path = "/Users/juliettedebono/"
path += "pro3600-mon-test/dev/chatbot-serveur/"

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Chargement données JSON
intents_file = open(path+'intents.json').read()
intents = json.loads(intents_file)

## 2- Prétraiter les données

# Diviser la phrase en mots
words=[]
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.']
for intent in intents['intents']:
    for pattern in intent['patterns']:

        word = nltk.word_tokenize(pattern) # Divise la phrase en mots
        words.extend(word) # Ajout des mots dans le tableau de tous les mots
        documents.append((word, intent['tag'])) # Ajout des mots dans le tableau de tous les mots avec classes associées

        if intent['tag'] not in classes:
            classes.append(intent['tag']) # Ajout de la classe dans la liste (si pas déjà présente)

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters] # Récupération des lemmes des mots en minuscule
words = sorted(list(set(words))) # Ordonne en supprimant les doublons
# Ordonner les classes
classes = sorted(list(set(classes)))
# documents = combination entre les lemmes des mots des phrases et les classes associées
print (len(documents), "documents")
# classes = intents
print (len(classes), "classes", classes)
# words = tous les mots possibles (lemmes)
print (len(words), "unique lemmatized words", words)

pickle.dump(words,open(path+'words.pkl','wb')) # Écriture des lemmes dans un fichier
pickle.dump(classes,open(path+'classes.pkl','wb')) # Écriture des classes dans un fichier

## 3- Créer des données de formation et de test

training = [] # Créer les données d'entrainement

output_empty = [0] * len(classes) # Créer tableau vide pour la sortie
# training set, bag of words for every sentence
for doc in documents:
    bag = [] # Initialisation

    word_patterns = doc[0] # Liste des mots divisés

    # On récupère le lemme de chaque mot : création d'une base de mots pour représenter les mots apparentés
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

    # On crée un tableau avec 1 si le mot se trouve dans les lemmes des mots possibles
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # On sort 0 pour tout les tags sauf celui dans lequel on se trouve
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training) # On mélange aléatoirement le tableau
training = np.array(training, dtype=object) # On converti le tableau en un tableau numpy
# create training and testing lists. X - patterns, Y - intents
# Création les listes d'entrainement et de test
train_x = list(training[:,0]) # Modèle -> 1 si lemme possible
train_y = list(training[:,1]) # Classe -> 1 pour la classe
print("Training data is created")

## 4- Former le modèle

# Modele de réseau de neurones profonds
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Modèle de compilation. SGD avec Nesterov accéléré gradient donne de bons résultats pour ce modèle
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entrainement et sauvegarde du modèle
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save(path+'chatbot_model.h5', hist)
print("model is created")