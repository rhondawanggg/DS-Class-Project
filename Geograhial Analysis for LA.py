#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 2024

@author: Shaoxian Wang
DS2500 Intermediate Programming with Data

### Geographical Distribution and Public Safety Analysis for Los Angeles

Part 1: Crime Hotspots in Los Angeles (2020-2024)
Visualize crime hotspots in Los Angeles, highlighting high crime intensity areas (red) and lower intensity areas (blue).

Part 2: Crime Density and Geographic Influence in Los Angeles (2020-2024)
Show crime density in different neighborhoods in Los Angeles and examine the impact of geographic factors on crime rates.

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import numpy as np

def load_la_crime_data():
    """Loads and processes LA crime data from the provided CSV file for the years 2020-2024."""
    la_path = "/Users/wsx/Desktop/ds 2500 project/LA Crime Incident Reports 2020-2024.csv"
    df = pd.read_csv(la_path, low_memory=False)
# Convert the date column to datetime, assuming the format "MM/DD/YYYY HH:MM:SS AM/PM"
    df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
# Drop rows with missing or zero values in latitude and longitude
    df = df.dropna(subset=['LAT', 'LON'])
    df = df[(df['LAT'] != 0) & (df['LON'] != 0)]
# Extract the year from the date and filter for the years 2020 to 2024
    df['YEAR'] = df['DATE OCC'].dt.year
    la_crime_data = df[df['YEAR'].isin([2020, 2021, 2022, 2023, 2024])]
# Load a shapefile for Los Angeles (replace with your own shapefile path)
    la_map = gpd.read_file("/Users/wsx/Desktop/ds 2500 project/ne_110m_admin_1_states_provinces.shp")
    
    return la_crime_data, la_map

##### Part 1: Crime Hotspots in Los Angeles (2020-2024)
def plot_la_crime_hotspots(la_crime_data, la_map):
    """Plots crime hotspots in Los Angeles using a scatter plot."""
    fig, ax = plt.subplots(figsize=(8, 8))
# Plot the LA map without borders
    la_map.plot(ax=ax, color='white', edgecolor='none')
# Scatter plot for crime locations
    sns.scatterplot(x='LON', y='LAT', data=la_crime_data, color='red', s=2, ax=ax)
# Annotate the top areas on the map
    top_areas = la_crime_data['AREA NAME'].value_counts().head(5).index.tolist()
    top_area_data = la_crime_data[la_crime_data['AREA NAME'].isin(top_areas)]
    for area in top_areas:
        area_data = top_area_data[top_area_data['AREA NAME'] == area]
        x_median = area_data['LON'].median()
        y_median = area_data['LAT'].median()
        ax.text(x_median, y_median, area, fontsize=10, ha='center', color='black', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
# Calculate dynamic limits with a small buffer and round to two decimal places
    x_min = round(la_crime_data['LON'].min() - 0.01, 2)
    x_max = round(la_crime_data['LON'].max() + 0.01, 2)
    y_min = round(la_crime_data['LAT'].min() - 0.01, 2)
    y_max = round(la_crime_data['LAT'].max() + 0.01, 2)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
# Set the x-axis and y-axis ticks with a difference of 0.02
    y_ticks = np.arange(y_min, y_max + 0.02, 0.02)
    ax.set_yticks(y_ticks)
# Set the title and labels for the plot
    ax.set_title('Crime Hotspots in Los Angeles (2020-2024)')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True)
    plt.show()

def plot_la_crime_coldspots(la_crime_data, la_map):
    """Plots a hexbin plot to visualize areas of lower crime density (coldspots) in Los Angeles on the map."""
    fig, ax = plt.subplots(figsize=(8, 8))
# Plot the LA map without borders
    la_map.plot(ax=ax, color='white', edgecolor='none')
# Hexbin plot for visualizing coldspots
    hb = ax.hexbin(la_crime_data['LON'], la_crime_data['LAT'], gridsize=60, cmap='Blues', mincnt=1, edgecolors='none')
    plt.colorbar(hb, ax=ax, label='Crime Count')
# Annotate the lowest areas on the map
    lowest_areas = la_crime_data['AREA NAME'].value_counts().tail(5).index.tolist()
    lowest_area_data = la_crime_data[la_crime_data['AREA NAME'].isin(lowest_areas)]
    for area in lowest_areas:
        area_data = lowest_area_data[lowest_area_data['AREA NAME'] == area]
        x_median = area_data['LON'].median()
        y_median = area_data['LAT'].median()
        ax.text(x_median, y_median, area, fontsize=10, ha='center', color='black', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
# Calculate dynamic limits with a small buffer and round to two decimal places
    x_min = round(la_crime_data['LON'].min() - 0.01, 2)
    x_max = round(la_crime_data['LON'].max() + 0.01, 2)
    y_min = round(la_crime_data['LAT'].min() - 0.01, 2)
    y_max = round(la_crime_data['LAT'].max() + 0.01, 2)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
# Set the x-axis and y-axis ticks with a difference of 0.02
    y_ticks = np.arange(y_min, y_max + 0.02, 0.02)
    ax.set_yticks(y_ticks)
# Set the title and labels for the plot
    ax.set_title('Crime Coldspots in Los Angeles (2020-2024)')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.grid(True)
    plt.show()

##### Part 2: Crime Density and Geographic Influence in Los Angeles (2020-2024)
def plot_crime_density_and_geographic_influence(la_crime_data):
    """Analyzes geographic influences on crime rates using a pair plot based on weapon usage."""
# Assume downtown LA coordinates for distance calculation (you may need to adjust these)
    la_crime_data['Distance to Downtown'] = (((la_crime_data['LAT'] - 34.0522)**2 + (la_crime_data['LON'] + 118.2437)**2) ** 0.5)
# Categorize data into proximity groups: Close (0-0.02), Medium (0.02-0.05), Far (>0.05)
    la_crime_data['Proximity Category'] = pd.cut(la_crime_data['Distance to Downtown'], 
                                                 bins=[0, 0.02, 0.05, float('inf')], 
                                                 labels=['Close', 'Medium', 'Far'])
# Filter data to include only incidents where a weapon was used
    weapon_data = la_crime_data.dropna(subset=['Weapon Used Cd'])
    
# Create a pair plot based on the proximity to downtown and weapon usage
    sns.pairplot(weapon_data[['Distance to Downtown', 'Weapon Used Cd', 'Proximity Category']],
                 hue='Proximity Category', palette='Set2', diag_kind="kde", kind="scatter")
# Set the title for the pair plot
    plt.suptitle('Pair Plot of Geographic Influence on Crime Involving Weapons in LA (2020-2024)', y=1.02)
    plt.show()

# Load the LA data and visualize
la_crime_data, la_map = load_la_crime_data()
plot_la_crime_hotspots(la_crime_data, la_map)
plot_la_crime_coldspots(la_crime_data, la_map)
plot_crime_density_and_geographic_influence(la_crime_data)


