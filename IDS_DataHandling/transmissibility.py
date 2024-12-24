import numpy as np
import matplotlib.pyplot as plt

def transmissibility(f, f_n, c, c_c):
    """
    Calculate the transmissibility for a given forcing frequency, natural frequency,
    damping coefficient, and critical damping coefficient.

    Parameters:
    f (float or np.array): Forcing frequency
    f_n (float): Natural frequency
    c (float): Damping coefficient
    c_c (float): Critical damping coefficient

    Returns:
    float or np.array: Transmissibility
    """
    r = f / f_n
    zeta = c / c_c
    numerator = 1 + (2 * r * zeta)**2
    denominator = (1 - r**2)**2 + (2 * r * zeta)**2
    return np.sqrt(numerator / denominator)

# Define the frequency ratio range
f = np.linspace(0.01, 3, 1000)  # Start from 0.01 to avoid division by zero
f_n = 1  # Assume natural frequency is 1 for simplicity

# Define a list of damping ratios (zeta)
zeta_values = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]

# Define the critical damping coefficient (assume it's 1 for simplicity)
c_c = 1

# Plot the transmissibility for each damping ratio
plt.figure(figsize=(10, 6))

for zeta in zeta_values:
    c = zeta * c_c  # Calculate the damping coefficient
    T = transmissibility(f, f_n, c, c_c)
    plt.plot(f / f_n, T, label=f'ζ = {zeta}')

plt.xlabel('Frequency Ratio (f / f_n)')
plt.ylabel('Transmissibility (T)')
plt.yscale('log')  # Set the y-axis to a logarithmic scale
plt.title('Transmissibility vs. Frequency Ratio (Logarithmic Scale)')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()
