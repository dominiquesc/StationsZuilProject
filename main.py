#dominique scoop versie 1.2

import csv
from datetime import datetime
import random
import psycopg2

#array van stationsnamen
stations = ['Arnhem', 'Almere', 'Amersfoort', 'Almelo', 'Alkmaar', 'Apeldoorn', 'Assen', 'Amsterdam', 'Boxtel', 'Breda',
          'Dordrecht', 'Delft', 'Deventer', 'Enschede', 'Gouda', 'Groningen', 'Den Haag', 'Hengelo', 'Haarlem', 'Helmond', 'Hoorn', 'Heerlen', 'Den Bosch', 'Hilversum',
          'Leiden', 'Lelystad', 'Leeuwarden', 'Maastricht', 'Nijmegen', 'Oss', 'Roermond', 'Roosendaal', 'Sittard', 'Tilburg', 'Utrecht', 'Venlo', 'Vlissingen', 'Zaandam', 'Zwolle', 'Zutphen']

#declareer functie save messages
def saveMessage():
    #input opvragen als gebruiksnaam leeg is het anoniem
    bericht = input("Voer je bericht in (maximaal 140 karakters): ").strip()
    gebruikersnaam = input("Voer je naam in (laat leeg voor 'anoniem'): ").strip()
    gebruikersnaam = gebruikersnaam if gebruikersnaam else "anoniem"
    #random waarde bij stations
    station = random.choice(stations)
    #datum variabele aanmaken
    datum_tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if len(bericht) <= 140:
        #sla de data op in een csv bestand
        with open('messages.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            #schrijf een nieuwe rij aan gegevens
            writer.writerow([bericht, datum_tijd, gebruikersnaam, station])
            print('Success! Je bericht is opgeslagen')
    else:
        #als je bericht langer is dan 140 characters krijg je deze print en wordt het bericht niet opgeslagen
        print('Onthoud je bericht mag niet langer zijn dan 140 karakters')


#declareer functie
saveMessage()
