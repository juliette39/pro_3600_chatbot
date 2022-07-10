Site web source : https://www.tophebergeur.com/blog/projet-chatbot-python/

pip install tensorflow
pip install keras
pip install nltk
(pip install pickle) # Déjà présent dans python3.9

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

Créer le dossier chatbot
Ajouter ces trois fichiers : train_chatbot.py, main_chatbot.py & intents.json (dans le dossier drive)

Puis lancer dans un terminal : python3 chatbot/train_chatbot.py # Création des fichiers nécessaire pour converser
Pour lancer l'application enfin, lancer chatbot/main_chatbot.py # On peut désormais parler avec le robot

Fichiers :

• train_chatbot.py : Dans ce fichier, nous allons créer et former le modèle de deep learning ou apprentissage profond. Ce dernier va classer et identifier ce que l’utilisateur demande au robot.

• main_Chatbot.py : C’est dans ce fichier que nous allons créer une interface utilisateur pour tchatter avec notre chatbot formé.

• intents.json : Le fichier d’intents contient toutes les données que nous allons utiliser pour former le modèle. Il comprend une collection de balises avec leurs modèles et réponses correspondants.

• chatbot_model.h5 : Il s’agit d’un fichier de format de données hiérarchique dans lequel nous avons sauvegardé les poids et l’architecture de notre modèle formé.

• classes.pkl : Le fichier pickle peut être utilisé pour sauvegarder tous les noms de balises à classer lorsque nous prédisons le message.

• words.pkl : Le fichier pickle words.pkl contient tous les mots uniques qui constituent le vocabulaire de notre modèle.