import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#import data from csv file and plot
path = '/Users/robertwaddy/Nextcloud/raidyMcRaiderson/Code/Lab-Data/CLSZ1/Hysteresis/Cold/-30_26x10/changealso.csv'
data = np.genfromtxt(path, delimiter=',', skip_header=1)
#data order: voltages,datarampup,stdrampup,reversedvoltages,datarampdown,stdrampdown
#voltages = data[0,:], datarampup = data[1,:], stdrampup = data[2,:]

print(data)
print(data[0,:])
#plot with error bars
plt.plot(data[0,:], data[1,:], '+', label='Data')
plt.errorbar(data[0,:], data[1,:], yerr=np.sqrt(data[2,:]**2 + 7000**2), fmt='none', label='Error')
#x error bar at 2mV
plt.errorbar(data[0,:], data[1,:], xerr=0.002, fmt='none', label='Error')

#create a linear fit for data with error bars
m, c = np.polyfit(data[0, :], data[1, :], 1, cov=False)  # Fit the data
p_cov = np.polyfit(data[0, :], data[1, :], 1, cov=True)[1]  # Get the covariance matrix
m_err, c_err = np.sqrt(np.diag(p_cov))  # Extract the errors from the covariance matrix
print('m_err =', m_err)

plt.plot(data[0,:], m*data[0,:] + c, label='Linear Fit')
#plt.plot(data[3,:], m2*data[3,:] + c2, label='Linear Fit')
#legend with m and c values
plt.legend(title=f'Fit: y = {m:.4f}x + {c:.4f}\nErrors: m_err = {m_err:.4f}, c_err = {c_err:.4f}')
plt.xlabel('Vg (V)')
plt.ylabel('Displacement (pm)')
plt.title('Displacement vs Vg')
plt.show()