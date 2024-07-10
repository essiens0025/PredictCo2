import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_squared_error, r2_score


model = joblib.load('modelXG.pkl')

st.title("Prédiction des émissions de CO2")

data_2017 = pd.read_csv('2017_Building_Energy_Benchmarking.csv')

# Afficher les données de 2017
st.header("Données de 2017")
st.write(data_2017)

# Faire des prédictions sur les données de 2017
if st.button('Prédire les émissions de CO2 pour les données de 2017'):
    predictions = model.predict(data_2017)
    predictions_exp = np.exp(predictions)
    data_2017['Prédiction CO2 (g/km)'] = predictions_exp
    st.write(data_2017)

# Interface utilisateur pour entrer manuellement les données et obtenir une prédiction
st.header("Prédiction manuelle des émissions de CO2")

building_types = [
    'NonResidential', 'Nonresidential COS', 'Multifamily MR (5-9)',
    'SPS-District K-12', 'Campus', 'Multifamily LR (1-4)',
    'Multifamily HR (10+)', 'Nonresidential WA'
]

# Options pour PrimaryPropertyType
primary_property_types = [
    'Hotel', 'Other', 'Mid-Rise Multifamily', 'Mixed Use Property', 'K-12 School',
    'University', 'Small- and Mid-Sized Office', 'Self-Storage Facility',
    'Warehouse', 'Large Office', 'Senior Care Community', 'Medical Office',
    'Retail Store', 'Hospital', 'Residence Hall', 'Distribution Center',
    'Worship Facility', 'Low-Rise Multifamily', 'Supermarket / Grocery Store',
    'Laboratory', 'Refrigerated Warehouse', 'Restaurant',
    'High-Rise Multifamily', 'Office'
]

LargestPropertyUseType = [
    'Hotel', 'Police Station', 'Other - Entertainment/Public Assembly',
    'Multifamily Housing', 'Library', 'Fitness Center/Health Club/Gym',
    'Social/Meeting Hall', 'Courthouse', 'Other', 'K-12 School',
    'College/University', 'Automobile Dealership', 'Office',
    'Self-Storage Facility', 'Non-Refrigerated Warehouse', 'Other - Mall',
    'Senior Care Community', 'Medical Office' ,'Retail Store',
    'Hospital (General Medical & Surgical)', 'Museum',
    'Repair Services (Vehicle, Shoe, Locksmith, etc)',
    'Other - Lodging/Residential', 'Residence Hall/Dormitory',
    'Other/Specialty Hospital', 'Financial Office' 'Distribution Center',
    'Parking' 'Worship Facility', 'Restaurant' 'Data Center', 'Laboratory',
    'Supermarket/Grocery Store', 'Urgent Care/Clinic/Other Outpatient',
    'Other - Services', 'Strip Mall', 'Wholesale Club/Supercenter',
    'Refrigerated Warehouse', 'Manufacturing/Industrial Plant',
    'Other - Recreation', 'Lifestyle Center', 'Other - Public Services',
    'Other - Education', 'Fire Station', 'Performing Arts',
    'Residential Care Facility', 'Bank Branch', 'Other - Restaurant/Bar',
    'Food Service', 'Adult Education', 'Other - Utility', 'Movie Theater',
    'Personal Services (Health/Beauty, Dry Cleaning, etc)',
    'Pre-school/Daycare', 'Prison/Incarceration'
]

neighborhoods = [
    'DOWNTOWN', 'SOUTHEAST', 'NORTHEAST', 'EAST', 'Central', 'NORTH',
    'MAGNOLIA / QUEEN ANNE', 'LAKE UNION', 'GREATER DUWAMISH', 'BALLARD',
    'NORTHWEST', 'CENTRAL', 'SOUTHWEST', 'DELRIDGE', 'Ballard', 'North', 'Delridge',
    'Northwest', 'DELRIDGE NEIGHBORHOODS'
]

# Sélecteurs pour BuildingType et PrimaryPropertyType
building_type = st.selectbox('Type de bâtiment', building_types)
primary_property_type = st.selectbox('Type de propriété principale', primary_property_types)
neighborhood = st.selectbox('Quartier', neighborhoods)
LargestPropertyUseType = st.selectbox('Utilisation principal de la propriété', LargestPropertyUseType)
property_gfa_total = st.number_input('Surface totale de la propriété (en pieds carrés)', min_value=0, value=1000)
energy_star_score = st.number_input('ENERGYSTAR Score', min_value=0, max_value=100, value=50)
number_of_floors = st.number_input('Nombre d\'étages', min_value=1, value=1)
number_of_buildings = st.number_input('Nombre de bâtiments', min_value=1, value=1)
year_built = st.number_input('Année de construction', min_value=1800, max_value=2024, value=2000)


input_data = pd.DataFrame({
    'BuildingType': [building_type],
    'PrimaryPropertyType': [primary_property_type],
    'Neighborhood': [neighborhood],
    'LargestPropertyUseType': [LargestPropertyUseType],
    'PropertyGFATotal': [property_gfa_total],
    'ENERGYSTARScore': [energy_star_score],
    'NumberofFloors': [number_of_floors],
    'NumberofBuildings': [number_of_buildings],
    'YearBuilt': [year_built]
})

if st.button('Prédire les émissions de CO2 pour les données saisies'):
    prediction = model.predict(input_data)
    prediction_exp = np.exp(prediction)
    st.write(f"Les émissions de CO2 prévues sont : {prediction_exp[0]:.2f} g/km")
