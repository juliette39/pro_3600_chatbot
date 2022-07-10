import datetime
import sqlite3
import re

path = "/home/juliette/"
path = "/Users/juliettedebono/"
path += "pro3600-mon-test/dev/chatbot-serveur/"
database = path + 'chatbot_bd.db'

def answer(category, sentence, response = "", mac = "02:00:00:44:55:66:"):

    infos = info(sentence, mac)

    if category == "agenda":
        answer = agenda(infos)

    elif category == "timebusy" :
        answer = timebusy(infos)

    elif category == "average" :
        answer = average(infos)

    elif category == "add" :
        answer = add(infos)

    elif category == "del" :
        answer = delete(infos)

    else :
        answer = response

    return answer

def agenda(infos):
    """Renvoie l'agenda sur le lapse de temps"""

    infos = complete_tout(infos)

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    resultat = "{0} :\n".format(infos["day"][0])

    jour_req = "( "

    for jour in infos["day"]:
        jour_req += "Name = '{}' OR ".format(jour)

    jour_req = jour_req[:-4] + ")"

    req = """SELECT Begin, End, Title, Name, Jour FROM
    (SELECT Begin, End, Title, type, Name as jour  FROM AGENDA
    JOIN DAYS ON day = id_day
    WHERE mac = '{3}' AND {0} AND BEGIN >= {1} AND BEGIN <= {2} AND END <= {2})
    JOIN TYPE ON type = id_type;""".format(jour_req, infos["begin"], infos["end"], infos["mac"])

    cur.execute(req)
    i = 0
    for info in cur.fetchall():
        if info[4] != infos["day"][i]:
            i += 1
            resultat += "\n{} :\n".format(infos["day"][i])
        resultat += "{0} - {1} : {2}, {3}\n".format(heure(info[0]), heure(info[1]), info[2], info[3])
    conn.commit()
    conn.close

    return resultat


def timebusy(infos):
    """Renvoie le temps dédié au pro/perso/libre dans un lapse de temps"""

    infos = complete_tout(infos)

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    resultat = "{0} :\n".format(infos["day"][0])

    jour_req = "( "
    for jour in infos["day"]:
        jour_req += "Name = '{}' OR ".format(jour)
    jour_req = jour_req[:-4] + ")"

    req = """SELECT Begin, End, Title, Jour FROM
    (SELECT Begin, End, Title, type, Name as Jour, id_day FROM AGENDA
    JOIN DAYS ON day = id_day
    WHERE {0} AND mac = '{2}')
    JOIN TYPE ON type = id_type WHERE LOWER(Name) = '{1}' ORDER BY id_day;
    """.format(jour_req, infos['type'], infos["mac"])

    cur.execute(req)
    i = 0
    for info in cur.fetchall():
        if info[3] != infos["day"][i]:
            i += 1
            resultat += "\n{} :\n".format(infos["day"][i])

        resultat += "{0} - {1} : {2}\n".format(heure(info[0]), heure(info[1]), info[2])
    conn.commit()
    conn.close

    return resultat


def average(infos):
    """Renvoie la moyenne de temps pro/perso/libre dans la semaine"""

    infos = complete_tout(infos)

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    req = """SELECT AVG(Temps) FROM
    (SELECT SUM(End - Begin) as temps FROM
    (SELECT Begin, End, Title, type, Name as Jour, id_day FROM AGENDA
    JOIN DAYS ON day = id_day WHERE mac = '{1}')
    JOIN TYPE ON type = id_type WHERE LOWER(Name) = '{0}' GROUP BY id_day)""".format(infos["type"], infos["mac"])

    cur.execute(req)
    avg = cur.fetchone()
    resultat = "Average time {0} in the week : {1}".format(infos["type"], heure(int(avg[0])))

    conn.commit()
    conn.close

    return resultat


def add(infos):                              #Fonction add terminée avec le traitement d'erreurs
    """Ajoute un évènement"""

    conn = sqlite3.connect(database)
    cur = conn.cursor()

    rep = forme(infos, ["title", "day", "begin"])
    if rep!="" : #il y a une erreur sur title, day ou begin (au moins un champ est nul)
        conn.commit()
        conn.close
        return rep
    else :

        if infos["end"]==None : #pas de valeur de fin renseignée
            infos["end"]=infos["begin"]+60 #ajouter une heure

        else :

            if infos["begin"] >= infos["end"] : #l'heure de début est plus grande que l'heure de fin
                conn.commit()
                conn.close
                return "The end time of the event is incorrect"

            else : #pas d'erreurs dans les infos
                type = ["pro", "perso", "undefined"].index(infos["type"])

                if not_intersect(infos["day"],infos["begin"],infos["end"], infos["mac"]) : #vérifier que deux événements ne se superposent pas

                    if infos["type"]==None : #pas de type renseigné
                        res="INSERT INTO agenda (Day, Begin, End, Title, Mac) VALUES ({0}, {1}, {2}, {3}, {4});".format(infos["day"], infos["begin"], infos["end"], infos["title"], infos["mac"])
                        cur.execute(res)
                        conn.commit()
                        conn.close
                        return "I modified your agenda"

                    else : #un type est renseigné
                        for day in infos["day"]:
                            day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day)
                            req="INSERT INTO agenda (Day, Begin, End, Type, Title, Mac) VALUES ('{0}', {1}, {2}, {3}, '{4}', '{5}');".format(day, infos["begin"], infos["end"], type, infos["title"], infos["mac"])

                            cur.execute(req)
                        conn.commit()
                        conn.close
                        return "I updated your agenda"

                else : #superposition avec un autre événement
                    conn.commit()
                    conn.close
                    return "There is already an event during this period of time"


def delete(infos):                  #Fonction terminée, peut être améliorée pour afficher les événements supprimés
    """Supprime un évènement"""

    #informations nécessaires pour supprimer un événement : jour et heure de début, ou titre
    conn = sqlite3.connect(database)
    cur = conn.cursor()


    if "title" in infos and infos["title"] != "Untitle event" : #le titre est reseigné

        suppr="DELETE FROM agenda WHERE Title='{0}' AND Mac = '{1}'".format(infos["title"], infos["mac"])

        cur.execute(suppr)
        conn.commit()
        conn.close
        return "I deleted the event from your agenda"

    else : #le jour et begin sont renseignés

        try :
            day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(infos["day"][0])
            suppr="DELETE FROM agenda WHERE Day={0} AND Begin={1} AND Mac = '{2}'".format(day, infos["begin"], infos["mac"])
            cur.execute(suppr)
            conn.commit()
            conn.close
            return "I deleted the event from your agenda"

        except :
            conn.close
            return "I don't have enough information to know which event I need to delete"

    conn.close



def info(sentence, mac):
    """Trouve les infos dans la phrase"""

    day, begin, end, type, title = [], None, None, None, None

    # Day
    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    today = day_name.index(date.strftime("%A"))

    for day_i in day_name:
        if day_i.lower() in sentence.lower():
            day.append(day_i)

    if "today" in sentence.lower():
        day = [day_name[today],]
    if "tomorrow" in sentence.lower():
        day = [day_name[today + 1],]
    if "yesteday" in sentence.lower():
        day = [day_name[today - 1],]

    # Title
    guillements = ['"', '“', '”', '‘', '’', '«', '»']

    for i in guillements:
        sentence = sentence.replace(i, "'")

    if "'" in sentence:
        title = sentence.split("'")[1]

    # Type
    all_type = ["pro", "perso"]
    for type_i in all_type:
        if type_i.lower() in sentence.lower():
            type = type_i
            break

    hour = re.findall(r'[\d{1,2}:?\d{2}]+', sentence.replace(",", ""))
    time = re.findall(r'[ap]m', sentence)

    if len(time) == 0:
        time = ["am"]

    if len(time) > 0:
        try:
            heure = format_heure(hour[0], time[0])
            begin = minute(heure)
        except IndexError:
            time = ["am"]
        except ValueError:
            time = []

    if len(hour) > 1:

        if len(time) < 2 :
            if "h " in sentence or "hour" in sentence:
                end = begin + int(hour[1])*60

            else :
                end = begin + int(hour[1])

        else:
            heure = format_heure(hour[1], time[1])
            end = minute(heure)

    # Gestion si on ne trouve pas les éléments
    if begin is None:
        begin = 0

    if end is None:
        end = 24*60

    if day == []:
        day = day_name[today]

    if type is None:
        type = "undefined"

    if title is None:
        title = "Untitled event"

    return {"day" : day, "begin" : begin, "end" : end, "type" : type, "title" : title, "mac" : mac}

def heure(minutes):
    """Converti un temps en minute en un horaire lisible"""
    heures = minutes//60
    minutes = minutes - heures * 60
    if heures>12 :
        return "{0}:{1:02d}pm".format(heures-12, minutes)
    else :
        return "{0}:{1:02d}am".format(heures, minutes)

def minute(heures):
    """Converti un horaire en minutes"""
    heures = heures.split(":")
    time = heures[1][2]
    if time == 'a' : #matin
        return int(heures[0])*60 + int(heures[1][:-2])
    else : #après-midi
        return int(heures[0])*60+12*60 + int(heures[1][:-2])

def format_heure(heure, time):
    """Corrige les erreurs de format des horaires"""
    if ":" in heure:
        heure = heure.split(":")
        return "{0}:{1:02d}{2}".format(int(heure[0]), int(heure[1]), time)
    else:
        return "{0}:00{1}".format(heure, time)

def not_intersect(d,begin,end, mac) : #end est après début

    conn=sqlite3.connect(database)
    cur=conn.cursor()

    req="SELECT COUNT(*) FROM AGENDA JOIN DAYS ON Day=id_day WHERE Mac = '{3}' AND Name='{0}' AND ((Begin<{1} AND End>{1}) OR ({1}<Begin AND Begin<{2}));".format(d[0], begin, end, mac)

    cur.execute(req)
    res = cur.fetchone()
    conn.commit()
    conn.close
    return res[0] == 0

def forme(infos, necessaire) : #retourne "" si aucune erreur, et l'erreur sinon
    rep=""
    for i in necessaire :
        if infos[i] is None :
            if rep=="" :
                rep="I didn't understand the {0}".format(i)
            else :
                rep=rep + "and the {0}".format(i)
    return rep


def complete_tout(infos):
    """Gestion si on ne trouve pas les éléments"""

    if infos["begin"] is None:
        infos["begin"] = 0

    if infos["end"] is None:
        infos["end"] = 24*60

    if infos["day"] == []:
        infos["day"] = day_name[today]

    if infos["type"] is None:
        infos["type"] = "undefined"

    if infos["title"] is None:
        infos["title"] = "Untitled event"

    return infos

date = datetime.datetime.now()
