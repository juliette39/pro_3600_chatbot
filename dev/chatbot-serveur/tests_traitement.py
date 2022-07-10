import traitement
import sqlite3

# Vérification des fonctions du traitement de la phrase en question

path = "/home/juliette/"
path = "/Users/juliettedebono/"
path += "pro3600-mon-test/dev/chatbot-serveur/"
database = path + 'chatbot_bd.db'

mac = "02:00:00:44:55:66:"

## Infos

sentence = "Tell me when I have a meetings on tuesday from 10am to 11am."
infosNormal = {'day': ['Tuesday'], 'begin': 600, 'end': 660, 'type': 'undefined', 'title': 'Untitle event', 'mac': '02:00:00:44:55:66:'}

infos = traitement.info(sentence, mac)

print(infos == infosNormal)


## Add

traitement.add(infos)

conn = sqlite3.connect(database)
cur = conn.cursor()

req = """SELECT day, begin, end, type, title FROM AGENDA WHERE mac = '02:00:00:44:55:66:' AND day = 1 AND BEGIN >= 600 AND BEGIN <= 660 AND END <= 660;"""

cur.execute(req)
result = cur.fetchone()
conn.commit()
conn.close

print(result == (1, 600, 660, 2, 'Untitle event'))

## Agenda

result = traitement.agenda(infos)

print(result == 'Tuesday :\n10:00am - 11:00am : Untitle event, Non défini\n')

## Delete

print(traitement.delete(infos) == "I deleted the event from your agenda")

conn = sqlite3.connect(database)
cur = conn.cursor()

req = """SELECT day, begin, end, type, title FROM AGENDA WHERE mac = '02:00:00:44:55:66:' AND day = 1 AND BEGIN >= 600 AND BEGIN <= 660 AND END <= 660;"""

cur.execute(req)
result = cur.fetchone()
conn.commit()
conn.close

print(result is None)

print(traitement.delete({}) == "I don't have enough information to know which event I need to delete")

## Infos Pro
s
infos = {'day': ['Thursday'], 'begin': 780, 'end': 840, 'type': 'pro', 'title': 'meeting pro', 'mac': '02:00:00:44:55:66:'}

## Add Pro

traitement.add(infos)

conn = sqlite3.connect(database)
cur = conn.cursor()

req = """SELECT day, begin, end, type, title FROM AGENDA WHERE mac = '02:00:00:44:55:66:' AND day = 3 AND BEGIN >= 780 AND BEGIN <= 900 AND END <= 900 AND type=0;"""

cur.execute(req)
result = cur.fetchone()
conn.commit()
conn.close
del cur, conn
print(result == (3, 780, 840, 0, 'meeting pro'))

## timebusy Pro

sentence = "When have I time pro on Thursday?"

infos = traitement.info(sentence, mac)
result = traitement.timebusy(infos)


## Delete Pro

infos = {'day': ['Thursday'], 'begin': 780, 'end': 840, 'type': 'pro', 'title': 'meeting pro', 'mac': '02:00:00:44:55:66:'}

print(traitement.delete(infos) == "I deleted the event from your agenda")

conn = sqlite3.connect(database)
cur = conn.cursor()

req = """SELECT day, begin, end, type, title FROM AGENDA WHERE mac = '02:00:00:44:55:66:' AND day = 3 AND BEGIN >= 780 AND BEGIN <= 660 AND END <= 840 AND type=0;"""

cur.execute(req)
result = cur.fetchone()
conn.commit()
conn.close

print(result is None)