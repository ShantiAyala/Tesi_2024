# services/data_analysis.py
import numpy as np

from db_handler import fetch_data, fetch_2data

def fetch_data_for_dash(query):
    # Fetch data using the query
    df = fetch_data(query)
    
    # Return the DataFrame for use in Dash
    return df


def fetch_data_for_dash2(query, params):
    df = fetch_2data(query, params)
    return df

#funzioni calcolo costi-----------------------------------------------------
def generate_energy_consumption(area_ha=20, mean_per_ha=7500, std_dev_per_ha=2000):
    """
    Genera un consumo energetico medio annuale per un'azienda agricola in Italia in kWh.
    
    Args:
        area_ha (int): Superficie dell'azienda agricola in ettari. Default 20.
        mean_per_ha (float): Media del consumo energetico per ettaro in kWh. Default 7500.
        std_dev_per_ha (float): Deviazione standard del consumo energetico per ettaro in kWh. Default 2000.
    
    Returns:
        float: Consumo energetico medio annuale in kWh.
    """
    total_mean = mean_per_ha * area_ha
    total_std_dev = std_dev_per_ha * area_ha
    return np.random.normal(total_mean, total_std_dev)

def generate_water_consumption(area_ha=20, mean_per_ha=4500, std_dev_per_ha=1000):
    """
    Genera un consumo idrico medio annuale per un'azienda agricola in Italia in m³.
    
    Args:
        area_ha (int): Superficie dell'azienda agricola in ettari. Default 20.
        mean_per_ha (float): Media del consumo idrico per ettaro in m³. Default 4500.
        std_dev_per_ha (float): Deviazione standard del consumo idrico per ettaro in m³. Default 1000.
    
    Returns:
        float: Consumo idrico medio annuale in m³.
    """
    total_mean = mean_per_ha * area_ha
    total_std_dev = std_dev_per_ha * area_ha
    return np.random.normal(total_mean, total_std_dev)

def generate_pesticide_use(area_ha=20, mean_per_ha=0.35, std_dev_per_ha=0.1):
    """
    Genera un consumo medio annuale di pesticidi per un'azienda agricola in Italia in quintali.
    
    Args:
        area_ha (int): Superficie dell'azienda agricola in ettari. Default 20.
        mean_per_ha (float): Media del consumo di pesticidi per ettaro in quintali. Default 0.35.
        std_dev_per_ha (float): Deviazione standard del consumo di pesticidi per ettaro in quintali. Default 0.1.
    
    Returns:
        float: Consumo di pesticidi medio annuale in quintali.
    """
    total_mean = mean_per_ha * area_ha
    total_std_dev = std_dev_per_ha * area_ha
    return np.random.normal(total_mean, total_std_dev)

def calculate_from_rainfall(rainfall_mm, area_ha=20):
    """
    Calcola il volume d'acqua in metri cubi (m³) a partire dalla quantità di pioggia in millimetri su una data area in ettari.
    
    Args:
        rainfall_mm (float): Quantità di pioggia in millimetri (mm).
        area_ha (float): Area in ettari. Default è 20 ettari.
    
    Returns:
        float: Volume d'acqua in metri cubi (m³).
    """
    # Convertire l'area da ettari a metri quadrati
    area_m2 = area_ha * 10_000  # 1 ettaro = 10,000 m²
    
    # Convertire la quantità di pioggia da millimetri a metri
    if not rainfall_mm:
        return 0

    rainfall_m = rainfall_mm / 1_000  # 1 mm = 0.001 m
    
    # Calcolare il volume d'acqua in metri cubi
    water_volume_m3 = rainfall_m * area_m2
    
    return water_volume_m3


#generate_energy_consumption, generate_water_consumption, generate_pesticide_use, calculate_from_rainfall