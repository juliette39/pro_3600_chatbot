#! /usr/local/bin/python

from flask import Flask, request
from traitement import answer
from answer_chatbot import send

app = Flask(__name__)

@app.route("/")
def cgi():
    question = request.args.get("question", "Show me my day of monday from 5am to 5pm").replace("_", " ").split("mac=")[0].strip(";")
    mac = request.args.get("mac", "02:00:00:44:55:66:")

    (tag, reponse) = send(question)
    result = answer(tag, question, reponse, mac)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)