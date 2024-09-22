# data/queries.py
sales_query = """
    SELECT ProductID, ProductName, StartDate, Price
    FROM PriceHistory
    WHERE StartDate IS NOT NULL
    WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
    ORDER BY ProductID, StartDate;
"""

# Query per estrarre i dati di prezzo nel tempo
price_query = """
    SELECT ProductID, ProductName, StartDate, Price
    FROM PriceHistory
    WHERE StartDate IS NOT NULL
    WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
    ORDER BY ProductID, StartDate;
"""

# Query per estrarre i prezzi massimi e minimi mensili
min_max_query = """
    SELECT 
        ProductID, 
        ProductName, 
        DATE_TRUNC('month', StartDate) AS Month,
        MIN(Price) AS MinPrice,
        MAX(Price) AS MaxPrice
    FROM PriceHistory
    WHERE StartDate IS NOT NULL
    GROUP BY ProductID, ProductName, DATE_TRUNC('month', StartDate)
    ORDER BY ProductID, Month;
"""

# Query per estrarre i dati di prezzo nel tempo
stock_query = """
    SELECT productname, stockquantity
    FROM Products
"""

#-------------------------------------------------------------------
#SEZIONE 1 analisi prodotti -----------------------------

stock_history_price = """
    SELECT productname, startdate, price
    FROM PriceHistory
"""
best_of_query = """
    SELECT p.productname, EXTRACT(YEAR FROM s.date) AS year, EXTRACT(MONTH FROM s.date) AS month, 
           SUM(s.quantity) AS total_sales, 
           COUNT(r.bestproductid) AS total_ratings
    FROM Sales s
    JOIN Products p ON p.productid = s.productid
    JOIN CustomerFeedback r ON p.productid = r.bestproductid
    GROUP BY p.productname, year, month
    ORDER BY p.productname;
"""
#SEZIONE 2 monitoraggio ambientale -----------------------------

weather_query = """
    SELECT date ,temperature , humidity, precipitation, windspeed, solarradiation, soilmoisture
    FROM WeatherConditions
"""

#SEZIONE 3 analisi vendite -----------------------------

quantities_sold = """
    SELECT p.productname, EXTRACT(MONTH FROM s.date) AS month, SUM(s.quantity) AS totalquantity
    FROM Sales s
    JOIN Products p
    ON p.productid = s.productid
    GROUP BY p.productname, month
    ORDER BY month;
"""

payment_methods_used = """
    SELECT t.paymentmethod, EXTRACT(MONTH FROM s.date) AS month, COUNT(s.saleid) AS totaltransactions
    FROM Sales s
    JOIN Transactions t
    ON s.transactionid = t.transactionid
    GROUP BY t.paymentmethod, month
    ORDER BY month;
"""
total_amounts_current_year = """
    SELECT 
        t.date, 
        SUM(t.totalamount) AS total_amount 
    FROM 
        Transactions t
    WHERE 
        EXTRACT(YEAR FROM t.date) = 2024
    GROUP BY 
        t.date
    ORDER BY 
        t.date;
"""
quantity_per_transaction_current_year = """
    SELECT 
        s.date, 
        SUM(s.quantity) AS total_quantity 
    FROM 
        Sales s
    JOIN 
        Transactions t ON s.transactionid = t.transactionid
    WHERE 
        EXTRACT(YEAR FROM s.date) = 2024
    GROUP BY 
        s.date
    ORDER BY 
        s.date;
"""
#Sezione 5 crops e piantagioni ------------------------------------


# Query per ottenere i dati delle colture
crop_details_query = """
    SELECT 
        ScientificName, 
        Description, 
        PlantingSeason, 
        HarvestSeason, 
        GrowthDuration, 
        SoilType, 
        OptimalTemperatureMin, 
        OptimalTemperatureMax, 
        OptimalHumidityMin, 
        OptimalHumidityMax, 
        OptimalPrecipitationMin, 
        OptimalPrecipitationMax, 
        OptimalSunlightHours, 
        FertilizersRequired, 
        PestsAndDiseases, 
        WateringNeeds, 
        Replant 
    FROM Crops 
    WHERE CropName = %s;
"""

# Query per ottenere i dati delle condizioni meteo per l'anno corrente 2024
weather_data_query = """
    SELECT 
        AVG(Temperature) as AvgTemperature, 
        AVG(Humidity) as AvgHumidity, 
        AVG(Precipitation) * %(days)s as AvgPrecipitation,
        AVG(SolarRadiation) as AvgSolarRadiation,
    FROM WeatherConditions 
    WHERE EXTRACT(YEAR FROM Date) = 2024 AND EXTRACT(MONTH FROM Date) = %(month)s;
"""

# Query per ottenere i nomi delle colture
crop_names_query = """
    SELECT DISTINCT CropName FROM Crops;
"""


# Query per ottenere i valori ottimali minimi
optimal_min_query = """
    SELECT 
        OptimalTemperatureMin AS TemperatureMin, 
        OptimalHumidityMin AS HumidityMin, 
        OptimalPrecipitationMin AS PrecipitationMin 
    FROM Crops 
    WHERE CropName = %s;
"""

# Query per ottenere i valori ottimali massimi
optimal_max_query = """
    SELECT 
        OptimalTemperatureMax AS TemperatureMax, 
        OptimalHumidityMax AS HumidityMax, 
        OptimalPrecipitationMax AS PrecipitationMax 
    FROM Crops 
    WHERE CropName = %s;
"""

#Query per ottenere il numero di ore di sole ottimali
optimal_sunlight_query = """
    SELECT 
        OptimalSunlightHours 
    FROM Crops 
    WHERE CropName = %s;
"""

temperature_query = """
    SELECT 
        (SELECT OptimalTemperatureMin 
         FROM Crops) AS mintemp,
        (SELECT OptimalTemperatureMax 
         FROM Crops) AS maxtemp,
        (SELECT AVG(Temperature) 
         FROM WeatherConditions 
         WHERE EXTRACT(YEAR FROM Date) = 2024) AS avgtemperature
"""

# Query per Humidity
humidity_query = """
    SELECT 
        (SELECT OptimalHumidityMin 
         FROM Crops) AS MinHumidity,
        (SELECT OptimalHumidityMax 
         FROM Crops) AS MaxHumidity,
        (SELECT AVG(Humidity) 
         FROM WeatherConditions 
         WHERE EXTRACT(YEAR FROM Date) = 2024) AS AvgHumidity
"""

# Query per Precipitation
precipitation_query = """
    SELECT 
        (SELECT OptimalPrecipitationMin 
         FROM Crops) AS MinPrecipitation,
        (SELECT OptimalPrecipitationMax 
         FROM Crops) AS MaxPrecipitation,
        (SELECT AVG(Precipitation) * 30 
         FROM WeatherConditions 
         WHERE EXTRACT(YEAR FROM Date) = 2024) AS Precipitation
"""

#Sezione 5 costi ------------------------------
# Query per ottenere i costi di acqua, energia e fertilizzanti per un determinato mese
costs_query = """
    SELECT 
        WaterCost AS TotalWaterCost,
        EnergyCost AS TotalEnergyCost,
        AvgFertilizerCost AS TotalFertilizerCost
    FROM Costs
    WHERE EXTRACT(YEAR FROM Date) = %s AND EXTRACT(MONTH FROM Date) = %s;
"""


# Query per ottenere la somma degli stipendi dei dipendenti per un determinato mese
salariescost_query = """
    SELECT 
        SUM(Salary) AS TotalSalaries
    FROM Employees
"""

#Query per ottenere la somma delle precipitazioni per un determinato mese
precipitationcost_query = """
    SELECT 
        SUM(Precipitation) AS MonthlyPrecipitation
    FROM WeatherConditions
    WHERE EXTRACT(YEAR FROM Date) = %s AND EXTRACT(MONTH FROM Date) = %s;
"""


#Sezione 6 --------------------------------