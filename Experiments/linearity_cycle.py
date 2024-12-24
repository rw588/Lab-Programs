import numpy as np
import matplotlib.pyplot as plt

# Load the data from CSV file
path = '/Users/robertwaddy/Nextcloud/raidyMcRaiderson/Code/Lab-Data/CLSZ1/Hysteresis/Cold/-30_26x10/changealso.csv'
data = np.genfromtxt(path, delimiter=',', skip_header=1)

# Check the shape of the data
print(data.shape)  # Should be (3, 160)

# Reshape the data to organize it into sweeps
# Each sweep has 16 points (columns) and 3 rows (voltage, displacement, error)
num_sweeps = 10
points_per_sweep = 16

# Extract the voltage values (first row, repeated across sweeps)
voltages = data[0, :points_per_sweep]  # Taking the first 16 voltage points

# Initialize lists to store displacement and error data
datarampup = np.zeros((num_sweeps, points_per_sweep))
stdrampup = np.zeros((num_sweeps, points_per_sweep))

# Loop through each sweep to populate the data arrays
for i in range(num_sweeps):
    start_index = i * points_per_sweep
    datarampup[i, :] = data[1, start_index:start_index + points_per_sweep]  # Displacement
    stdrampup[i, :] = data[2, start_index:start_index + points_per_sweep]  # Error

# Plot each sweep with error bars for ramp up
plt.figure(figsize=(10, 6))

# Plotting the 10 sweeps (ramp up)
for i in range(num_sweeps):
    plt.errorbar(voltages, datarampup[i, :], yerr=stdrampup[i, :], fmt='-o', label=f'Ramp Up Sweep {i+1}', alpha=0.5)

plt.xlabel('Voltage (V)')
plt.ylabel('Displacement')
plt.title('Voltage vs Displacement with Error Bars for 10 Sweeps (16 Points per Sweep)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Calculate and plot mean and standard deviation for each voltage step
mean_rampup = np.mean(datarampup, axis=0)
std_rampup = np.std(datarampup, axis=0)

plt.figure(figsize=(10, 6))

# Mean plot for ramp up
plt.errorbar(voltages, mean_rampup, yerr=std_rampup, fmt='-o', label='Mean Ramp Up', color='blue', capsize=5)

plt.xlabel('Voltage (V)')
plt.ylabel('Mean Displacement with Standard Deviation')
plt.title('Mean and Standard Deviation of Displacement over 10 Sweeps (16 Points per Sweep)')
plt.legend()
plt.tight_layout()
plt.show()

# Optional: Calculate and print the Coefficient of Variation (CV)
cv_rampup = std_rampup / mean_rampup
print("Coefficient of Variation (CV) for Ramp Up:", cv_rampup)
print("Standard Deviation of CV for Ramp Up:", std_rampup)
print("Mean of std for Ramp Up:", np.mean(std_rampup))
