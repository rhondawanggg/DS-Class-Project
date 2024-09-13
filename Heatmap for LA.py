#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 2024

@author: Shaoxian Wang
DS2500 Intermediate Programming with Data

Appendix: Heatmap of LA Crime Data in 2020-2024

"""
import pandas as pd
import folium
from folium.plugins import HeatMap

def load_and_prepare_data():
# Path for the LA crime data CSV file
    file_path = "/Users/wsx/Desktop/ds 2500 project/LA Crime Incident Reports 2020-2024.csv"# Load the data
    df = pd.read_csv(file_path, low_memory=False)
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    
# Drop rows with missing or zero values in latitude and longitude
    df = df.dropna(subset=['LAT', 'LON'])
    df = df[(df['LAT'] != 0) & (df['LON'] != 0)]
    
# Extract the year from the date and filter for the years 2020 to 2024
    df['YEAR'] = df['DATE OCC'].dt.year
    la_crime_data = df[df['YEAR'].isin([2020, 2021, 2022, 2023, 2024])]

    return la_crime_data

def create_heatmap(la_crime_data):
# Initialize a folium map centered at Los Angeles
    m = folium.Map(location=[34.05, -118.25], zoom_start=10)
    
# Create a list of lists for the heatmap: [[lat, lon], [lat, lon], ...]
    coordinates = la_crime_data[['LAT', 'LON']].values.tolist()
    
# Add a heatmap to the map
    HeatMap(coordinates).add_to(m)
    
# Save the heatmap to an HTML file
    heatmap_file_path = '/Users/wsx/Desktop/ds 2500 project/la_crime_heatmap.html'
    m.save(heatmap_file_path)
    
    return heatmap_file_path

# Load the data and create a heatmap
la_crime_data = load_and_prepare_data()
heatmap_file_path = create_heatmap(la_crime_data)
print("Heatmap created and saved at:", heatmap_file_path)


