/*Per modificare qualcosa nelle tabelle sottostanti, manutenzione del codice*/

SELECT tablename
FROM pg_tables
WHERE schemaname = 'public';

DO $$ 
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || r.tablename || ' CASCADE';
    END LOOP;
END $$;


/*Struttura tabelle db farm_db*/

CREATE TABLE IF NOT EXISTS Products (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(50),
    Category VARCHAR(50),
    Price DECIMAL(10, 2),
    StockQuantity INT
    --ReorderLeveL
);

 CREATE TABLE IF NOT EXISTS PriceHistory (
    PriceHistoryID SERIAL PRIMARY KEY ,
    ProductID INT,
    ProductName VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    Price DECIMAL(10, 2),
    Discontinued BOOLEAN,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE IF NOT EXISTS CustomerFeedback (
    FeedbackID SERIAL PRIMARY KEY ,
    Date DATE,
    Rating INT,
    Comment TEXT,
    BestProductID INT,
    CostumerName VARCHAR(50),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

 CREATE TABLE IF NOT EXISTS Employees (
    EmployeeID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    City VARCHAR(50),
    State VARCHAR(50),
    ZipCode VARCHAR(10),
    Country VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    HireDate DATE,
    JobTitle VARCHAR(100),
    Salary DECIMAL(10, 2),
    EmploymentStatus VARCHAR(50),
    --SSN VARCHAR(20),
    EmergencyContact VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS WeatherConditions (
    WeatherID SERIAL PRIMARY KEY,
    --FarmID INT, da aggiungere nel caso si avessero più sedi
    Date DATE,
    Temperature DECIMAL(5, 2),
    Humidity DECIMAL(5, 2),
    Precipitation DECIMAL(5, 2),
    WindSpeed DECIMAL(5, 2),
    SolarRadiation DECIMAL(5, 2),
    SoilMoisture DECIMAL(5, 2),
    WeatherDescription VARCHAR(100)
    --FOREIGN KEY (FarmID) REFERENCES Farm(FarmID)
);

CREATE TABLE IF NOT EXISTS Transactions (
    TransactionID SERIAL PRIMARY KEY ,
    Date DATE,
    TotalAmount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    TransactionStatus VARCHAR(50)
);

 CREATE TABLE IF NOT EXISTS Sales (
    SaleID SERIAL PRIMARY KEY ,
    Date DATE,
    ProductID INT,
    TransactionID INT,
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    TotalPrice DECIMAL(10, 2),
    Discount DECIMAL(5, 2),
    SalesChannel VARCHAR(50),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (TransactionID ) REFERENCES Transactions(TransactionID )
);


 CREATE TABLE IF NOT EXISTS WorkHours (
    WorkHourID SERIAL PRIMARY KEY,
    EmployeeID INT,
    Date DATE,
    HoursWorked DECIMAL(5, 2),
    OvertimeHours DECIMAL(5, 2),
    WorkType VARCHAR(50),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

 CREATE TABLE IF NOT EXISTS Farm (
    --FarmID SERIAL PRIMARY KEY,
    FarmName VARCHAR(100),
    OwnerName VARCHAR(100),
    EstablishedDate DATE,
    Location VARCHAR(255),
    TotalArea DECIMAL(10, 2),
    CultivatedArea DECIMAL(10, 2),
    NumberOfEmployees INT,
    ContactEmail VARCHAR(100),
    ContactPhone VARCHAR(20),
    FarmType VARCHAR(50),
    Certifications TEXT,
    --AnnualRevenue DECIMAL(15, 2),
    PrimaryCrops TEXT,
    Machinery TEXT,
    SoilType VARCHAR(50),
    ClimateZone VARCHAR(50)
    --AnnualProductionVolume DECIMAL(15, 2),
);

 CREATE TABLE IF NOT EXISTS Crops (
    CropID SERIAL PRIMARY KEY,
    CropName VARCHAR(100),
    ScientificName VARCHAR(100),
    Description TEXT,
    PlantingSeason VARCHAR(50),
    HarvestSeason VARCHAR(50),
    GrowthDuration INT, -- durata in giorni
    SoilType VARCHAR(50),
    OptimalTemperatureMin DECIMAL(5, 2),
    OptimalTemperatureMax DECIMAL(5, 2),
    OptimalHumidityMin DECIMAL(5, 2),
    OptimalHumidityMax DECIMAL(5, 2),
    OptimalPrecipitationMin DECIMAL(5, 2),
    OptimalPrecipitationMax DECIMAL(5, 2),
    OptimalSunlightHours DECIMAL(5, 2),
    FertilizersRequired TEXT,
    PestsAndDiseases TEXT,
    WateringNeeds TEXT,
    Replant BOOLEAN
);

 CREATE TABLE IF NOT EXISTS Plantings (
    PlantingID SERIAL PRIMARY KEY,
    CropID INT,
    --FarmID INT,
    PlantingDate DATE,
    HarvestDate DATE,
    AreaDedicated DECIMAL(10, 2),
    FertilizersUsed TEXT,
    Notes TEXT,
    FOREIGN KEY (CropID) REFERENCES Crops(CropID)
    --FOREIGN KEY (FarmID) REFERENCES Farm(FarmID)
);

CREATE TABLE IF NOT EXISTS Costs (
    CostsID SERIAL PRIMARY KEY,     
    Date DATE NOT NULL,             
    WaterCost DECIMAL(10, 2),       
    EnergyCost DECIMAL(10, 2),      
    AvgFertilizerCost DECIMAL(10, 2) 
);