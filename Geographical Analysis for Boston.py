#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 9 2024

@author: Shaoxian Wang
DS2500 Intermediate Programming with Data

### Geographical Distribution and Public Safety Analysis for Boston

Part 1: Crime Hotspots and Coldspots in Boston (2020-2024)
Visualize crime hotspots and coldspots in Boston, showing areas with high crime intensity (red) and lower intensity (blue). 

Part 2: Crime Density and Geographic Influence in Boston (2020-2024)
Display overall crime density across Boston neighborhoods. Analyze how geographic factors like proximity to economic centers or public facilities influence crime rates.

"""
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd 

def load_boston_crime_data():
    """Loads and processes Boston crime data from CSV files for the years 2020-2024."""
    boston_paths = ["/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2020.csv",
                    "/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2021.csv",
                    "/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2022.csv",
                    "/Users/wsx/Desktop/ds 2500 project/Crime Incident Reports - 2023 to Present.csv"]
    all_data = []
# Iterate over each file path in the list of Boston crime data files
    for path in boston_paths:
        df = pd.read_csv(path, low_memory=False)
        df['OCCURRED_ON_DATE'] = pd.to_datetime(df['OCCURRED_ON_DATE'].str.replace(r'\+00$', '', regex=True), errors='coerce')
        df = df.dropna(subset=['Lat', 'Long'])
        df = df[(df['Lat'] != 0) & (df['Long'] != 0)]
        df['year'] = df['OCCURRED_ON_DATE'].dt.year
        all_data.append(df)
# Combine all the data into a single DataFrame
    boston_crime_data = pd.concat(all_data, ignore_index=True)
    boston_crime_data = boston_crime_data[boston_crime_data['year'].isin([2020, 2021, 2022, 2023, 2024])]
# Load the shapefile for Boston
    boston_map = gpd.read_file("/Users/wsx/Desktop/ds 2500 project/ne_110m_admin_1_states_provinces.shp")
    return boston_crime_data, boston_map

##### Part 1: Crime Hotspots and Coldspots in Boston (2020-2024)
def plot_boston_crime_hotspots(boston_crime_data, boston_map):
    """Plots crime hotspots on a map of Boston using a scatterplot and annotates top crime streets."""
# Set the scatter plot
    fig, ax = plt.subplots(figsize=(8, 8))
    boston_map.plot(ax=ax, color='white', edgecolor='black')
    sns.scatterplot(x='Long', y='Lat', data=boston_crime_data, color='red', s=2, ax=ax)
# Group by STREET to find the top crime locations
    top_streets = boston_crime_data['STREET'].value_counts().head(5).index.tolist()
    top_street_data = boston_crime_data[boston_crime_data['STREET'].isin(top_streets)]
# Annotate the top areas on the map
    for street in top_streets:
        street_data = top_street_data[top_street_data['STREET'] == street]
        x_median = street_data['Long'].median()
        y_median = street_data['Lat'].median()
        ax.text(x_median, y_median, street, fontsize=10, ha='center', color='black', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    ax.set_title('Crime Hotspots in Boston (2020-2024)')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_xlim(-71.15, -71.00)
    ax.set_ylim(42.24, 42.40)
    ax.grid(True)
    plt.show()

def plot_boston_crime_coldspots(boston_crime_data, boston_map):
    """Plots a hexbin plot to visualize areas of lower crime density (coldspots) in Boston on the map."""
# Set the hexbin plot
    fig, ax = plt.subplots(figsize=(10, 8))
    boston_map.plot(ax=ax, color='white', edgecolor='black')
    hb = ax.hexbin(boston_crime_data['Long'], boston_crime_data['Lat'], gridsize=50, cmap='Blues', mincnt=1, edgecolors='none')
    plt.colorbar(hb, ax=ax, label='Crime Count')
# Group by STREET to find the top crime locations
    lowest_streets = boston_crime_data['STREET'].value_counts().tail(5).index.tolist()
    lowest_street_data = boston_crime_data[boston_crime_data['STREET'].isin(lowest_streets)]
# Annotate the top areas on the map
    for street in lowest_streets:
        street_data = lowest_street_data[lowest_street_data['STREET'] == street]
        x_median = street_data['Long'].median()
        y_median = street_data['Lat'].median()
        ax.text(x_median, y_median, street, fontsize=10, ha='center', color='black', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    ax.set_title('Crime Coldspots in Boston (2020-2024)')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_xlim(-71.15, -71.00)
    ax.set_ylim(42.24, 42.40)
    ax.grid(True)
    plt.show()

##### Part 2:Crime Density and Geographic Influence in Boston (2020-2024)
def plot_crime_density_and_geographic_influence(boston_crime_data):
    """Analyzes geographic influences on crime rates using a pair plot."""
# Add a column for the distance from downtown Boston
    boston_crime_data['DISTANCE_TO_DOWNTOWN'] = (((boston_crime_data['Lat'] - 42.3601)**2 + (boston_crime_data['Long'] + 71.0589)**2) ** 0.5)
# Categorize data into proximity groups: Close (0-0.02), Medium (0.02-0.05), Far (>0.05)
    boston_crime_data['PROXIMITY_CATEGORY'] = pd.cut(boston_crime_data['DISTANCE_TO_DOWNTOWN'], bins=[0, 0.02, 0.05, float('inf')], labels=['Close', 'Medium', 'Far'])
# Set Pair Plot
    sns.pairplot(boston_crime_data[['DISTANCE_TO_DOWNTOWN', 'SHOOTING', 'PROXIMITY_CATEGORY']], hue='PROXIMITY_CATEGORY', palette='Set2', diag_kind="kde", kind="scatter")
    plt.suptitle('Pair Plot of Geographic Influence on Crime Involving Shotting in Boston (2020-2024)', y=1.02)
    plt.show()

# Load the Boston data and visualize
boston_crime_data, boston_map = load_boston_crime_data()
plot_boston_crime_hotspots(boston_crime_data, boston_map)
plot_boston_crime_coldspots(boston_crime_data, boston_map)
plot_crime_density_and_geographic_influence(boston_crime_data)



