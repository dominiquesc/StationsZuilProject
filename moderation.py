#dominique scoop versie 1.2

from pprint import pprint
import psycopg2
import csv
from datetime import datetime
import os

#db connectie parameters
dbconnection = {
    'dbname': 'stationszuil',
    'user': 'postgres',
    'password': 'Eerrttff_786:',
    'host': '20.68.195.240',
    'port': '5432'
}

# Declareer de functie
def processMessages():
    # pen het geimporteerde csv bestand
    with open('messages.csv', 'r') as file:
        messages = csv.reader(file)
        approved_messages = []  # vang goedgekeurde berichten op in een lege array
        for message in messages:
            #kleine veiligheads check om de kijken of er 4 waarden in bericht zit anders word de functie niet uitgevoerd zorgde voor fouten
            if len(message) == 4:
                text, date_time, user_name, station = message
                #strip for Y als het niet y is wordt het niet uitgevoerd
                approval_status = input(f"bericht goedkeuren: '{text}'? (y/n): ").strip().lower() == 'y'
                #variabele om relevante tijd te pakken
                approval_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                moderator_name = input('Moderator naam: ')
                moderator_email = input('Moderator email: ')
                #als approvalstatus gelijk is aan Y word de if statement uitgevoerd
                if approval_status:
                    #maak een connectie met de database doormiddel van de db parameters
                    conn = psycopg2.connect(**dbconnection)
                    #maak een connectie cursor
                    cursor = conn.cursor()
                    # insert de berichten in de database
                    cursor.execute(
                        "INSERT INTO berichten (bericht, datum_tijd, gebruikersnaam, station, goedgekeurd, goedkeuring_datum_tijd, moderator_naam, moderator_email) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (text, date_time, user_name, station, approval_status, approval_date_time, moderator_name, moderator_email)
                    )
                    #commit de gegevens naar de database
                    conn.commit()
                    #sluit de database connectie
                    conn.close()
                else:
                    #als het bericht niet is goedgekeurd voeg het toe aan de approvedmessages
                    approved_messages.append(message)

        #maak het csv file leeg
        with open('messages.csv', 'w', newline='') as file:
            file.write('')

        #schrijf de berichten terug naar csv bestand
        with open('messages.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(approved_messages)

#roep de functie aan om het uit te voeren
processMessages()
