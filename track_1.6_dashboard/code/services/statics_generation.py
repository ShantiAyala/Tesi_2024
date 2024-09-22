#Non eseguo statics_generation.py nel main, perchè l'ho eseguito precedentemente per popolare i csv

import os
import pandas as pd
import numpy as np
import csv
import random
from datetime import datetime, timedelta
from faker import Faker
from collections import defaultdict

#Genero statics/price_history.csv--------------------------------------------------------------------------------------

    
def generate_price_variations():
    # Leggi il CSV con i dati originali
    data_csv = pd.read_csv('../statics/products_price_avg_5years.csv')  
    output_file = '../statics/price_history.csv'
    price_history = []
    today = datetime.now()
    
    # Definizione dell'errore statistico (errore relativo)
    error_margin = 0.05  # Errore del 5%

    # Funzione per generare una variazione di prezzo
    def generate_price(base_price):
        return round(base_price * random.uniform(1 - error_margin, 1 + error_margin), 2)

    # Intervalli trimestrali (Gennaio, Aprile, Luglio, Ottobre)
    quarters = [1, 4, 7, 10]

    # Evita duplicati con un set
    unique_entries = set()

    # Itera su ogni combinazione di prodotto e anno
    for _, row in data_csv.iterrows():
        product_name = row['ProductName']
        avg_price = row['AveragePrice']
        year = row['Year']

        # Genera variazioni trimestrali solo fino all'anno attuale
        for month in quarters:
            start_date = datetime(year, month, 1)

            # Se la data è successiva a oggi, interrompi il loop
            if start_date > today:
                break

            # Simula il prezzo con una piccola variazione basata sull'errore statistico
            price_variation = generate_price(avg_price)

            # Genera casualmente lo stato di 'discontinued' (interrotto)
            discontinued = random.choices([False, True], weights=[85, 15])[0]  # 85% False, 15% True

            # Verifica l'unicità della combinazione (ProductName, StartDate)
            unique_key = (product_name, start_date.strftime('%Y-%m-%d'))

            # Aggiungi solo se non esiste già
            if unique_key not in unique_entries:
                unique_entries.add(unique_key)

                # Aggiungi i dati della variazione al price_history
                price_history.append([
                    product_name,
                    start_date.strftime('%Y-%m-%d'),
                    price_variation,
                    discontinued
                ])

    # Crea un DataFrame per salvare i dati generati
    price_history_df = pd.DataFrame(price_history, columns=['ProductName', 'StartDate', 'Price', 'Discontinued'])

    # Salva i dati nel CSV
    price_history_df.to_csv(output_file, index=False)
    print(f"File {output_file} creato con successo!")

# Esegui la funzione
#generate_price_variations()
#--------------------------------------------------------------------------------------

def update_history_price():
    # Leggi il file CSV esistente
    price_history_file = '../statics/price_history.csv'
    price_history_df = pd.read_csv(price_history_file)

    today = datetime.now()
    current_year = today.year

    # Intervalli trimestrali (Gennaio, Aprile, Luglio, Ottobre)
    quarters = [1, 4, 7, 10]

    # Definizione dell'errore statistico (es. una variazione relativa)
    error_margin = 0.05  # 5% di errore relativo per simulare la variazione dei prezzi

    # Controlla se esistono già record per l'anno corrente
    if not price_history_df[price_history_df['StartDate'].str.contains(str(current_year))].empty:
        print(f"I dati per l'anno {current_year} esistono già.")
        return

    new_entries = []

    # Itera sui prodotti esistenti e genera nuove variazioni per l'anno corrente
    for product_name in price_history_df['ProductName'].unique():
        # Filtra i dati dell'anno precedente per il prodotto
        previous_year = current_year - 1
        previous_year_data = price_history_df[
            (price_history_df['ProductName'] == product_name) &
            (price_history_df['StartDate'].str.contains(str(previous_year)))
        ]

        if previous_year_data.empty:
            # Se non ci sono dati dell'anno precedente, salta il prodotto
            print(f"Non ci sono dati per {product_name} nell'anno {previous_year}.")
            continue

        # Genera 4 nuove istanze per l'anno corrente (uno per trimestre)
        for month in quarters:
            # Trova il prezzo dell'anno precedente per lo stesso trimestre
            prev_quarter = previous_year_data[previous_year_data['StartDate'].str.contains(f'-{str(month).zfill(2)}-')]

            if prev_quarter.empty:
                print(f"Non ci sono dati per {product_name} nel trimestre {month}/{previous_year}.")
                continue

            # Prendi il prezzo medio del trimestre precedente
            previous_price = prev_quarter['Price'].values[0]

            # Genera il nuovo prezzo con una piccola variazione basata sull'errore relativo
            new_price = round(previous_price * random.uniform(1 - error_margin, 1 + error_margin), 2)

            # Genera casualmente lo stato di 'discontinued' (interrotto)
            discontinued = random.choices([False, True], weights=[90, 10])[0]  # 90% False, 10% True

            # Crea la data di inizio per il trimestre nell'anno corrente
            start_date = datetime(current_year, month, 1).strftime('%Y-%m-%d')

            # Aggiungi i nuovi dati all'elenco
            new_entries.append([
                product_name,
                start_date,
                new_price,
                discontinued
            ])

    # Se ci sono nuovi dati, aggiungili al file CSV
    if new_entries:
        new_entries_df = pd.DataFrame(new_entries, columns=['ProductName', 'StartDate', 'Price', 'Discontinued'])
        updated_price_history_df = pd.concat([price_history_df, new_entries_df], ignore_index=True)

        # Salva il nuovo file CSV
        updated_price_history_df.to_csv(price_history_file, index=False)
        print(f"I dati per l'anno {current_year} sono stati aggiunti con successo.")
    else:
        print("Nessun nuovo dato da aggiungere.")

#update_history_price()

#Genero statics/weather_conditions.csv-------------------------------------------------------------------------------------

# Funzione per generare una lista di date giornaliere tra due date specifiche
def generate_dates(start_date, end_date):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

# Imposta le date degli ultimi 5 anni
end_date = datetime.now().date()  # Data di oggi
start_date = end_date - timedelta(days=5 * 365)  # Data di inizio, 5 anni fa

# Genera tutte le date negli ultimi 5 anni
dates = generate_dates(start_date, end_date)

# Funzione per generare dati climatici in base al periodo dell'anno
def generate_weather_data(date):
    month = date.month

    # Temperature: medie stagionali
    if 6 <= month <= 8:  # Estate
        temperature = round(random.uniform(25, 35), 2)
    elif 12 <= month or month <= 2:  # Inverno
        temperature = round(random.uniform(5, 15), 2)
    elif 3 <= month <= 5:  # Primavera
        temperature = round(random.uniform(10, 25), 2)
    else:  # Autunno
        temperature = round(random.uniform(10, 20), 2)

    # Umidità: più alta in inverno e nei periodi di pioggia
    humidity = round(random.uniform(50, 90), 2)

    # Precipitazioni: più comuni in autunno e inverno
    precipitation = round(random.uniform(0, 10), 2) if month in [10, 11, 12, 1, 2, 3] else round(random.uniform(0, 2), 2)

    # Velocità del vento: generalmente moderata
    wind_speed = round(random.uniform(0.5, 10), 2)

    # Radiazione solare: più alta in estate
    solar_radiation = round(random.uniform(100, 800) if 5 <= month <= 9 else random.uniform(50, 300), 2)

    # Umidità del suolo: più alta nei mesi piovosi
    soil_moisture = round(random.uniform(10, 50) if month in [10, 11, 12, 1, 2, 3] else random.uniform(5, 20), 2)

    # Descrizione meteo
    if precipitation > 8:
        weather_description = "Forte pioggia"
    elif temperature > 28:
        weather_description = "Soleggiato e caldo"
    elif wind_speed > 8:
        weather_description = "Ventoso"
    elif precipitation > 3:
        weather_description = "Possibile pioggia"
    else:
        weather_description = "Sereno"

    return [date, temperature, humidity, precipitation, wind_speed, solar_radiation, soil_moisture, weather_description]

# Genera i dati meteo per ogni data
weather_data = [generate_weather_data(date) for date in dates]

# Scrivi i dati nel file CSV
with open('../statics/weather_conditions.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Intestazione del CSV
    writer.writerow(['Date', 'Temperature', 'Humidity', 'Precipitation', 'WindSpeed', 'SolarRadiation', 'SoilMoisture', 'WeatherDescription'])
    # Scrivi i dati meteo
    writer.writerows(weather_data)
    print("File weather_conditions.csv generato con successo.")




#--------------------------------------------------------------------------------------