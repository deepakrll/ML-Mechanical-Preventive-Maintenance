# Fixing warnings and re-running the corrected version

# Re-import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Try to mount Google Drive (if running in Colab)
try:
    from google.colab import drive
    drive.mount('/content/drive')
    file_path = "/content/drive/My Drive/Colab Notebooks/sensor_data.csv"
    print("Google Drive Mounted!")
except:
    file_path = "sensor_data.csv"  # Local path
    print("Running locally, saving CSV in the current directory.")

# Recreate the synthetic sensor dataset
np.random.seed(42)
num_samples = 1000

timestamps = pd.date_range(start="2025-01-01", periods=num_samples, freq="h")  # Fix: Use lowercase 'h'
temperature = np.random.normal(loc=75, scale=10, size=num_samples)
vibration = np.random.normal(loc=2.0, scale=0.5, size=num_samples)
pressure = np.random.normal(loc=5.5, scale=1.0, size=num_samples)

# Introduce failure cases
temperature[::50] += 15  # Overheating
vibration[::75] += 1.5   # High vibration
pressure[::100] += 2.0   # Excess pressure

# Create DataFrame
df = pd.DataFrame({
    "timestamp": timestamps,
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure
})

# Save dataset to CSV
df.to_csv(file_path, index=False)
print(f" Dataset created and saved to: {file_path}")

# Reload dataset
df = pd.read_csv(file_path, parse_dates=["timestamp"])

# Define failure conditions
df["failure_reason"] = "Normal Operation"
df.loc[df["temperature"] > 85, "failure_reason"] = "Overheated"
df.loc[df["vibration"] > 3.0, "failure_reason"] = "High Vibration"
df.loc[df["pressure"] > 6.5, "failure_reason"] = "Excess Pressure"

# Machines with multiple failure conditions
df.loc[(df["temperature"] > 85) & (df["vibration"] > 3.0), "failure_reason"] = "Overheat & High Vibration"
df.loc[(df["temperature"] > 85) & (df["pressure"] > 6.5), "failure_reason"] = "Overheat & Excess Pressure"
df.loc[(df["vibration"] > 3.0) & (df["pressure"] > 6.5), "failure_reason"] = "Vibration & Excess Pressure"
df.loc[(df["temperature"] > 85) & (df["vibration"] > 3.0) & (df["pressure"] > 6.5), "failure_reason"] = "All Factors"

# Count of failure types
failure_counts = df["failure_reason"].value_counts()

# Display dataset preview with failure reasons
print("\n Sensor Data Preview (with Failure Reasons):")
print(df.head(10))

# Print failure analysis
print("\n Failure Analysis:")
print(failure_counts)

# Visualization: Failure reasons distribution (Fix applied)
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=failure_counts.index, y=failure_counts.values, hue=failure_counts.index, palette="coolwarm", legend=False)

# Annotate values on bars
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.xticks(rotation=45, ha="right", fontsize=12)
plt.title("Machine Failure Reasons & Frequency", fontsize=14, fontweight="bold")
plt.xlabel("Failure Reason", fontsize=12, fontweight="bold")
plt.ylabel("Number of Failures", fontsize=12, fontweight="bold")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()

# Time-Series Trend Analysis for Failures
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["temperature"], label="Temperature (°C)", color="red", alpha=0.7)
plt.plot(df["timestamp"], df["vibration"], label="Vibration (mm/s)", color="blue", alpha=0.7)
plt.plot(df["timestamp"], df["pressure"], label="Pressure (bar)", color="green", alpha=0.7)

# Highlight failure points
failure_points = df[df["failure_reason"] != "Normal Operation"]
plt.scatter(failure_points["timestamp"], failure_points["temperature"], color="red", label="Overheated", s=10)
plt.scatter(failure_points["timestamp"], failure_points["vibration"], color="blue", label="High Vibration", s=10)
plt.scatter(failure_points["timestamp"], failure_points["pressure"], color="green", label="Excess Pressure", s=10)

plt.xlabel("Timestamp", fontsize=12, fontweight="bold")
plt.ylabel("Sensor Values", fontsize=12, fontweight="bold")
plt.title("Sensor Data Trends Over Time", fontsize=14, fontweight="bold")
plt.legend()
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.show()

# Scatter Plot to show correlation between different parameters
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df["temperature"], y=df["vibration"], hue=df["failure_reason"], palette="coolwarm", alpha=0.7)
plt.xlabel("Temperature (°C)", fontsize=12, fontweight="bold")
plt.ylabel("Vibration (mm/s)", fontsize=12, fontweight="bold")
plt.title("Temperature vs. Vibration with Failure Categories", fontsize=14, fontweight="bold")
plt.legend(title="Failure Reason", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(alpha=0.3)
plt.show()
