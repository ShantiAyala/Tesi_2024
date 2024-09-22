import csv
import random
import string
import pandas as pd
import psycopg2
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
from cleanup import close_db_connection
from db_handler import connect_to_db
from decimal import Decimal
from dateutil.relativedelta import relativedelta


# Inizializza Faker per generare dati italiani
fake = Faker('it_IT')

# Generazione Employees ----------------------------------------------------------------------------

# Mappatura città e codici postali
CITY_ZIP_CODE_MAPPING = {
    "Grosseto": "58100",
    "Marina di Grosseto": "58100",
    "Principina a Mare": "58100",
    "Principina Terra": "58100",
    "Braccagni": "58100",
    "Rispescia": "58100",
    "Alberese": "58100",
    "Istia d'Ombrone": "58100",
    "Roselle Terme": "58100",
    "Batignano": "58100",
    "Montepescali": "58100",
    "Grancia": "58100",
    "Bagno Roselle": "58100",
    "Ponte Tura": "58100",
    "Podere Giardino": "58100",
    "Castiglione della Pescaia": "58043",
    "Vetulonia": "58043",
    "Buriano": "58043",
    "Giuncarico": "58023",
    "Caldana": "58023",
    "Sticciano Scalo": "58036",
    "Campagnatico": "58042",
    "Arcille": "58042",
    "Baccinello": "58051",
    "Montorsaio": "58051",
    "Montiano": "58051",
    "Roccastrada": "58036",
    "Ribolla": "58027",
    "Paganico": "58045",
    "Civitella Marittima": "58045"
}

# Ruoli con stipendi medi
JOBS_SALARIES = {
    "Direttore Agricolo": (50000, 70000),
    "Agronomo": (35000, 50000),
    "Tecnico Agrario": (28000, 40000),
    "Capo Coltivatore": (30000, 45000),
    "Operaio Agricolo Specializzato": (25000, 35000),
    "Operaio Agricolo": (20000, 28000),
    "Addetto alla Raccolta": (18000, 25000),
    "Responsabile di Magazzino": (28000, 40000),
    "Addetto alla Manutenzione": (22000, 30000),
    "Zootecnico": (30000, 45000),
    "Veterinario": (40000, 55000),
    "Contabile Agricolo": (25000, 35000),
    "Responsabile Vendite": (35000, 50000),
    "Addetto al Confezionamento": (20000, 27000),
    "Responsabile Qualità": (30000, 45000),
    "Assistente di Fattoria": (18000, 25000),
    "Trattorista": (24000, 32000),
    "Irrigatore": (18000, 26000),
    "Responsabile Logistica": (30000, 45000),
    "Esperto di Irrigazione": (28000, 38000)
}


# Funzione per generare email personalizzate
def generate_email(first_name, last_name):
    """Genera un'email basata parzialmente su first_name e last_name con fino a 6 caratteri aggiuntivi."""
    name_part = f"{first_name[:random.randint(1, len(first_name))].lower()}"
    surname_part = f"{last_name[:random.randint(1, len(last_name))].lower()}"
    
    # Aggiungi da 0 a 6 caratteri casuali
    random_length = random.randint(0, 6)
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random_length))
    
    domain = fake.free_email_domain()
    return f"{name_part}{surname_part}{random_string}@{domain}"

# Genera dati per un numero specificato di dipendenti
def generate_employee_data(n):
    employees = []
    for _ in range(n):
        city = random.choice(list(CITY_ZIP_CODE_MAPPING.keys()))
        zipcode = CITY_ZIP_CODE_MAPPING[city]
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = generate_email(first_name, last_name)
        phone = f"+39 {fake.msisdn()[:10]}"
        state = "Toscana"
        country = "Italia"
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)
        gender = random.choice(['Male', 'Female'])
        hire_date = fake.date_between(start_date='-10y', end_date='today')
        job_title = random.choice(list(JOBS_SALARIES.keys()))
        salary_range = JOBS_SALARIES[job_title]
        salary = round(random.uniform(salary_range[0], salary_range[1]), 2)
        employment_status = random.choice(['Determinato', 'Indeterminato'])
        emergency_contact = f"{fake.name()} - +39 {fake.msisdn()[:10]}"

        employees.append({
            "FirstName": first_name,
            "LastName": last_name,
            "Email": email,
            "Phone": phone,
            "City": city,
            "State": state,
            "ZipCode": zipcode,
            "Country": country,
            "DateOfBirth": date_of_birth,
            "Gender": gender,
            "HireDate": hire_date,
            "JobTitle": job_title,
            "Salary": salary,
            "EmploymentStatus": employment_status,
            "EmergencyContact": emergency_contact
        })

    return employees





#Non credo di usarla.. ------------------------------- ??--------

# Funzione per inserire i dati nel database
def insert_data_to_db(employees):
    try:
        # Connessione al database
        conn, cursor = connect_to_db()
        
        # Query per inserire i dati
        insert_query = """
        INSERT INTO Employees (FirstName, LastName, Email, Phone, City, State, ZipCode, Country, 
        DateOfBirth, Gender, HireDate, JobTitle, Salary, EmploymentStatus, EmergencyContact) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Inserisce ogni dipendente nel database
        for emp in employees:
            cursor.execute(insert_query, (
                emp["FirstName"], emp["LastName"], emp["Email"], emp["Phone"], emp["City"], emp["State"], 
                emp["ZipCode"], emp["Country"], emp["DateOfBirth"], emp["Gender"], emp["HireDate"], 
                emp["JobTitle"], emp["Salary"], emp["EmploymentStatus"], emp["EmergencyContact"]
            ))
        
        # Conferma le modifiche
        conn.commit()
        print(f"{len(employees)} record inseriti con successoin Employees.")
        
    except Exception as e:
        print(f"Errore durante l'inserimento dei dati: {e}")
    finally:
        cursor.close()
        conn.close()




# Generazione Products ----------------------------------------------------------------------------

# Categorie e nomi dei prodotti associati
categories = {
    'Cereali': ['grano', 'orzo', 'avena', 'farro'],
    'Frutta': ['uva', 'albicocche', 'pesche', 'ciliegie', 'mele', 'fichi', 'olive'],
    'Ortaggi': ['pomodori', 'zucchine', 'cipolle', 'asparagi', 'carciofi'],
    'Legumi': ['fagioli', 'ceci', 'lenticchie'],
    'Processati': ['vino', 'olio', 'marmellate']
}
# Funzione per popolare la tabella Products con un prodotto per ogni prodotto
def generate_products_table():
    conn, cursor = connect_to_db()
    
    try:
        for category, product_names in categories.items():
            for product_name in product_names:
                # Genera casualmente lo stock 
                stock_quantity = random.randint(0, 400)
                            
                # Inserisci i dati nel database lasciando il campo Price vuoto
                cursor.execute(
                    """
                    INSERT INTO Products (ProductName, Category, StockQuantity)
                    VALUES (%s, %s, %s)
                    """,
                    (product_name, category, stock_quantity)
                )
        print("Tabella popolata con un prodotto per ogni nome prodotto.")
    except Exception as e:
        print(f"Errore durante l'inserimento: {e}")
    finally:
        cursor.close()
        conn.close()

# Riempimento di PriceHistory da csv generato ------------------------------------------------------

# Percorso del CSV
csv_path = 'statics/price_history.csv'

def populate_price_history(csv_path):
    """Popola la tabella PriceHistory utilizzando i dati dal CSV."""
    conn, cur = connect_to_db()
    
    # Carica i dati dal CSV
    df = pd.read_csv(csv_path)
    
    for index, row in df.iterrows():
        product_name = row['ProductName']
        start_date = row['StartDate']
        price = row['Price']
        discontinued = row['Discontinued']
        # Recupera ProductID
        cur.execute("""
            SELECT ProductID FROM Products
            WHERE ProductName = %s
        """, (product_name,))
        
        result = cur.fetchone()
        if result:
            product_id = result[0]
            
            # Inserisci i dati in PriceHistory
            cur.execute("""
                INSERT INTO PriceHistory (ProductID, ProductName, StartDate, Price, Discontinued)
                VALUES (%s, %s, %s, %s, %s)
            """, (product_id, product_name, start_date,  price, discontinued))
        else:
            print(f"Product '{product_name}' not found in Products table.")
    
    cur.close()
    conn.close()

#Genera Costumers_feedback-------------------------------------------------

# Funzione per leggere i commenti dal CSV
def load_comments_from_csv(file_path):
    comments = {1: [], 2: [], 3: [], 4: [], 5: []}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            rating = int(row[0])
            comment = row[1]
            comments[rating].append(comment)
    return comments

# Carica i commenti dal file CSV
comments = load_comments_from_csv('statics/feedback_comments.csv')


def generate_random_feedback():
    
    # Rating e commenti
    ratings = [1, 2, 3, 4, 5]
    rating_weights = [0.01, 0.03, 0.05, 0.11, 0.80]  # Percentuali per i rating
    rating = random.choices(ratings, weights=rating_weights, k=1)[0]

   

    # Genera un nome cliente
    customer_name = fake.first_name()

    # Data casuale tra 5 anni fa e oggi
    start_date = datetime.now() - timedelta(days=5*365)
    end_date = datetime.now()
    date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    comment = random.choice(comments[rating])  
    return customer_name, date.strftime('%Y-%m-%d'), rating, comment

# Funzione per popolare la tabella CustomerFeedback
def populate_customer_feedback(n):
    conn, cur = connect_to_db()
    
    try:
        # Recupera gli ID dei prodotti dalla tabella Products
        cur.execute("SELECT ProductID FROM Products;")
        product_ids = [row[0] for row in cur.fetchall()]

        if not product_ids:
            raise Exception("Nessun prodotto trovato nella tabella Products.")

        for _ in range(n):
            customer_name, date, rating, comment = generate_random_feedback()
            best_product_id = random.choice(product_ids)

            # Inserisci i dati nella tabella CustomerFeedback
            cur.execute(
                """
                INSERT INTO CustomerFeedback (Date, Rating, Comment, BestProductID, CostumerName)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (date, rating, comment, best_product_id, customer_name)
            )
        
        print(f"Tabella CustomerFeedback popolata con {n} record.")
    except Exception as e:
        print(f"Errore durante l'inserimento: {e}")
    finally:
        cur.close()
        conn.close()

#Generazione WeatherConditions data----------------------------------------------------------------------------

def populate_weather_table():

    conn, cursor = connect_to_db()

    try:
        # Lettura dei dati dal CSV
        with open('statics/weather_conditions.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Salta l'intestazione

            # Query SQL per inserire i dati nella tabella WeatherConditions
            insert_query = """
            INSERT INTO WeatherConditions 
            (Date, Temperature, Humidity, Precipitation, WindSpeed, SolarRadiation, SoilMoisture, WeatherDescription) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Iterazione su ciascuna riga del CSV e inserimento nel database
            for row in reader:
                # Conversione dei valori dal CSV se necessario
                date = row[0]
                temperature = float(row[1])
                humidity = float(row[2])
                precipitation = float(row[3])
                wind_speed = float(row[4])
                solar_radiation = float(row[5])
                soil_moisture = float(row[6])
                weather_description = row[7]

                # Esecuzione dell'inserimento nel database
                cursor.execute(insert_query, (date, temperature, humidity, precipitation, wind_speed, solar_radiation, soil_moisture, weather_description))

        # Salvataggio delle modifiche
        conn.commit()
        print("Dati inseriti con successo nella tabella WeatherConditions.")

    except Exception as e:
        print(f"Errore durante l'inserimento: {e}")
    finally:
        cursor.close()
        conn.close()

#Generazione WorkHours----------------------------------------------------------------------------

# Funzione per generare le ore di lavoro
def populate_work_hours():
    try:
        conn, cursor = connect_to_db()

        # Ottieni la lista dei dipendenti
        cursor.execute("SELECT EmployeeID, HireDate FROM Employees;")
        employees = cursor.fetchall()

        today = datetime.now().date()
        holidays = [datetime(today.year, 12, 25), datetime(today.year, 1, 1), datetime(today.year, 6, 2)]

        for employee in employees:
            employee_id, hire_date = employee

            # Genera i record settimanali
            current_date = hire_date
            while current_date <= today:
                # Skip holidays
                if current_date in holidays:
                    current_date += timedelta(days=1)
                    continue
                
                # Aggiungi 5 record a settimana
                for i in range(5):
                    work_type_prob = random.random()
                    if work_type_prob < 0.0769:
                        work_type = 'Ferie'
                    else:
                        sick_prob = random.random()
                        if sick_prob < 0.06:
                            work_type = 'Malattia'
                        else:
                            work_type = 'Regular'

                    overtime_hours = random.choices([0, 1, 2, 3, 4, 5], weights=[90, 0.2, 0.2, 0.2, 0.2, 0.2])[0]

                    # Inserisci il record
                    cursor.execute("""
                        INSERT INTO WorkHours (EmployeeID, Date, HoursWorked, OvertimeHours, WorkType)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (employee_id, current_date, 8, overtime_hours, work_type))

                # Passa alla settimana successiva
                current_date += timedelta(weeks=1)

        # Salva le modifiche
        conn.commit()
        print("Dati inseriti con successo nella tabella WorkHours.")

    except Exception as e:
        print(f"Errore durante l'inserimento dei dati: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

#Generation Farm ------------------------------------------------------------------
# Funzione per ottenere il numero di dipendenti
def get_employee_count(cursor):
    cursor.execute("SELECT COUNT(EmployeeID) FROM Employees")
    count = cursor.fetchone()[0]
    return count

# Funzione per ottenere tutti i nomi dei prodotti
def get_product_names(cursor):
    cursor.execute("SELECT ProductName FROM Products")
    product_names = cursor.fetchall()
    return ', '.join([name[0] for name in product_names])

# Funzione per leggere il CSV delle macchine
def read_machinery_csv():
    df = pd.read_csv('statics/macchine_aziende_agricole.csv')
    machinery_text = '; '.join(df['Nome'] + ' (' + df['Tipo'] + '): ' + df['Descrizione'])
    return machinery_text

def insert_farm_data():
    conn, cursor = connect_to_db()

    # Generazione di dati casuali
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = generate_email(first_name, last_name)
    phone = f"+39 {fake.msisdn()[:10]}"

    # Ottieni il numero di dipendenti e i nomi dei prodotti
    number_of_employees = get_employee_count(cursor)
    primary_crops = get_product_names(cursor)
    machinery = read_machinery_csv()

    # Dati per la tabella Farm
    farm_name = 'ATTavola, Agricoltura Tradizionale Toscana'
    owner_name = f"{first_name} {last_name}"
    established_date = '2014-09-11'
    location = 'Via Fiesole 5 - 58100 Grosseto (GR), Toscana, Italia'
    total_area = 35
    cultivated_area = 32
    farm_type = 'Azienda Agricola Biodinamica'
    certifications = 'Certificazione ISO 22000, Certificazione Social Accountability 8000 (SA8000), Certificazione DOP (Denominazione di Origine Protetta), Certificazione DOC (Denominazione di Origine Controllata), Certificazione IFS (International Featured Standards)'
    soil_type = 'Suolo Limoso'
    climate_zone = 'Mediterranea'

    # Inserisci i dati nella tabella Farm
    cursor.execute("""
        INSERT INTO Farm (
            FarmName, OwnerName, EstablishedDate, Location, TotalArea, CultivatedArea, NumberOfEmployees,
            ContactEmail, ContactPhone, FarmType, Certifications, PrimaryCrops, Machinery, SoilType, ClimateZone
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        farm_name, owner_name, established_date, location, total_area, cultivated_area, number_of_employees,
        email, phone, farm_type, certifications, primary_crops, machinery, soil_type, climate_zone
    ))

    conn.commit()
    print("Dati inseriti con successo nella tabella Farm.")
    cursor.close()
    conn.close()


#Generate Transition e Sales ----------------------------------------------------------------------------

# Funzione per creare transazioni
def create_transactions(start_date, end_date):
    conn, cursor = connect_to_db()
    if conn is None:
        return
    current_date = start_date

    # Generazione delle transazioni giorno per giorno
    while current_date <= end_date:
        num_transactions = random.randint(5, 30)
        for _ in range(num_transactions):
            total_amount = Decimal(round(random.uniform(10, 600), 2)) #prima era (30, 1500), 2)
            payment_method = random.choice(['carta', 'contanti', 'paypal'])
            transaction_status = random.choices(
                ['completata', 'sospesa', 'annullata'],
                weights=[99, 0.7, 0.3],
                k=1
            )[0]

            # Inserimento della transazione nel database
            cursor.execute("""
                INSERT INTO Transactions (Date, TotalAmount, PaymentMethod, TransactionStatus)
                VALUES (%s, %s, %s, %s) RETURNING TransactionID;
            """, (current_date, total_amount, payment_method, transaction_status))
        
        # Incrementa la data di un giorno
        current_date += timedelta(days=1)

    # Commit delle transazioni e chiusura
    conn.commit()
    cursor.close()
    conn.close()
    print("Transazioni create con successo.")

# Funzione per creare vendite per le transazioni completate
def create_sales():
    conn, cursor = connect_to_db()

    # Seleziona tutte le transazioni completate
    cursor.execute("SELECT TransactionID, Date, TotalAmount, PaymentMethod FROM Transactions WHERE TransactionStatus = 'completata';")
    transactions = cursor.fetchall()

    for transaction in transactions:
        transaction_id, sale_date, total_amount, payment_method = transaction
        num_sales = random.randint(1, 15)
        total_sales_amount = Decimal(0)
        max_amount = Decimal(1237)  # Limite massimo per total_sales_amount, altrimenti scontrini troppo alti

        for _ in range(num_sales):
            if total_sales_amount >= max_amount:
                break

            # Seleziona un prodotto casuale
            cursor.execute("SELECT ProductID, StockQuantity FROM Products ORDER BY RANDOM() LIMIT 1")
            product = cursor.fetchone()
            product_id, stock_quantity = product

            # Calcola la quantità massima che possiamo vendere senza superare il limite
            remaining_amount = max_amount - total_sales_amount
            max_quantity = remaining_amount / 100  # Supponendo un prezzo massimo di 100 per unità per sicurezza

            if max_quantity < 1:
                break 

            # Seleziona una quantità casuale compatibile con il rimanente
            quantity = random.randint(1, min(20, int(max_quantity)))

            # Riassortimento se necessario
            if stock_quantity < quantity:
                restock_amount = random.randint(quantity + 100, 500)  # Prima era 1000
                cursor.execute("UPDATE Products SET StockQuantity = StockQuantity + %s WHERE ProductID = %s", (restock_amount, product_id))
                conn.commit()
                stock_quantity += restock_amount

            # Aggiorna lo stock
            cursor.execute("UPDATE Products SET StockQuantity = StockQuantity - %s WHERE ProductID = %s", (quantity, product_id))
            conn.commit()

            # Ottieni il prezzo dal PriceHistory
            cursor.execute("""
                SELECT Price, Discontinued FROM PriceHistory 
                WHERE ProductID = %s AND StartDate <= %s
                ORDER BY StartDate DESC LIMIT 1
            """, (product_id, sale_date))
            price_history = cursor.fetchone()

            if price_history:
                unit_price = Decimal(price_history[0])
                discontinued = price_history[1]
                discount = Decimal(0.95) if discontinued else Decimal(1.00)
            else:
                # Se non c'è uno storico valido, prezzo casuale e nessuno sconto
                unit_price = Decimal(round(random.uniform(10, 100), 2))
                discount = Decimal(1.00)

            total_price = round(unit_price * Decimal(quantity) * discount, 2)

            # Se l'aggiunta del prezzo totale supera il limite, riduci la quantità e calcola il nuovo total_price
            if total_sales_amount + total_price > max_amount:
                max_possible_quantity = int((max_amount - total_sales_amount) / (unit_price * discount))
                if max_possible_quantity < 1:
                    break 
                quantity = max_possible_quantity
                total_price = round(unit_price * Decimal(quantity) * discount, 2)

            total_sales_amount += total_price

            # Determina il canale di vendita
            if payment_method == 'paypal':
                sales_channel = 'Online'
            elif payment_method == 'contanti':
                sales_channel = 'Store'
            else:
                sales_channel = random.choice(['Online', 'Store'])

            # Inserisce la vendita nel database
            cursor.execute("""
                INSERT INTO Sales (Date, ProductID, TransactionID, Quantity, UnitPrice, TotalPrice, Discount, SalesChannel)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (sale_date, product_id, transaction_id, quantity, unit_price, total_price, discount, sales_channel))

        # Aggiorna il TotalAmount della transazione se la somma delle vendite non combacia
        if round(total_sales_amount, 2) != round(total_amount, 2):
            cursor.execute("UPDATE Transactions SET TotalAmount = %s WHERE TransactionID = %s", (total_sales_amount, transaction_id))
            conn.commit()

    # Commit delle vendite e chiusura
    conn.commit()
    cursor.close()
    conn.close()
    print("Vendite create con successo.")

    
def calcola_giorni_da_inizioAnno():
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    days_since_start_of_year = (now - start_of_year).days
    return days_since_start_of_year


#Populate Crops-------------------------------------------------------------------------------------------

def populate_crops_table():
    conn, cur = connect_to_db()
    try:
        df = pd.read_csv('statics/crops_info.csv')
        # Controlla che la colonna 'Replant' esista e convertila in boolean
        if 'Replant' in df.columns:
            # Converte i valori della colonna 'Replant' in booleani
            df['Replant'] = df['Replant'].apply(lambda x: str(x).strip().lower() in ['true', '1', 'yes'])
        else:
            print("Colonna 'Replant' non trovata nel CSV.")
            return
        # Loop attraverso le righe del DataFrame e inserimento nella tabella
        for index, row in df.iterrows():
            cur.execute("""
                INSERT INTO Crops (
                    CropName, ScientificName, Description, PlantingSeason, 
                    HarvestSeason, GrowthDuration, SoilType, 
                    OptimalTemperatureMin, OptimalTemperatureMax, 
                    OptimalHumidityMin, OptimalHumidityMax, 
                    OptimalPrecipitationMin, OptimalPrecipitationMax, 
                    OptimalSunlightHours, FertilizersRequired, 
                    PestsAndDiseases, WateringNeeds, Replant
                ) 
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                row['CropName'], row['ScientificName'], row['Description'], 
                row['PlantingSeason'], row['HarvestSeason'], row['GrowthDuration'], 
                row['SoilType'], row['OptimalTemperatureMin'], row['OptimalTemperatureMax'], 
                row['OptimalHumidityMin'], row['OptimalHumidityMax'], 
                row['OptimalPrecipitationMin'], row['OptimalPrecipitationMax'], 
                row['OptimalSunlightHours'], row['FertilizersRequired'], 
                row['PestsAndDiseases'], row['WateringNeeds'], 
                row['Replant']
            ))
        
        # Commit delle modifiche
        conn.commit()
        print("Tabella popolata con successo.")
    
    except Exception as e:
        print(f"Errore durante il popolamento della tabella: {e}")
    
    finally:
        # Chiusura del cursore e della connessione
        cur.close()
        conn.close()
#Populate Plantings -------------------------------------------------------------------------------------------

# Funzione per generare una data casuale all'interno di una stagione specifica
def generate_date_within_season(season, year):
    season_months = {
        'inverno': [1, 2, 12],  # Dicembre, Gennaio, Febbraio
        'primavera': [3, 4, 5],  # Marzo, Aprile, Maggio
        'estate': [6, 7, 8],     # Giugno, Luglio, Agosto
        'autunno': [9, 10, 11]   # Settembre, Ottobre, Novembre
    }
    
    # Se la stagione non è trovata, ritorna una data casuale
    if season not in season_months:
        return datetime(year, 1, 1) + relativedelta(months=random.randint(0, 11))
    
    month = random.choice(season_months[season])
    day = random.randint(1, 28) 
    return datetime(year, month, day)

# Funzione per popolare la tabella Plantings
def populate_plantings():
   
    conn, cur = connect_to_db()
    
    try:
        # Ottieni i dati necessari da Crops e Farm
        cur.execute("""
            SELECT c.CropID, c.Replant, c.PlantingSeason, c.HarvestSeason, c.GrowthDuration,
                   c.FertilizersRequired
            FROM Crops c
        """)
        crops_data = cur.fetchall()

        # Simula il periodo di 3 anni fa fino ad oggi
        today = datetime.now()
        start_date = today - relativedelta(years=3)

        # Generazione delle note casuali con probabilità 87% di nessun commento
        possible_notes = ['', 'Raccolta abbondante', 'Raccolta scarsa', 'Ottima qualità', 
                          'Problemi con parassiti', 'Buona resa', 'Crescita lenta', 'Qualità media']
        
        # Ciclo sui dati dei raccolti
        for crop in crops_data:
            crop_id, replant, planting_season, harvest_season, growth_duration, fertilizers_required = crop

            # Determina la data di piantagione per 3 anni
            for year in range(start_date.year, today.year + 1):
                # Genera una data di piantagione
                planting_date = generate_date_within_season(planting_season, year)

                # Se la pianta deve essere ripiantata ogni anno
                if replant:
                    # Aggiungi un errore del 15% al GrowthDuration
                    error_days = int(growth_duration * 0.15 * random.uniform(-1, 1))
                    harvest_date = planting_date + timedelta(days=growth_duration + error_days)
                else:
                    # Se la pianta non deve essere ripiantata, mantiene la stessa data
                    planting_date = generate_date_within_season(planting_season, start_date.year)
                    harvest_date = generate_date_within_season(harvest_season, year)

                # Simula AreaDedicated con errore relativo
                area_dedicated = round(random.uniform(0.8, 1.2) * (random.randint(1, 100) % (random.randint(1, 10) + 1)), 2)

                # Seleziona una nota casuale con una probabilità dell'87% di essere vuota
                note = random.choices(possible_notes, weights=[87, 2, 2, 2, 2, 1, 1, 1], k=1)[0]

                # Inserisci i dati nella tabella Plantings
                cur.execute("""
                    INSERT INTO Plantings (
                        CropID, PlantingDate, HarvestDate, AreaDedicated, 
                        FertilizersUsed, Notes
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    crop_id, planting_date, harvest_date, area_dedicated, 
                    fertilizers_required, note
                ))

        
        conn.commit()
        print("Tabella Plantings popolata con successo.")
    
    except Exception as e:
        print(f"Errore durante il popolamento della tabella: {e}")
    
    finally:
        
        cur.close()
        conn.close()

#Populate Costs --------------------------------------------------------

def generate_quarterly_dates(start_year):
    # Genera date per ogni quadrimestre dal 2020 ad oggi
    today = datetime.now()
    dates = []
    for year in range(start_year, today.year + 1):
        for month in [1, 5, 9]:  # Inizio dei quadrimestri (Gennaio, Maggio, Settembre)
            if year == today.year and month > today.month:
                break
            dates.append(datetime(year, month, 1))
    return dates

def generate_realistic_costs(base_value, trend_factor=0.02):
    """
    Funzione che genera costi credibili con una variazione realistica
    trend_factor: incremento medio per riflettere l'inflazione (2% per default)
    """
    # Usa distribuzioni normali per generare variazioni dei costi
    inflation_rate = trend_factor  # Tasso di inflazione standard
    seasonal_variation = np.random.normal(1, 0.05)  # Variazione stagionale

    # Applica una variazione casuale basata sul tasso di inflazione
    adjusted_value = base_value * (1 + inflation_rate) * seasonal_variation
    return round(adjusted_value, 2)

def populate_costs():
    # Connessione al DB
    conn, cursor = connect_to_db()

    # Genera date dal 2020 ad oggi ogni quadrimestre
    dates = generate_quarterly_dates(2020)

    # Valori di base per i costi (approssimativi, basati su valori tipici dell'economia italiana)
    base_water_cost = 1.5  # Euro per metro cubo
    base_energy_cost = 0.25  # Euro per kWh
    base_fertilizer_cost = 35.0  # Euro per quintale

    # Itera su ogni data quadrimestrale e inserisci dati credibili
    for date in dates:
        # Genera costi realistici per ogni quadrimestre
        water_cost = generate_realistic_costs(base_water_cost, trend_factor=0.02)  # Tasso di inflazione 2%
        energy_cost = generate_realistic_costs(base_energy_cost, trend_factor=0.03)  # Tasso di crescita leggermente superiore
        avg_fertilizer_cost = generate_realistic_costs(base_fertilizer_cost, trend_factor=0.04)  # Maggiore volatilità per i fertilizzanti

        # Query di inserimento nel database
        insert_query = """
        INSERT INTO Costs (Date, WaterCost, EnergyCost, AvgFertilizerCost)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (date, water_cost, energy_cost, avg_fertilizer_cost))

    # Commit della transazione e chiusura della connessione
    conn.commit()
    cursor.close()
    conn.close()

    print("Tabella 'Costs' popolata con successo.")


#MAINesecutive-----------------------------------------------------------


def populate_all_tables():
    """Popola tutte le tabelle del database con i dati generati."""
    try:

        employee_data = generate_employee_data(10)  
        insert_data_to_db(employee_data)
        generate_products_table()     
        populate_price_history(csv_path) 
        populate_customer_feedback(60) 
        populate_weather_table()    
        populate_work_hours()   
        insert_farm_data()  
        populate_costs()
        start_date = datetime.now() - timedelta(days= calcola_giorni_da_inizioAnno()) #Da inizio anno
        end_date = datetime.now()
        create_transactions(start_date, end_date)
        create_sales()
        populate_crops_table() 
        populate_plantings()
        
    except Exception as e:
        print(f"Error while populating tables: {e}")
