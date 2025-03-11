from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import random

# Define file path in Google Drive
file_path = "/content/drive/My Drive/Colab Notebooks/sensor_data.csv"

# Increase dataset size: 10 machines, 5000 timestamps (~7 months data at hourly intervals)
timestamps = pd.date_range(start="2023-06-01", periods=5000, freq="H")
machine_ids = [f"Machine_{i}" for i in range(1, 11)]

# Generate new data with more variety
data = []
for timestamp in timestamps:
    for machine in machine_ids:
        temperature = round(np.random.normal(loc=75, scale=5), 2)
        vibration = round(np.random.normal(loc=1.2, scale=0.3), 2)
        pressure = round(np.random.normal(loc=5, scale=0.5), 2)

        # Introduce occasional failures (5% chance)
        failure = 0
        if random.random() < 0.05:  
            temperature += random.uniform(5, 15)
            vibration += random.uniform(1, 2)
            failure = 1

        data.append([timestamp, machine, temperature, vibration, pressure, failure])

# Create DataFrame
df_large = pd.DataFrame(data, columns=["timestamp", "machine_id", "temperature", "vibration", "pressure", "failure"])

# Save to CSV in Google Drive
df_large.to_csv(file_path, index=False)

# Print confirmation message and first few rows
print(f"Dataset saved to {file_path}")
df_large.head(10)

