import answer_chatbot

# Vérification de l'identification de la catégorie de la phrase

question = "Hello!"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "greeting", "greeting")

question = "See you!"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "goodbye", "goodbye")

question = "Thank you very much!"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "thanks", "thanks")

question = "What's new?"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "news", "news")

question = "I like you"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "iloveyou", "iloveyou")

question = "What about you?"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "description", "description")

question = "Please help me"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "help", "help")

question = "Tell me my meetings on monday"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "agenda", "agenda")

question = "When am I busy?"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "timebusy", "timebusy")

question = "What is my average busy time?"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "average", "average")

question = "Add a meeting on Monday"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "add", "add")

question = "Delete a meeting on Monday"
(tag, reponse) = answer_chatbot.send(question)
print(tag == "del", "del")
