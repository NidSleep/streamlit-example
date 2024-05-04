import streamlit as st
import pandas as pd
from sklearn.cluster import Birch
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt
import mplcursors  # Import mplcursors library

# Title
st.title('Mass Shotting Case''s Casualty Visualization')
st.write("""
### You may adjust the parameter below, lets see how the clustering going

""")

# Sidebar for threshold selection
threshold = st.slider('Threshold', min_value=0.1, max_value=0.5, step=0.1, value=0.1)

# Load the data from the provided URL
url = 'https://raw.githubusercontent.com/NidSleep/streamlit-example/master/dataset_cleansed.csv'
df = pd.read_csv(url)

# Create a copy of the DataFrame to avoid SettingWithCopyWarning
df_coordinates = df[['Longitude', 'Latitude', 'Fatalities', 'Injured', 'Total victims', 'Policeman Killed', 'S#']].copy()

# Drop missing values from the copied DataFrame
df_coordinates.dropna(inplace=True)

# Selecting relevant columns
df_casualty = df_coordinates[['Fatalities', 'Injured', 'Total victims', 'Policeman Killed', 'S#']]  # Include S#

# Calculate silhouette score
birch = Birch(threshold=threshold, n_clusters=None)
cluster_labels = birch.fit_predict(df_casualty.iloc[:, :-1])  # Exclude S# for clustering
silhouette_score_value = silhouette_score(df_casualty.iloc[:, :-1], cluster_labels)

# Plot the clustering results
fig, ax = plt.subplots()
scatter = ax.scatter(df_casualty['Fatalities'], df_casualty['Injured'], c=cluster_labels, cmap='viridis', alpha=0.5)

# Create a dummy scatter plot for colorbar creation
dummy = ax.scatter([], [], c=[], cmap='viridis')
colorbar = plt.colorbar(dummy, ax=ax, label='Cluster')

# Enable mplcursors
mplcursors.cursor(scatter).connect(
    "add",
    lambda sel: sel.annotation.set_text(f'ID: {df_casualty.iloc[sel.target.index]["S#"]}')
)

plt.xlabel('Fatalities')
plt.ylabel('Injured')
plt.title(f'Birch Clustering(Threshold={threshold}, Silhouette Score={silhouette_score_value:.2f})')

st.pyplot(fig)

# Display silhouette score
st.write(f'Silhouette Score: {silhouette_score_value:.2f}')
