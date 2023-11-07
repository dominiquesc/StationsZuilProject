#dominique scoop versie 1.2

import tkinter as tk
from tkinter import Label, Frame
import psycopg2
import requests

#database parameters
db_params = {
    'dbname': 'stationszuil',
    'user': 'postgres',
    'password': 'Eerrttff_786:',
    'host': '20.68.195.240',
    'port': '5432'
}

#declareer open weather api key
OPENWEATHER_API_KEY = '1cc1453e28cfd5e8c4f20b1d9e273764'

#laatste berichte functie declareren
def fetchLastMessages():
    #connectie aanmaken en cursor aanmaken
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    #select statement maken zodat we berichten kunnen tonen we sorteren bij datum en limit van 5 voor laatste 5 chronologische volgorde
    cursor.execute(
        "SELECT station, bericht, datum_tijd "
        "FROM berichten "
        "ORDER BY datum_tijd DESC "
        "LIMIT 5"
    )
    #pakken alle rijen van de query op
    messages = cursor.fetchall()
    #sluit connectie
    conn.close()
    return messages

#declareer weer functie
def fetchWeather(station):
    #vang errors op
    try:
        #maken een api call met ons stationsnaam en api key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={station}&appid={OPENWEATHER_API_KEY}&units=metric"
        #wachten op reactie van api request
        response = requests.get(url)
        data = response.json()
        #lezen weer omschrijving en temperatuur uit de json file
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        #return de weerinfo als er iets terug komt uit call
        return f"Weer informatie: {weather_description}\nTemperatuur: {temperature}°C"
    except Exception as e:
        #return error code als er niks uit de api call komt
        return f"Weer informatie niet beschikbaar voor {station}"


#declareer displaymessages
def displayMessages():
    #declareer wat de berichten zijn in dit geval de select functie bovenaan
    messages = fetchLastMessages()
    message_text.config(state=tk.NORMAL)
    message_text.delete(1.0, tk.END)
    #for loop om alle berichten te laten zien
    for message in messages:
        #laat zien wat de waardes zijn in messages en insert het in tkinter gui
        station, text, date_time  = message
        message_text.insert(tk.END, f"Station: {station}\n")
        message_text.insert(tk.END, f"Bericht: {text}\n")
        message_text.insert(tk.END, f"Datum/Tijd: {date_time}\n")

        #connectie met database parameters
        conn = psycopg2.connect(**db_params)
        #cursor aanmaken
        cursor = conn.cursor()
        #select statement voor faciliteiten
        cursor.execute(
            "SELECT ov_bike, elevator, toilet, park_and_ride "
            "FROM station_service "
            "WHERE station_city = %s", (station,)
        )
        facilities = cursor.fetchone()
        conn.close()

        #hieronder checken we of de 4 boolean waardes in the if statments op true zijn zoja insert het in tkinter gui zodat we faciliteiten tonen per bericht per station
        if facilities:
            message_text.insert(tk.END, "Beschikbare faciliteiten\n")
            ov_bike, elevator, toilet, park_and_ride = facilities
            if ov_bike:
                message_text.insert(tk.END, "OV Bike\n")
            if elevator:
                message_text.insert(tk.END, "Elevator\n")
            if toilet:
                message_text.insert(tk.END, "Toilet\n")
            if park_and_ride:
                message_text.insert(tk.END, "Park and Ride\n")

        #pak weer uit bovenstaande functie per station
        weather_info = fetchWeather(station)
        message_text.insert(tk.END, weather_info + '\n\n')
    message_text.config(state=tk.DISABLED)



#Tkinter logica
root = tk.Tk()
root.title("Stationshalscherm")


root.geometry("1000x800")


label_frame = Frame(root, padx=20, pady=10, bg='lightgray')
label_frame.pack()


title_label = Label(label_frame, text="Stationshalscherm", font=("Arial", 30), bg='lightgray')
title_label.pack()

message_text = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg='lightgray', state=tk.DISABLED)
message_text.pack(expand=True, fill='both')


refresh_button = tk.Button(root, text="Ververs berichten", command=displayMessages)
refresh_button.pack()

displayMessages()

#roep functie aan
root.mainloop()
