#! /usr/local/bin/python

from traitement import answer
from answer_chatbot import send

def ask(question):

    (tag, reponse) = send(question)
    result = answer(tag, question, reponse)
    return result

