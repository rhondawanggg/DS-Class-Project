#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 2024

@author: Shaoxian Wang
DS2500 Intermediate Programming with Data

Appendix: Heatmap of Boston Crime Data in 2020-2024

"""
import pandas as pd
import folium
from folium.plugins import HeatMap

# List of file paths for the crime data CSV files for different years
def load_and_prepare_data():
    file_paths = ["/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2020.csv",
                  "/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2021.csv",
                  "/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2022.csv",
                  "/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2023 to Present.csv"]

# List to store data from all files
    all_data = []

# Load the data from each file
    for file_path in file_paths:
        df = pd.read_csv(file_path, low_memory=False)
        df['OCCURRED_ON_DATE'] = pd.to_datetime(df['OCCURRED_ON_DATE'], errors='coerce')
        df = df.dropna(subset=['Lat', 'Long'])
        df = df[(df['Lat'] != 0) & (df['Long'] != 0)]
        df['YEAR'] = df['OCCURRED_ON_DATE'].dt.year
        boston_crime_data = df[df['YEAR'].isin([2020, 2021, 2022, 2023, 2024])]
        all_data.append(boston_crime_data)
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data

# Initialize a folium map centered at Boston
def create_heatmap(boston_crime_data):
    m = folium.Map(location=[42.3601, -71.0589], zoom_start=12)
    coordinates = boston_crime_data[['Lat', 'Long']].values.tolist()
    HeatMap(coordinates).add_to(m)
    heatmap_file_path = '/Users/wsx/Desktop/ds 2500 project/boston_crime_heatmap.html'  
    m.save(heatmap_file_path)
    return heatmap_file_path

# Load the data and create a heatmap
boston_crime_data = load_and_prepare_data()
heatmap_file_path = create_heatmap(boston_crime_data)
print("Heatmap created and saved at:", heatmap_file_path)