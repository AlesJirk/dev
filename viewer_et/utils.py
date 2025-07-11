# utils.py
import pandas as pd
import numpy as np
import geopandas
from datetime import date

# --- ALL SHARED CONSTANTS ---
CODE_A2_TO_A3 = {
    'AT': 'AUT', 'BE': 'BEL', 'BG': 'BGR', 'HR': 'HRV', 'CY': 'CYP', 'CZ': 'CZE',
    'DK': 'DNK', 'EE': 'EST', 'FI': 'FIN', 'FR': 'FRA', 'DE': 'DEU', 'GR': 'GRC',
    'HU': 'HUN', 'IE': 'IRL', 'IT': 'ITA', 'LV': 'LVA', 'LT': 'LTU', 'LU': 'LUX',
    'MT': 'MLT', 'NL': 'NLD', 'PL': 'POL', 'PT': 'PRT', 'RO': 'ROU', 'SK': 'SVK',
    'SI': 'SVN', 'ES': 'ESP', 'SE': 'SWE', 'GB': 'GBR', 'NO': 'NOR', 'CH': 'CHE'
}
CODE_A3_TO_A2 = {v: k for k, v in CODE_A2_TO_A3.items()}
COUNTRY_NAMES = {
    'AUT': 'Austria', 'BEL': 'Belgium', 'BGR': 'Bulgaria', 'HRV': 'Croatia', 'CYP': 'Cyprus',
    'CZE': 'Czechia', 'DNK': 'Denmark', 'EST': 'Estonia', 'FIN': 'Finland', 'FRA': 'France',
    'DEU': 'Germany', 'GRC': 'Greece', 'HUN': 'Hungary', 'IRL': 'Ireland', 'ITA': 'Italy',
    'LVA': 'Latvia', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'MLT': 'Malta', 'NLD': 'Netherlands',
    'POL': 'Poland', 'PRT': 'Portugal', 'ROU': 'Romania', 'SVK': 'Slovakia', 'SVN': 'Slovenia',
    'ESP': 'Spain', 'SWE': 'Sweden', 'GBR': 'United Kingdom', 'NOR': 'Norway', 'CHE': 'Switzerland'
}
DEFAULT_SELECTION_A2 = ['DE', 'FR', 'ES', 'HU', 'GB', 'IT']


# --- ALL SHARED DATA FUNCTIONS ---
def generate_spot_data(start_date: date, end_date: date, countries_a2: list) -> pd.DataFrame:
    """Generates random hourly spot price data for a given date range and countries."""
    all_dfs = []
    if start_date > end_date:
        return pd.DataFrame()
    for day in pd.date_range(start=start_date, end=end_date, freq='D'):
        timestamps = pd.to_datetime(pd.date_range(start=day, periods=24, freq='h'))
        for country_a2 in countries_a2:
            base_price = np.random.uniform(20, 60); volatility = np.random.uniform(0.3, 0.8)
            peak_factor = np.random.uniform(1.5, 2.5); x = np.linspace(0, 2 * np.pi, 24)
            price_shape = peak_factor - np.sin(x - np.pi / 4)
            prices = np.maximum(0, base_price * price_shape + np.random.normal(0, base_price * volatility * 0.1, 24))
            all_dfs.append(pd.DataFrame({'timestamp': timestamps, 'country_code': country_a2, 'value': prices}))
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

def get_europe_geodata():
    try:
        url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
        world = geopandas.read_file(url)
        european_codes_a3 = list(CODE_A3_TO_A2.keys())
        europe = world[world['id'].isin(european_codes_a3)].copy()
        europe['iso_a2'] = europe['id'].map(CODE_A3_TO_A2)
        return europe[['id', 'iso_a2', 'geometry']]
    except Exception as e:
        print(f"Error loading geodata: {e}") # Use print for backend errors
        return None