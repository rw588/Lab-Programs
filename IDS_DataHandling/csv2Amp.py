import numpy as np
import matplotlib.pyplot as plt

#location of csv file
#file_path = "Data/IDS/840mK.csv"
#file_path = "Data/IDS/coldishNoPulseNoTurbo.csv"
#file_path = "Data/IDS/pulseTubeOFF.csv"
file_path = "/Users/robertwaddy/Downloads/75mKpulseOnNoTurbo.csv"

#load csv file extract data from line 9 onwards
data = np.genfromtxt(file_path, delimiter=';', skip_header=7)

#shape of the data
print(data.shape)

#average displacement
displacement = np.mean(data[:, 1])
print(f"Average displacement: {displacement:.4f}")
amplitudes = data[:, 1] - displacement
#standard deviation
std_dev = np.std(amplitudes)
print(f"Standard Deviation of Displacement: {std_dev:.12f}")

#find differences between each point
differences = np.diff(amplitudes)
print(f"Mean of differences: {np.mean(np.abs(differences)):.12f}")


#plot amplitudes
plt.plot(data[:-1, 0], np.abs(differences))
plt.xlabel('Time / s')
plt.ylabel('Displacement / pm')
plt.title('Displacement of IDS')
plt.show()